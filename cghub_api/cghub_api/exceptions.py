# -*- coding: utf-8 -*-

"""
cghub_api.exceptions
~~~~~~~~~~~~~~~~~~~~

This module contains the set of cghub_api's exceptions.

"""

class RequestException(RuntimeError):
    """There was an ambiguous exception that occurred while handling your
    request."""

class QueryRequired(RequestException):
    """Either query parameters or file name must be specified."""
