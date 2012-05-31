# -*- coding: utf-8 -*-

"""
cghub_api.models
~~~~~~~~~~~~~~~~

This module contains the primary objects that power Requests.
"""

from .exceptions import (
        RequestException, QueryRequired)


class Request(object):
    """The :class:`Request <Request>` object. It carries out all functionality of
    Requests. Recommended interface is with the Requests functions.
    """

    def __init__(self,
            query=None,
            filename=None):
        self.query = query

    def __repr__(self):
        return '<Request [%s]>' % (self.query)

    def send(self, anyway=False, prefetch=False):
        """
        """
        pass


class Response(object):
    """The core :class:`Response <Response>` object. All
    :class:`Request <Request>` objects contain a
    :class:`response <Response>` attribute, which is an instance
    of this class.
    """

    def __init__(self):

        #: Resulting :class:`HTTPError` of request, if one occurred.
        self.error = None

        #: The :class:`Request <Request>` that created the Response.
        self.request = None

    def __repr__(self):
        return '<Response to request [%s]>' % (self.request)
