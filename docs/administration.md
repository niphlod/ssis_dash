
## Installation
The app runs on the [web2py](http://www.web2py.com) framework.
There are several deployment models available:
 - if you want to use the source version, you need to install web2py.
  Web2py itself is really easy to install: just download the sourcecode zip
  archive from [web2py's site](http://www.web2py.com) and uncompress it in a folder
  (like c:\web2py). Then download this repo as an archive and uncompress it in a folder
  named *init* in the *applications* folder of web2py's repo.
  To start web2py, just launch ```python web2py.py -a yourpassword``` and open the browser
  pointing to ```http://localhost:8000/```
 - if you don't have python you can download the provided binary archive. To start web2py
 you should launch ```web2py.exe -a yourpassword```

The default webserver can handle 30-50 users but is not recommended for heavy or production
enviroments. You should instead read the [deployment chapter](http://web2py.com/books/default/chapter/29/13/deployment-recipes)
on web2py's book (see Windows-->IIS section)

## Configuration
All settings are stored into the appconfig.ini file at the root of the
application.

A tipical config file looks like this

```
[forms]
formstyle = bootstrap3_inline
separator = 

[ssis_dash]
days_span = 15
debug = 0
secret = a secret string
default_message = You're not authorized to any SSISDB instance. Please contact <admin_address> to be added
admin_address = admin@example.com
mode = protected

[instance_01]
connstring = mssql4://username:password@127.0.0.1/SSISDB
description = Production ENV for DWH
name = localhost
style = light-blue

[instance_02]
connstring = mssql4://DRIVER={SQL Server};SERVER=127.0.0.1;DATABASE=SSISDB;UID=all_dbo;PWD=all_dbo
description = Local SSISDB with explicit connectionstring
name = localhost_explicit
style = green

[instance_03]
connstring = mssql4://all_dbo:all_dbo@10.2.10.15/SSISDB
.......

[users_permissions]
default = *
user@example.com = prod*

[db]
uri = mssql4://all_dbo:all_dbo@localhost/ssis_dash
migrate = 0
```

As you can see it contains different sections, namely:

 - **ssis_dash** : common parameters for this app
 - **instance_xx** : backend connections, descriptions, etc
 - **users_permissions** : simple permission stanza for protected mode
 - **db** : typically a sqlite backend, used for only authentication in protected mode

### ssis_dash

**days_span** : number of days to limit diagnostic queries

**debug** : prints timings for backend queries

**secret** : set this to a random string. It'll be used to sign links for the RSS feed

**default_message** : this is shown to your users if they can't access any instance

**admin_address** : set this to your email so users can ask you for permissions

**mode** : can be either *protected* or *public*. The latter is useful when everybody
can see the dashboard (e.g. a little MSSQL shop), or for demo purposes.
When you set it to *protected* authentication kicks in: users need to authenticate
beforehand and you need to set in **users_permissions** the instances they can see.
It's particularly useful for enterprises or for when you'd like to give access to customers,
each one directed at its own instance.

### instance_xx
Every section starting with *instance_* is listed alphabetically (ordered by "name") in the home page.
Every instance has a "name" that is used as part of the "clean url" to access
the dashboard. The "name" parameter must be unique for each instance.
The "connstring" parameter holds the uri of the database.
You can either use the ```mssql4://username:password@hostname/SSISDB``` notation or using an
odbc-like connection string as the one in the example for **instance_02**

**NB** : in order to see every record in SSISDB the user must be at least a member 
of the *ssis_admin* role on SSISDB.
Don't be afraid, this app uses read-only queries.

The **description** bit can be used to describe the instance in detail

**style** is used for the color of the panel. Available values are

```light-blue, red, green, aqua, yellow, blue, navy, teal, olive, lime, orange, fuchsia, purple, maroon, black, gray```

### users_permissions

This section MUST have a **default** value for **public** mode that holds the
instances available to every user.
If you are instead using the **protected** mode, every line must be composed
of the user's email address with its permissions.
Permissions are evaluated with a *glob-like* syntax. A few examples are better
than a thousand words

 - every user can see every instance
 ```
 [ssis_dash]
 mode = public
 ....
 [users_permissions] default = *
 ```
 - every user can see only instances starting with *prod*
 ```
 [ssis_dash]
 mode = public
 ....

 [users_permissions]
 default = prod*
 ```
 - user *user1@example.com* can see only instances starting with *prod*,
   *user2@example.com* can see only instances starting with *dev*
 ```
 [ssis_dash]
 mode = protected
 ....

 [users_permissions]
 user1@example.com = prod*
 user2@example.com = dev*
 ```
 - user *user1@example.com* can see only *prod_dwh* and *quality_dwh*,
  *user2@example.com* can see only *dev_dwh*
 ```
 [ssis_dash]
 mode = protected
 ....

 [users_permissions]
 user1@example.com = prod_dwh,quality_dwh
 user2@example.com = dev_dwh
 ```

You can mix and match *glob* expressions and/or exact instance *name*s, separating
then with a comma.

### db
Here you can set a web2py URI to connect to a database. sqlite is the default backend
but you can use whatever backend you'd like. In this database (db_owner access required)
are created tables to support authentication for **protected** mode


## Compatibility
A modern browser is required for optimal experience.
IE 9+, Android 2.4+, Firefox 20+, Chrome 20+ ... you get the idea.
