from lxml import objectify
import shutil
import os
from django.utils import unittest
from cghub_api.api import request
from cghub_api.settings import CACHE_DIR


class PaginationTestCase(unittest.TestCase):
    cache_files = [
        '10f911319953a88d95231b4d63e29434.xml'
    ]

    def setUp(self):
        """
        Copy cached files to default cache directory.
        """

        # cache filenames are generated as following:
        # >>> m = hashlib.md5()
        # >>> m.update('xml_text=6d5*')
        # >>> m.hexdigest()
        # '10f911319953a88d95231b4d63e29434'

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


if __name__ == '__main__':
    unittest.main()
