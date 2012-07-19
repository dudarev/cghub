There are two projects here 

`cghub` - web interface to CGHub data written with Django
`cghub_api` - Python API to this data

API is used by the cghub the Django app.

Documentation for each project in Sphinx format may be found in

`cghub/docs`
`cghub_api/docs`

In each case it can be built with `make html` command. Another target was added:
`make serve` so that the documentation is rebuilt and served at 

http://localhost:8002
http://localhost:8001
