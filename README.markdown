There are two projects here 

`cghub` - web interface to CGHub data written with Django
`cghub_api` - Python API to this data

API is used by the cghub the Django app.

## Makefile targets

### Testing

- `make test` - test both projects
- `make test_api` - only API
- `make test_web` - test Django app

### Running

- `make run` - run Django app
- `make celeryd` - launch Celery daemon to control caches cleaning
- `make celeryd_stop` - stop Celery daemon

### Compiling statics

- `make less` - create static CSS from LESS files
- `make minjs` - minify JavaScript

## Documentation

Documentation for each project in Sphinx format may be found in

`cghub/docs`
`cghub_api/docs`

In each case it can be built with `make html` command from those directories. 
One more target was added to Makefile:
`make serve` so that the documentation is rebuilt and served at 

http://localhost:8002
http://localhost:8001

