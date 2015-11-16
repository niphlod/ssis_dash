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

import datetime
from gluon.serializers import json
import fnmatch

def overview():
    if request.args(0) not in INSTANCE_VALID_ARG:
        non_valid_instance()
    curr_env = {
        'base_url': URL('console', 'overview'),
    }

    return dict(curr_env=json(curr_env))


def history():
    if request.args(0) not in INSTANCE_VALID_ARG:
        non_valid_instance()
    curr_env = {
        'base_url': URL('console', 'history')
    }
    return dict(curr_env=json(curr_env))


def rssfeed():
    request.extension = 'json'
    if request.args(0) not in INSTANCE_VALID_ARG:
        non_valid_instance()
    mode = myappconfig.take('ssis_dash.mode')
    if mode == 'public':
        user = 'default'
    elif mode == 'protected':
        user = auth.user.email
    rtn = {
        'feed_url': URL('subscriptions', 'feed', extension='', args=request.raw_args.split('/'), vars={'user' : user}, hmac_key=SIGN_KEY)
    }
    return json(rtn)
