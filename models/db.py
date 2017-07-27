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


## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myappconfig = AppConfig(reload=True)


from gluon.tools import Auth, Service

service = Service()

response.generic_patterns = ['*'] if request.is_local else []

mode = myappconfig.take('ssis_dash.mode')

response.formstyle = myappconfig.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myappconfig.take('forms.separator')


if mode == 'protected':
    db = DAL(myappconfig.take('db.uri'), pool_size=myappconfig.take('db.pool_size', cast=int), check_reserved=['all'])

    auth = Auth(db)

    ## create all tables needed by auth if not custom tables
    auth.define_tables(username=False, signature=False)

    ## configure email
    mail = auth.settings.mailer
    mail.settings.server = 'logging' or 'smtp.gmail.com:587'
    mail.settings.sender = 'you@gmail.com'
    mail.settings.login  = 'username:password'

    ## configure auth policy
    auth.settings.registration_requires_verification = False
    auth.settings.registration_requires_approval = False
    auth.settings.reset_password_requires_verification = True
