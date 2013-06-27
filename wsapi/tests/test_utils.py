#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import hashlib
import urllib2

from mock import patch

from wsapi.utils import prepare_query, get_setting, urlopen


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

    def test_get_from_test_cache(self):
        from wsapi.utils import get_from_test_cache
        query = 'all_metadata=TCGA-04-1337-01A-01W-0484-10'
        format = 'xml'
        CACHE_DIR = get_setting('TESTING_CACHE_DIR')
        url = u'{0}{1}?{2}'.format(
            get_setting('CGHUB_SERVER'),
            get_setting('CGHUB_ANALYSIS_ID_URI'),
            query)
        md5 = hashlib.md5(url)
        path = os.path.join(CACHE_DIR, '%s.%s.cache' % (md5.hexdigest(), format))
        if os.path.exists(path):
            os.remove(path)
        settings = {'TESTING_MODE': True}
        result = get_from_test_cache(url, format, settings)
        content = result.read()
        self.assertTrue(content)
        self.assertTrue(os.path.exists(path))
        get_from_test_cache(url, format, settings)
        os.remove(path)

    def urlopen_mock(url):
            raise urllib2.URLError('Connection error')

    @patch('urllib2.urlopen', urlopen_mock)
    def test_urlopen_exceptions(self):
        query = 'all_metadata=TCGA-04-1337-01A-01W-0484-10'
        url = u'{0}{1}?{2}'.format(
                get_setting('CGHUB_SERVER'),
                get_setting('CGHUB_ANALYSIS_ID_URI'),
                query)
        was_exception = False
        settings = {'TESTING_MODE': False}
        try:
            urlopen(url, 'xml', settings)
        except urllib2.URLError as e:
            was_exception = True
            self.assertIn('No response after', str(e))
        except:
            assert False, 'Enother exception than URLError raised'
        self.assertTrue(was_exception)


if __name__ == '__main__':
    unittest.main()
