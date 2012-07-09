#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
import unittest

from cghub_api.api import request


class CacheTest(unittest.TestCase):
    """Test functions that do sorting."""

    def setUp(self):
        """
        Copy cached files to default cache directory.
        """
        cache_files = [
                '51132f0c270ef77be56d54cabae862aa.xml'
                ]
        CACHE_DIR = '/tmp/cghub_api/'
        TEST_DATA_DIR = 'tests/test_data/'
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        for f in cache_files:
            shutil.copy(
                    os.path.join(TEST_DATA_DIR, f),
                    os.path.join(CACHE_DIR, f)
                    )

    def test_data_if_from_cache(self):
        """
        Tests that data is obtained from cache directory if it exists there.
        """
        pass


if __name__ == '__main__':
    unittest.main()
