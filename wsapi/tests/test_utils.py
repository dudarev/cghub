#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from wsapi.utils import prepare_query, get_setting


class UtilsTestCase(unittest.TestCase):

    def test_get_setting(self):
        server_url = get_setting('CGHUB_SERVER')
        new_url = 'http://someserver.com'
        self.assertIn('http', server_url)
        self.assertNotEqual(server_url, new_url)
        server_url = get_setting(
                    'CGHUB_SERVER', settings={'CGHUB_SERVER': new_url})
        self.assertEqual(server_url, new_url)

    def test_prepare_query(self):
        """
        Quoting, limit -> rows, offset -> first, - -> :desc

        upload_date=[NOW-7DAY TO NOW]&state=(live)&last_modified=[NOW-1DAY TO NOW]
        ->
        upload_date=%5BNOW-7DAY%20TO%20NOW%5D&state=%28live%29&last_modified=%5BNOW-1DAY%20TO%20NOW%5D
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
