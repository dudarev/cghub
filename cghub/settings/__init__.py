import logging

from default import *
from admins import *
from databases import *
from static import *
from middleware import *
from template import *
from apps import *
from cart_cache import *
from api_cache import *
from debug_toolbar_settings import *
from celery_settings import *
from logging import *
from tests import *

try:
    from local import *
except:
    print '***cghub/settins/local.py not found***'
