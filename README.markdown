There are two projects here 

`cghub` - web interface to CGHub data written with Django
`cghub_api` - Python API to this data

API is used by the cghub the Django app.

To run the app:

```bash
# pay attention to comments

git clone git@github.com:dudarev/cghub.git cghub
cd cghub
cp Makefile.def.default Makefile.def
cp cghub/settings/local.py.default cghub/settings/local.py
mkdir {pids,logs}

# either
mkvirtualenv -r requirements.txt cghub
# or (if not using virtualenvwrapper)
pip install -r requirements

make syncdb
make celeryd

# in another terminal from `cghub` directory
make run
```
## Updating styles

LESS is used to maintain stylesheets.
Client side LESS compilator is used in developement environment.

Some requirements should be satisfied to compile static files from LESS
to CSS and Javascript minification for production environment.

Install both nodejs and npm either via packages

https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager

or directly from

http://nodejs.org http://npm.org

```bash
curl http://npmjs.org/install.sh | sh)
```
Install grunt:
```bash
sudo npm install -g grunt
```
Install grunt-less:
```bash
sudo npm install -g grunt-less
```

To compile from LESS to CSS use `less` target:
```bash
make less
```

To minify js use `minjs` target:
```bash
make minjs
```

## Deployment

It should be pretty standard to deploy the site with Apache mod_wsgi, 
see [documentation on Django site](https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/modwsgi/).

Since, we are using Celery to handle caches the `celeryd` process should be activated. 
In the example of `post_deploy.sh` file local dabase is synced, 
API documentaiton is created,
and `celeryd` process is started.

```bash
# post_deploy.sh
#!/bin/sh

rev_path=`pwd`
config_path=`dirname ${rev_path}`/uwsgi

# syncdb
PYTHONPATH="${config_path}:${rev_path}" django-admin.py syncdb --noinput --settings settings_deploy

# make documentation
cd ${rev_path}/cghub_api/docs/ && make html

# start celeryd process
cd ${rev_path} && make celeryd &
```

It is a good idea to keep database file (in case of sqlite) outside of the code directory if 

```python
# settings_deploy.py
from cghub.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '../deploy.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
```

## Local settings

Local settings in `cghub/settings/local.py` need to be updated. An example:

```python
# cghub/settings/local.py
import os

def rel(*x):
        return os.path.normpath(os.path.join(os.path.abspath\
                                        (os.path.dirname(__file__)), *x))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': rel('..', '..', '..', 'deploy.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
```
