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
Less is used to maintain stylesheets.
Client side less compilator is used in developement environment.

Some requirements should be satisfied to compile static files from less
to css and javascript minification for production environment.

1. Install node.js (http://nodejs.or)
2. Install npm (http://npm.org)
    ```bash
    curl http://npmjs.org/install.sh | sh)
    ```
3. Install grunt:
    ```bash
    npm install -g grunt
    ```
4. Install grunt-less:
    ```bash
    npm install -g grunt-less
    ```

To compile from less to css use less target:

```bash
make less
```

To minify js use minjs target:

```bash
make minjs
```
