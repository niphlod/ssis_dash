# -*- coding: utf-8 -*-
# Copyright 2017 Niphlod <niphlod@gmail.com>
#
# This file is part of ssis_dash.
#
# ssis_dash is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# ssis_dash is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ssis_dash. If not, see <http://www.gnu.org/licenses/>.

import gluon.contrib.rss2 as rss2
from gluon.storage import List
import hashlib
import os
from collections import defaultdict
import time
import glob
import datetime

CACHE_FOR = 60
PRUNING = CACHE_FOR * 100


class NoOutput:
    def __init__(self):
        pass

    def publish(self, handler):
        pass


class CDATARSS2(rss2.RSSItem):
    def __init__(self, **kwargs):
        rss2.RSSItem.__init__(self, **kwargs)

    def publish(self, handler):
        self.do_not_autooutput_description = self.description.decode('utf8')
        self.description = NoOutput()  # This disables the Py2GenRSS "Automatic" output of the description, which would be escaped.
        rss2.RSSItem.publish(self, handler)

    def publish_extensions(self, handler):
        handler._write('<%s><![CDATA[%s]]></%s>' % ("description", self.do_not_autooutput_description, "description"))


def TDNW(el):
    return TD(el, _nowrap='')


def feed():
    request.args = List(request.raw_args.split('/'))
    if not URL.verify(request, hmac_key=SIGN_KEY):
        raise HTTP(403, 'invalid signature')
    rtn = recalc_token(user=request.get_vars.user)
    if request.args(0) not in rtn:
        raise HTTP(403, 'instance not valid')
    request.extension = 'rss'
    rargs = List(request.raw_args.split('/'))
    fname = "%s.rss" % hashlib.md5('/'.join(rargs)).hexdigest()
    basepath = os.path.join(request.folder, 'private', 'temp_feeds')
    if not os.path.exists(basepath):
        os.makedirs(basepath)
    fpath = os.path.join(basepath, fname)
    lock_file = fpath + '.__lock'
    return_cached = os.path.isfile(lock_file)
    if not return_cached:
        return_cached = os.path.isfile(fpath) and time.time() - os.path.getmtime(fpath) < CACHE_FOR
    if return_cached:
        x = 0
        while x < 60:
            x += 1
            if os.path.isfile(fpath):
                with open(fpath, 'rb') as g:
                    rtn = g.read()
                return rtn
    with open(lock_file, 'w') as g:
        g.write('%s' % request.utcnow)
    folder = rargs(2) if rargs(1) == 'folder' else 'all'
    project = rargs(4) if rargs(3) == 'project' else 'all'
    status = rargs(6) if rargs(5) == 'status' else 'all'
    package = rargs(8) if rargs(7) == 'package' else 'all'
    folder_pattern = folder != 'all' and fixup_like_param(folder) or '%'
    project_name = project != 'all' and fixup_like_param(project) or '%'
    package_pattern = package != 'all' and fixup_like_param(package) or '%'
    status_ = status != 'all' and status or 'all'
    status = 0
    for k, v in STATUS_CODES.iteritems():
        if status_ == v:
            status = k
            break
    res = read_and_exec('package-list.sql', placeholders=(HOURSPAN, folder_pattern, project_name, package_pattern, status), as_dict=True)
    msgs = read_and_exec('package-messages.sql', placeholders=(HOURSPAN, folder_pattern, project_name, package_pattern, status), as_dict=True)
    res = massage_resultset(res)
    msgs = massage_resultset(msgs)
    msgs_dict = defaultdict(list)
    for msg in msgs:
        msgs_dict[msg.operation_id].append(msg)
    title = "SSIS Dashboard: Executions for %s" % request.args(0)
    title += folder != 'all' and ', folder %s' % folder or ''
    title += project != 'all' and ', project %s' % project or ''
    title += status != 'all' and ', status %s' % STATUS_CODES[status] or ''
    title += package != 'all' and ', package %s' % package or ''
    items = []
    for entry in res:
        now = request.utcnow.strftime('%Y%m%d%H%M%S')
        link = URL('console', 'overview', host=True, scheme='https', extension='', args=[request.args(0), 'folder', entry.folder_name, 'project',
                            entry.project_name, 'status', 'all', 'package', entry.package_name, 'execution', entry.execution_id])
        if entry.elapsed_time_min is None:
            guid = link + '@' + now
        else:
            guid = link + '@now'
        detailed_status = [
            ['Status', STATUS_CODES[entry.status]],
            ['Elapsed (min)', entry.elapsed_time_min]
        ]
        errors = None
        if entry.execution_id in msgs_dict:
            errors = 0
            warnings = 0
            for m in msgs_dict[entry.execution_id]:
                if m.event_name == 'OnWarning':
                    warnings += 1
                if m.event_name == 'OnError':
                    errors += 1
            detailed_status.extend([
                ['Errors', errors],
                ['Warnings', warnings],
            ])
            err_rows = msgs_dict[entry.execution_id]
            messages = [[TDNW('Event Name'), TDNW('Message Time (UTC)'), TDNW('Message'), TDNW('Package'),
                        TDNW('Package Path'), TDNW('Subcomponent Name'), TDNW('Execution Path')]]
            for msg in err_rows:
                messages.append([TDNW(msg.event_name), TDNW(msg.message_time), TD(msg.message), TDNW(msg.package_name),
                    TD(msg.package_path), TDNW(msg.subcomponent_name), TD(msg.execution_path)])
            errors = TABLE(
                [TR(
                    [a for a in msg]
                    ) for msg in messages]
                ,_border=1)
        detailed_status = TABLE(
            [TR([TD(el) for el in row]) for row in detailed_status]
            )
        if errors:
            detailed_status = detailed_status.xml() + '<hr />' + errors.xml()
        else:
            detailed_status = detailed_status.xml()
        pubdate = request.now
        if entry.end_time:
            pubdate = datetime.datetime.strptime(entry.end_time, '%Y-%m-%d %H:%M:%S')
        items.append(
            CDATARSS2(
               title="%s - %s - (%s)" % (entry.execution_id, entry.package_name, STATUS_CODES[entry.status]),
               link=link,
               author="%s/%s@%s" % (entry.folder_name, entry.project_name, request.args(0)),
               guid=guid,
               description=detailed_status,
               pubDate=pubdate,
               )
            )
    rss = rss2.RSS2(title=title,
                    link=URL(args=request.args, scheme='https', host=True),
                    description="Execution Packages",
                    ttl=CACHE_FOR,
                    lastBuildDate=request.utcnow,
                    items=items)
    rtn = rss.to_xml(encoding='utf-8')
    if not os.path.exists(os.path.dirname(fpath)):
        os.makedirs(os.path.dirname(fpath))
    with open(fpath, 'wb') as g:
        g.write(rtn)
    try:
        os.unlink(lock_file)
    except:
        pass

    # can we do some cleaning ?
    allfiles = glob.glob(os.path.join(basepath, '*.rss'))
    for fpath in allfiles:
        if os.path.isfile(fpath) and time.time() - os.path.getmtime(fpath) > PRUNING:
            try:
                os.unlink(fpath)
            except:
                pass
    # this should never happen
    allfiles = glob.glob(os.path.join(basepath, '*.__lock'))
    for fpath in allfiles:
        if os.path.isfile(fpath) and time.time() - os.path.getmtime(fpath) > 120:
            try:
                os.unlink(fpath)
            except:
                pass
    return rtn
