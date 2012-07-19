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
