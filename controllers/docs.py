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

import os
from gluon.serializers import json

response.view = 'docs/main.html'

def index():
    with open(os.path.join(request.folder, 'docs', 'index.md')) as g:
        content = g.read()
    return dict(content=json(content))

def administration():
    with open(os.path.join(request.folder, 'docs', 'administration.md')) as g:
        content = g.read()
    return dict(content=json(content))

def user():
    with open(os.path.join(request.folder, 'docs', 'user.md')) as g:
        content = g.read()
    return dict(content=json(content))
