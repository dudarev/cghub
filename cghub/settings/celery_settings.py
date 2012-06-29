from celery.schedules import crontab
import djcelery


djcelery.setup_loader()

BROKER_URL = "django://"
CELERY_IMPORTS = (
    "cghub.apps.cart.tasks",
    )
CELERYBEAT_SCHEDULE = {
    "every-daily-midnight": {
        "task": "cghub.apps.cart.tasks.cache_clear_task",
        "schedule": crontab(minute=0, hour=0),
        },
    }
