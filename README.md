# ssis_dash
SSISDB monitoring

A spin-off of https://github.com/yorek/ssis-dashboard

Developed in web2py (my framework of choice) to engage developers and to ease
distribution. Mainly done to:
- help a great guy (yorek)
- disengage from SSIS Developers requests
- try to code all the frontend in javascript

BTW: sorry guys, it's my first BIG javascript-frontended-app.

User docs are in [docs/user.md](docs/user.md)

Installation procedures are on [docs/administration.md](docs/administration.md)

Release Notes:
- public mode (as yorek's one)
- protected mode (requires authentication)
- protected mode restricts (optionally) available SSISDB instances
- can monitor multiple instances of SSISDB
- rss feeds
- execution history for folder, project and package
- keyboard shortcuts
- navigation refactoring
- live kpi, no page refreshes necessary


TODO:
- [ ] Rest API is basically there. Need to choose a solid authentication scheme (JWT?)
  for out-of-band requests
- [ ] UI improvements: ideally this should become a SPA
- [ ] History management: ATM there are some "FIXME" pieces around
- [ ] Refactoring: use consistent names among all code (both python and javascript)

