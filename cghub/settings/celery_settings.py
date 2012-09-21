import os
import djcelery
from distutils.util import strtobool

from cart_cache import TIME_CHECK_CART_CACHE_INTERVAL
from api_cache import TIME_CHECK_API_CACHE_INTERVAL

djcelery.setup_loader()
# if strtobool(os.environ.get("TESTING", "no")):
#     CELERY_ALWAYS_EAGER = True
#     CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

BROKER_URL = "django://"
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
