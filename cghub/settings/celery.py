import djcelery


djcelery.setup_loader()

BROKER_URL = "django://"
CELERY_IMPORTS = (
    "cghub.apps.cart.tasks",
    )
