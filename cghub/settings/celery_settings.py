import djcelery

from media import TIME_CHECK_CACHE_INTERVAL

djcelery.setup_loader()

BROKER_URL = "django://"
CELERY_IMPORTS = (
    "cghub.apps.cart.tasks",
    )
CELERYBEAT_SCHEDULE = {
    "every-daily-midnight": {
        "task": "cghub.apps.cart.tasks.cache_clear_task",
        "schedule": TIME_CHECK_CACHE_INTERVAL,
        },
    }
