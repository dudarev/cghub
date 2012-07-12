# -*- coding: utf-8 -*-

"""
cghub_api
~~~~~~~~~

:copyright: (c) 2012 CGHub UCSC
:license: New BSD, see ../LICENSE for more details.

"""

__title__ = 'cghub_api'
__version__ = '0.0.3'
__author__ = 'Artem Dudarev'
__license__ = 'New BSD'
__copyright__ = 'Copyright 2012 CGHub UCSC'


from .api import request
from .exceptions import (
    RequestException, QueryRequired,
)
