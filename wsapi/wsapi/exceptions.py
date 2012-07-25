# -*- coding: utf-8 -*-

"""
wsapi.exceptions
~~~~~~~~~~~~~~~~~~~~

This module contains the set of wsapi's exceptions.

"""

class RequestException(RuntimeError):
    """There was an ambiguous exception that occurred while handling your
    request."""

class QueryRequired(RequestException):
    """Either query parameters or file name must be specified."""
