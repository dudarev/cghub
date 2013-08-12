The `cghub` app - web interface to CGHub data written with Django.
It uses cghub-python-api.
cghub-python-api can be downloaded from
https://github.com/42cc/cghub-python-api

## Makefile targets

### Testing

- `make test` - test Django app
- `make test_ui` - test UI with Selenium, this is not ran as part of `make test`!

### Running

- `make run` - run Django app

### Compiling statics

- `make less` - create static CSS from LESS files
- `make minjs` - minify JavaScript

## Documentation

Documentation for the project in Sphinx format may be found in

`cghub/docs`

It can be built with `make html` command from those directories. 
One more target was added to Makefile:
`make serve` so that the documentation is rebuilt and served at 

<http://localhost:8001>.
