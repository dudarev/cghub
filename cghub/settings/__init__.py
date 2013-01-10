import sys

from .default import *
from .admins import *
from .databases import *
from .static import *
from .middleware import *
from .template import *
from .apps import *
from .cart_cache import *
from .api_cache import *
from .debug_toolbar_settings import *
from .celery_settings import *
from .logging_settings import *

if 'test' in sys.argv:
    from tests import *

from .local import *
