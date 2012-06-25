import logging

from default import *
from admins import *
from databases import *
from static import *
from media import *
from middleware import *
from template import *
from apps import *
from cache import *
from debug_toolbar_settings import *
from celery import *
from logging import *
from tests import *

try:
    from local import *
except:
    print '***cghub/settins/local.py not found***'
