import logging
from celery.signals import after_setup_logger, after_setup_task_logger
from django.conf import settings


def after_setup_logger_handler(sender=None, logger=None, loglevel=None,
                                logfile=None, format=None,
                                colorize=None, **kwds):
    """
    Setup loggers for celery
    """
    handler = logging.handlers.SysLogHandler(address=settings.SYSLOG_ADDRESS)
    handler.setFormatter(logging.Formatter(format))
    handler.setLevel(loglevel or logging.INFO)
    logger.addHandler(handler)

after_setup_logger.connect(after_setup_logger_handler)
after_setup_task_logger.connect(after_setup_logger_handler)
