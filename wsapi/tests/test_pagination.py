from lxml import objectify
import shutil
import os
from django.utils import unittest
from wsapi.api import request
from wsapi.settings import CACHE_DIR


class PaginationTestCase(unittest.TestCase):
    cache_files = [
        '427dcd2c78d4be27efe3d0cde008b1f9.xml'
    ]

    def setUp(self):
        """
        Copy cached files to default cache directory.
        """

        # cache filenames are generated as following:
        # >>> from wsapi.cache import get_cache_file_name
        # >>> get_cache_file_name('xml_text=6d5%2A', True)
        # u'/tmp/wsapi/427dcd2c78d4be27efe3d0cde008b1f9.xml'

        TEST_DATA_DIR = 'tests/test_data/'
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        for f in self.cache_files:
            shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(CACHE_DIR, f)
            )
        self.default_results = objectify.fromstring(open(os.path.join(CACHE_DIR, self.cache_files[0])).read())
        self.default_results_count = len(self.default_results.findall('Result'))

    def tearDown(self):
        for f in self.cache_files:
            os.remove(os.path.join(CACHE_DIR, f))

    def test_pagination_offset_and_limit_are_none(self):
        results = request(query='xml_text=6d5*')
        self.assertEqual(len(results.findall('Result')), self.default_results_count)

    def test_pagination_offset_gt_size(self):
        results = request(query='xml_text=6d5*', offset=self.default_results_count + 1)
        self.assertEqual(len(results.findall('Result')), 0)

    def test_pagination_offset_lt_zero(self):
        results = request(query='xml_text=6d5*', offset=-3, limit=2)
        self.assertEqual(len(results.findall('Result')), 2)

    def test_pagination_offset_gt_zero_limit_gt_size(self):
        offset = 3
        limit = self.default_results_count + offset
        results = request(query='xml_text=6d5*', offset=offset, limit=limit)
        self.assertEqual(len(results.findall('Result')), self.default_results_count - offset)

    def test_pagination_offset_gt_zero_and_lt_size_limit_gt_zero(self):
        results = request(query='xml_text=6d5*', offset=3, limit=3)
        self.assertEqual(len(results.findall('Result')), 3)

if __name__ == '__main__':
    unittest.main()
