#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import shutil
import unittest

from wsapi.api_light import *
from wsapi.utils import get_setting, makedirs_group_write


class ApiLightTest(unittest.TestCase):
    """Test functions from api_light.py."""

    def test_parse_sort_by(self):
        self.assertEqual(
                    parse_sort_by('study'),
                    'study:asc')
        self.assertEqual(
                    parse_sort_by('-study'),
                    'study:desc')

    def test_get_cache_file_name(self):
        """
        Test that filenames calculated correctly
        """
        filepath = get_cache_file_name(query='xml_text=6d51*', settings={})
        self.assertEqual(
                filepath,
                '%sec0d99a4758829215ef1d7730bb19eb4.ids' % get_setting('CACHE_DIR'))

    def test_get_ids(self):
        """
        Test get ids from cache if cache file exist
        """
        TEST_DATA_DIR = 'tests/test_data/'
        cache_dir = get_setting('CACHE_DIR')
        if not os.path.exists(cache_dir):
            makedirs_group_write(cache_dir)
        f = 'ec0d99a4758829215ef1d7730bb19eb4.ids'
        shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(cache_dir, f))
        ids = get_ids('xml_text=6d51*', 0, 10, settings={})
        self.assertEqual(ids[0], 10)
        self.assertEqual(len(ids[1]), 10)
        self.assertTrue('2a9d16a9-711b-4198-b808-528611aa3b7c' in ids[1])
        os.remove(os.path.join(cache_dir, f))

    def test_get_all_ids(self):
        """
        Test get all ids from cache if cache file exist
        """
        TEST_DATA_DIR = 'tests/test_data/'
        cache_dir = get_setting('CACHE_DIR')
        if not os.path.exists(cache_dir):
            makedirs_group_write(cache_dir)
        f = 'ec0d99a4758829215ef1d7730bb19eb4.ids'
        shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(cache_dir, f))
        ids = get_all_ids('xml_text=6d51*', settings={})
        self.assertEqual(len(ids), 10)
        self.assertTrue('2a9d16a9-711b-4198-b808-528611aa3b7c' in ids)
        os.remove(os.path.join(cache_dir, f))
        # test sorting doesn't matter
        # 1e0d4e80b3c68459fa38ac23185faae7.ids - 'xml_text=6d51*' sorted by study:asc
        # ec0d99a4758829215ef1d7730bb19eb4.ids - 'xml_text=6d51*' unsorted
        # only ec0d99a4758829215ef1d7730bb19eb4.ids contains
        # '9b62b3c9-e33a-4736-8e65-777777777777'
        f = '1e0d4e80b3c68459fa38ac23185faae7.ids'
        shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(cache_dir, f))
        ids = get_all_ids('xml_text=6d51*', settings={})
        self.assertEqual(len(ids), 10)
        self.assertTrue('9b62b3c9-e33a-4736-8e65-777777777777' in ids)
        os.remove(os.path.join(cache_dir, f))
        # test :desc sorting doesn't matter
        # 7e154190657ebbb5ff774b1f0f90f1e0.ids - 'xml_text=6d51*' sorted by upload_date:desc
        # ec0d99a4758829215ef1d7730bb19eb4.ids - 'xml_text=6d51*' unsorted
        # only 7e154190657ebbb5ff774b1f0f90f1e0.ids contains
        # '9b62b3c9-e33a-4736-8e65-888888888888'
        # try to get unsorted
        f = '7e154190657ebbb5ff774b1f0f90f1e0.ids'
        shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(cache_dir, f))
        ids = get_all_ids('xml_text=6d51*', settings={})
        self.assertEqual(len(ids), 10)
        self.assertTrue('9b62b3c9-e33a-4736-8e65-888888888888' in ids)
        os.remove(os.path.join(cache_dir, f))


    def test_request_light_no_results(self):
        """
        Test what returned in case when no results finded
        """
        result = request_light('analysis_id=123-bad-id', 0, 10, settings={})
        self.assertEqual(result[0], 0)

if __name__ == '__main__':
    unittest.main()
