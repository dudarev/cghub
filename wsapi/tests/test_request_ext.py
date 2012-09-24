#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

from wsapi.api import request
from wsapi.cache import get_cache_file_name


class RequestTest(unittest.TestCase):
    """Test request."""

    def test_returns_something(self):
        """
        A query to external site from docs. Make sure that somethis is returned.
        """
        results = request(query='aliquot_id=087484e8-dc3e-461a-be5f-4217b7c39732')
        self.assertTrue(len(results.Result) > 0)

        # cleaning up temp cache directory
        os.remove(get_cache_file_name('aliquot_id=087484e8-dc3e-461a-be5f-4217b7c39732', True))

if __name__ == '__main__':
    unittest.main()
