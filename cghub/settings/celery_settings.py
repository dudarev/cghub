import sys
import djcelery

from .cache import TIME_CHECK_CART_CACHE_INTERVAL,  TIME_CHECK_API_CACHE_INTERVAL

djcelery.setup_loader()

CELERY_IMPORTS = (
    "cghub.apps.core.tasks",
    "cghub.apps.cart.tasks",
    )

CELERYBEAT_SCHEDULE = {}

CELERY_RESULT_BACKEND = "amqp"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

if 'test' in sys.argv:
    BROKER_URL = "django://"

CELERYD_CONCURRENCY = 1

CELERYD_MAX_TASKS_PER_CHILD = 5
CELERYD_TASK_TIME_LIMIT = 600 # 10 minutes
