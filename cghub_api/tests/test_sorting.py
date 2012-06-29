#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from cghub_api.api import request


class SortingTest(unittest.TestCase):
    """Test functions that do sorting."""

    def test_calculate_files_size(self):
        """
        Tests that total files size is calculated correctly.
        """
        results = request(file_name='tests/test_data/search_several_files.xml')
        results.calculate_files_size()
        self.assertEqual(results.Result[0].files_size, 8407199477+10497249326)
        self.assertEqual(results.Result[1].files_size, 10497249326)

if __name__ == '__main__':
    unittest.main()
