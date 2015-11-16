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

import os
import fnmatch
import time
import hashlib

from gluon.storage import Storage

DEBUG = myappconfig.take('ssis_dash.debug', cast=int)
HOURSPAN = 24 * myappconfig.take('ssis_dash.days_span', cast=int)
SIGN_KEY = myappconfig.take('ssis_dash.secret')

INSTANCES = [v for k, v in sorted(myappconfig.iteritems()) if k.startswith('instance')]

INSTANCES_DICT = {i['name']: i['connstring'] for i in INSTANCES}

INSTANCE_VALID_ARG = session.ssis_dash_instances or []

STATUS_CODES = {
    0: 'all',
    1: 'created',
    2: 'running',
    3: 'cancelled',
    4: 'failed',
    5: 'pending',
    6: 'halted',
    7: 'succeeded',
    8: 'stopping',
    9: 'completed'
}

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def check_auth(user, instance):
    pattern = myappconfig['users_permissions'].get(user, '').split(',')
    for pa in pattern:
        if fnmatch.fnmatch(instance, pa):
            return True

def recalc_token(user=None):
    mode = myappconfig.take('ssis_dash.mode')
    if mode == 'protected':
        if not user:
            if not auth.user_id:
                redirect(URL('default', 'user', args='login', extension='') + '?_next=' + URL(args=request.args, extension=''))
            user = auth.user.email
    elif mode == 'public':
        user = 'default'
    session.ssis_dash_instances = []
    AUTH_INSTANCES = [i for i in INSTANCES if check_auth(user, i['name'])]
    rtn = [i['name'] for i in AUTH_INSTANCES]
    session.ssis_dash_instances = rtn
    return rtn

def non_valid_instance():
    rtn = recalc_token()
    if request.args(0) in rtn:
        redirect(URL(args=request.args, extension=''))
    response.view = 'non_valid_instance.html'
    response.status = 404
    return


def read_and_exec(filepath, **kwargs):
    if DEBUG:
        start = time.time()
    time_expire = kwargs.pop('time_expire', None)
    key = "%s:%s:%s" % (request.args(0), filepath, hashlib.md5("%s" % kwargs).hexdigest())
    if time_expire:
        rtn = cache.ram(key, lambda: fetch_results(filepath, **kwargs), time_expire=time_expire)
    else:
        rtn = fetch_results(filepath, **kwargs)
    if DEBUG:
        print 'Timings : %s, %.2f' % (filepath, (time.time() - start))
    return rtn

def fetch_results(filepath, **kwargs):
    try:
        dbssis = DAL(INSTANCES_DICT[request.args(0)], migrate=False, attempts=1, driver_args={'timeout' : 5}, pool_size=2)
        with open(os.path.join(request.folder, 'queries', filepath)) as g:
            content = g.read()
        rtn = dbssis.executesql(content, **kwargs)
    except:
        raise HTTP(500, 'Unable to execute query')
    return rtn

def massage_resultset(resultset):
    return [Storage(row) for row in resultset]

def fixup_like_param(param):
    return param.replace('*', '%')