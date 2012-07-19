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
