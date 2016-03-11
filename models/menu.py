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

response.logo =  A("SSIS Dashboard", _class="navbar-brand")

response.title = 'SSIS monitoring'
response.subtitle = 'SSISDB monitoring'

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Niphlod <niphlod@gmail.com>'
response.meta.description = 'SSISDB monitoring'
response.meta.keywords = 'SSISDB monitoring'
response.meta.generator = 'Web2py Web Framework'

response.static_version = '0.0.35'
response.static_version_urls = True

response.menu = [
    ('Home', False, URL('default', 'index'), []),
    ('Docs', False, URL('docs', 'index'), []),
]

static_files = [
    'css/nprogress.css',
    'css/adminlte.css',
    'css/font-awesome.min.css',
    'vendor/morris.css',
    'css/layout.css',
    'vendor/datatables/css/datatables.utils.min.css',
    'js/console.js',
    'js/moment.min.js',
    'vendor/datatables/js/jquery.dataTables.min.js',
    'vendor/datatables/js/datatables.utils.min.js',
    'js/nprogress.js',
    'js/jquery.pjax.js',
    'js/lodash.min.js',
    'vendor/raphael.min.js',
    'vendor/morris.min.js',
    'js/signals.min.js',
    'js/uri-iri.min.js',
    'js/crossroads.min.js',
    'js/ractive.js',
    'js/ractive-load.min.js',
    'js/keymaster.min.js',
    'js/marked.min.js',
    'js/app.js'
]

response.files.extend([URL('static', f) for f in static_files])

PJAX_ENV = request.env.http_x_pjax
