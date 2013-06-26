# -*- coding: utf-8 -*-

"""
wsapi
~~~~~~~~~

:copyright: (c) 2012 CGHub UCSC
:license: New BSD, see ../LICENSE for more details.

"""

__title__ = 'wsapi'
__version__ = '0.0.5'
__author__ = 'Oleksandr Polyeno'
__license__ = 'New BSD'
__copyright__ = 'Copyright 2013 CGHub UCSC'


from .api import (
    request_page, request_ids, request_details, item_details, item_xml)
from .exceptions import (
    RequestException, QueryRequired)
