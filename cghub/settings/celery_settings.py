import djcelery

from media import TIME_CHECK_CACHE_INTERVAL
from api_cache import TIME_CHECK_API_CACHE_INTERVAL

djcelery.setup_loader()

BROKER_URL = "django://"
CELERY_IMPORTS = (
    "cghub.apps.cart.tasks",
    "cghub.apps.core.tasks",
    )
CELERYBEAT_SCHEDULE = {
    "every-daily-midnight": {
        "task": "cghub.apps.cart.tasks.cache_clear_task",
        "schedule": TIME_CHECK_CACHE_INTERVAL,
        },
    "clear-api-cache": {
        "task": "cghub.apps.core.tasks.api_cache_clear_task",
        "schedule": TIME_CHECK_API_CACHE_INTERVAL,
        },
    }
