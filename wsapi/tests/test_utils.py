#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from wsapi.utils import generate_tmp_file_name, quote_query, prepare_query


class UtilsTestCase(unittest.TestCase):

    def test_generate_tmp_file_name(self):
        """
        smoke test for generate_tmp_file_name function
        """
        name = generate_tmp_file_name()
        self.assertIn('.tmp', name)

    def test_quote_query(self):
        """
        upload_date=[NOW-7DAY TO NOW]&state=(live)&last_modified=[NOW-1DAY TO NOW]
        ->
        upload_date=%5BNOW-7DAY%20TO%20NOW%5D&state=%28live%29&last_modified=%5BNOW-1DAY%20TO%20NOW%5D
        """
        query = 'upload_date=[NOW-7DAY TO NOW]&state=(live)&last_modified=[NOW-1DAY TO NOW]'
        self.assertEqual(quote_query(query),
                'upload_date=%5BNOW-7DAY%20TO%20NOW%5D&state=%28live%29&'
                'last_modified=%5BNOW-1DAY%20TO%20NOW%5D')

    def test_prepare_query(self):
        """
        Quoting, limit -> rows, offset -> first, - -> :desc
        """
        # quoting
        query = 'upload_date=[NOW-7DAY TO NOW]&state=(live)&last_modified=[NOW-1DAY TO NOW]'
        self.assertEqual(prepare_query(query),
                'upload_date=%5BNOW-7DAY%20TO%20NOW%5D&state=%28live%29&'
                'last_modified=%5BNOW-1DAY%20TO%20NOW%5D')
        # limit, offset
        query = 'upload_date=[NOW-7DAY TO NOW]&state=(live)'
        self.assertEqual(prepare_query(query, limit=10, offset=20),
                'upload_date=%5BNOW-7DAY%20TO%20NOW%5D&state=%28live%29&start=20&rows=10')
        # sort_by
        query = 'upload_date=[NOW-7DAY TO NOW]&state=(live)'
        self.assertEqual(prepare_query(query, sort_by='last_modified'),
                'upload_date=%5BNOW-7DAY%20TO%20NOW%5D&state=%28live%29&sort_by=last_modified:asc')
        # sort_by -
        query = 'upload_date=[NOW-7DAY TO NOW]&state=(live)&sort_by=-last_modified'
        self.assertEqual(prepare_query(query, sort_by='-last_modified'),
                'upload_date=%5BNOW-7DAY%20TO%20NOW%5D&state=%28live%29&sort_by=last_modified:desc')
        # not allowed sort_by
        query = 'upload_date=[NOW-7DAY TO NOW]&state=(live)'
        self.assertEqual(prepare_query(query, sort_by='badsortby'),
                'upload_date=%5BNOW-7DAY%20TO%20NOW%5D&state=%28live%29')


if __name__ == '__main__':
    unittest.main()
