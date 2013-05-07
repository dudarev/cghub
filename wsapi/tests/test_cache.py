#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
import unittest
import datetime, time

from wsapi.api import request, Results
from wsapi.utils import clear_cache, get_setting, makedirs_group_write


TEST_DATA_DIR = 'tests/test_data/'


class CacheTest(unittest.TestCase):
    """Test functions that do sorting."""

    cache_files = [
        '10f911319953a88d95231b4d63e29434.xml',
    ]

    bad_cache_file = [
        '9a47690bef15473baaab6613ccb0edaf.xml', # query='xml_text=6d7*'
    ]

    def setUp(self):
        """
        Copy cached files to default cache directory.
        """

        cache_dir = get_setting('CACHE_DIR')
        if not os.path.exists(cache_dir):
            makedirs_group_write(cache_dir)
        for f in self.cache_files + self.bad_cache_file:
            shutil.copy(
                    os.path.join(TEST_DATA_DIR, f),
                    os.path.join(cache_dir, f)
                    )

    def tearDown(self):
        for f in self.cache_files + self.bad_cache_file:
            try:
                os.remove(os.path.join(get_setting('CACHE_DIR'), f))
            except OSError:
                pass

    def test_from_file_method(self):
        for f in self.cache_files:
            results = Results.from_file(os.path.join(TEST_DATA_DIR, f), settings={})
            self.assertFalse(results.Result[0].reason == None)

    def test_data_is_from_cache(self):
        """
        Tests that data is obtained from cache directory if it exists there.
        """
        results = request(query='xml_text=6d5*')
        # reason was modified in the test file by hand to 'a very good reason'
        first_result_reason = results.Result[0].reason
        self.assertEqual(first_result_reason, 'a very good reason')

    def test_handling_bad_xml_syntax_in_cache(self):
        """
        Test that no XMLSyntaxError exception is raised when cache file contains bad xml.
        """
        results = request(query='xml_text=6d7*')

    def test_clear_cache(self):
        """
        Test that `clear_cache` function removes old files.
        """
        TEN_DAYS_AGO = datetime.datetime.now() - datetime.timedelta(days=10)
        TEN_DAYS_AGO= time.mktime(TEN_DAYS_AGO.timetuple())
        cache_dir = get_setting('CACHE_DIR')

        for f in self.cache_files:
            os.utime(os.path.join(cache_dir, f), (TEN_DAYS_AGO, TEN_DAYS_AGO))

        # clear cache older than a day
        clear_cache(
                cache_dir=get_setting('CACHE_DIR'),
                older_than=datetime.datetime.now() - datetime.timedelta(days=1))

        for f in self.cache_files:
            self.failIf(os.path.exists(os.path.join(cache_dir, f)))


if __name__ == '__main__':
    unittest.main()
