# -*- coding: utf-8 -*-
# Copyright 2015 Niphlod <niphlod@gmail.com>
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
    fpath = os.path.join(request.folder, 'private', 'temp_feeds', fname)
    if os.path.isfile(fpath) and time.time() - os.path.getmtime(fpath) < (600):
        with open(fpath, 'rb') as g:
            rtn = g.read()
        return rtn
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
    res = massage_resultset(res)
    title = "SSIS Dashboard: Executions for %s" % request.args(0)
    title += folder != 'all' and ', folder %s' % folder or ''
    title += project != 'all' and ', project %s' % project or ''
    title += status != 'all' and ', status %s' % STATUS_CODES[status] or ''
    title += package != 'all' and ', package %s' % package or ''
    items = []
    for entry in res:
        link = URL('console', 'overview', host=True, scheme='https', extension='', args=[request.args(0), 'folder', entry.folder_name, 'project',
                            entry.project_name, 'status', 'all', 'package', entry.package_name, 'execution', entry.execution_id])
        items.append(
            rss2.RSSItem(
               title=entry.package_name,
               link=link,
               guid=link + 'now',
               description="Status : %s\n Warnings: %s\n Errors: %s\n Elapsed (min): %s" % (
                    STATUS_CODES[entry.status], entry.warnings, entry.errors, entry.elapsed_time_min),
               pubDate=entry.start_time.replace(' ', 'T'),
               )
            )
    rss = rss2.RSS2(title=title,
                    link=URL(args=request.args, scheme='https', host=True),
                    description="Execution Packages",
                    ttl=10*60,
                    lastBuildDate=request.now,
                    items=items)
    rtn = rss.to_xml(encoding='utf-8')
    if not os.path.exists(os.path.dirname(fpath)):
        os.makedirs(os.path.dirname(fpath))
    with open(fpath, 'wb') as g:
        g.write(rtn)
    return rtn
