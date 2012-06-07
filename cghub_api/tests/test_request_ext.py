#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from cghub_api.api import request


class RequestTest(unittest.TestCase):
    """Test request."""

    def test_returns_something(self):
        """
        A query to external site from docs. Make sure that somethis is returned.
        """
        results = request(query='aliquot_id:087484e8-dc3e-461a-be5f-4217b7c39732')
        self.assertTrue(len(results) > 0)


if __name__ == '__main__':
    unittest.main()
