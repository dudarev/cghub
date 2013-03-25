import sys

from .default import *
from .admins import *
from .databases import *
from .static import *
from .middleware import *
from .template import *
from .apps import *
from .cache import *
from .wsapi import *
from .ui import *
from .help import *
from .variables import *
from .debug_toolbar_settings import *
from .celery_settings import *
from .logging_settings import *

if 'test' in sys.argv:
    from tests import *

from .local import *
