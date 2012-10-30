import sys
import djcelery

from cart_cache import TIME_CHECK_CART_CACHE_INTERVAL
from api_cache import TIME_CHECK_API_CACHE_INTERVAL

djcelery.setup_loader()

CELERY_IMPORTS = (
    "cghub.apps.cart.tasks",
    "cghub.apps.core.tasks",
    )

CELERYBEAT_SCHEDULE = {
    "clear-cart-cache": {
        "task": "cghub.apps.cart.tasks.cache_clear_task",
        "schedule": TIME_CHECK_CART_CACHE_INTERVAL,
        },
    "clear-api-cache": {
        "task": "cghub.apps.core.tasks.api_cache_clear_task",
        "schedule": TIME_CHECK_API_CACHE_INTERVAL,
        },
    }

CELERY_RESULT_BACKEND = "amqp"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
if 'test' in sys.argv:
    BROKER_URL = "amqp://cghub:cghub@localhost:5672/cghub"

CELERYD_CONCURRENCY = 1
