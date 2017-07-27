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


from gluon.serializers import json
from collections import OrderedDict
from gluon.storage import List

session.forget(response)

request.extension = 'json'

if request.args(0) not in INSTANCE_VALID_ARG:
    non_valid_instance()


def folders():
    res = read_and_exec('engine-projects.sql', as_dict=True, time_expire=600)
    rtn_ = OrderedDict()
    for row in massage_resultset(res):
        if row.folder_id not in rtn_:
            rtn_[row.folder_id] = {'folder_id': row.folder_id, 'name': row.folder_name, 'projects': []}
        rtn_[row.folder_id]['projects'].append(
            {'name': row.project_name, 'desc': row.description}
        )
    thelist_ = []
    for k, v in rtn_.iteritems():
        thelist_.append(v)
    return json(thelist_)

def engine_kpi():

    rargs = List(request.raw_args.split('/'))

    folder = rargs(2) if rargs(1) == 'folder' else 'all'
    project = rargs(4) if rargs(3) == 'project' else 'all'
    package = rargs(6) if rargs(5) == 'package' else 'all'
    folder_pattern = folder != 'all' and fixup_like_param(folder) or '%'
    project_name = project != 'all' and fixup_like_param(project) or '%'
    package_pattern = package != 'all' and fixup_like_param(package) or '%'

    res = read_and_exec('engine-kpi.sql', placeholders=(HOURSPAN, folder_pattern, project_name, package_pattern), as_dict=True, time_expire=60)
    rtn = {}
    for row in massage_resultset(res):
        rtn[STATUS_CODES[row.status_code]] = row.status_count
    return json(rtn)


def package_list():
    rargs = List(request.raw_args.split('/'))
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
    res = read_and_exec('package-list.sql', placeholders=(HOURSPAN, folder_pattern, project_name, package_pattern, status), as_dict=True, time_expire=60)
    return json(res)

def package_config():
    rargs = List(request.raw_args.split('/'))
    execution = rargs(2) if rargs(1) == 'execution' else -1
    res = read_and_exec('package-details-execution-values.sql', placeholders=(execution,), as_dict=True, time_expire=180)
    return json(res)

def package_kpi():
    rargs = List(request.raw_args.split('/'))
    folder = rargs(2) if rargs(1) == 'folder' else 'all'
    project = rargs(4) if rargs(3) == 'project' else 'all'
    package = rargs(6) if rargs(5) == 'package' else 'all'
    execution = rargs(8) if rargs(7) == 'execution' else -1
    folder_pattern = folder != 'all' and fixup_like_param(folder) or '%'
    project_name = project != 'all' and fixup_like_param(project) or '%'
    package_pattern = package != 'all' and fixup_like_param(package) or '%'
    execution = execution != 'all' and execution or -1
    time_expire = 60
    if rargs(2) == 'details':
        execution = rargs(1)
        time_expire = 180
    res = read_and_exec('package-kpi.sql', placeholders=(HOURSPAN, folder_pattern, project_name, package_pattern, execution), as_dict=True, time_expire=time_expire)
    return json(res[0])


def package_info():
    rargs = List(request.raw_args.split('/'))
    execution = rargs(2) if rargs(1) == 'execution' else 0
    res = read_and_exec('package-info.sql', placeholders = (execution,), as_dict=True, time_expire=180)
    res = massage_resultset(res)
    rtn = {}
    res = res[0]
    rtn['folder'] = res.folder_name
    rtn['project'] = res.project_name
    rtn['package_name'] = res.package_name
    rtn['execution'] = execution
    return json(rtn)


def package_children():
    rargs = List(request.raw_args.split('/'))
    execution = rargs(2) if rargs(1) == 'execution' else -1
    res = read_and_exec('package-children.sql', placeholders=(execution,), as_dict=True, time_expire=180)
    return json(res)


def package_executables():
    rargs = List(request.raw_args.split('/'))
    execution = rargs(2) if rargs(1) == 'execution' else -1
    res = read_and_exec('package-executables.sql', placeholders=(execution,), as_dict=True, time_expire=180)

    return json(res)


def package_details():
    rargs = List(request.raw_args.split('/'))
    execution = rargs(2) if rargs(1) == 'execution' else -1
    res = read_and_exec('package-details.sql', placeholders=(execution,), as_dict=True, time_expire=180)

    return json(res)

def package_history():
    rargs = List(request.raw_args.split('/'))
    folder = rargs(2) if rargs(1) == 'folder' else 'all'
    project = rargs(4) if rargs(3) == 'project' else 'all'
    package = rargs(6) if rargs(5) == 'package' else 'all'


    folder_pattern = folder != 'all' and fixup_like_param(folder) or '%'
    project_name = project != 'all' and fixup_like_param(project) or '%'
    package_pattern = package != 'all' and fixup_like_param(package) or '%'
    res = read_and_exec('package-history.sql', placeholders=(folder_pattern, project_name, package_pattern), as_dict=True, time_expire=60)

    return json(res)