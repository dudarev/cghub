#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from wsapi.api import request


TEST_DATA = os.path.join(os.path.dirname(__file__) + '/test_data')
SEARCH_SEVERAL_FILES = os.path.join(TEST_DATA, 'search_several_files.xml')


class SortingTest(unittest.TestCase):
    """Test functions that do sorting."""

    def test_calculate_files_size(self):
        """
        Tests that total files size is calculated correctly.
        """
        results = request(file_name=SEARCH_SEVERAL_FILES)
        results.calculate_files_size()
        self.assertEqual(results.Result[0].files_size, 8407199477+10497249326)
        self.assertEqual(results.Result[1].files_size, 10497249326)

    def test_sort_by_files_size(self):
        results = request(file_name=SEARCH_SEVERAL_FILES)
        results.sort(sort_by='-files_size')
        for i in range(len(results.Result)-1):
            self.assertGreaterEqual(
                results.Result[i].files_size,
                results.Result[i+1].files_size,
                msg='Files size is not sorted for elements: {0}, {1}'.format(i,i+1))

    def test_sort_by_last_modified(self):
        results = request(file_name=SEARCH_SEVERAL_FILES)
        results.sort(sort_by='last_modified')
        for i in range(len(results.Result)-1):
            self.assertLessEqual(
                results.Result[i].last_modified,
                results.Result[i+1].last_modified,
                msg='Upload date is not sorted for elements: {0}, {1}'.format(i,i+1))


if __name__ == '__main__':
    unittest.main()
