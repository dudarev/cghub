import djcelery


djcelery.setup_loader()

BROKER_URL = "django://"
