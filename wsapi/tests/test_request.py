#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from wsapi.api import Request


class RequestTest(unittest.TestCase):
    """
    Just smoke tests.
    """

    def test_request_paginated(self):
        query = 'all_metadata=TCGA-04-1337-01A-01W-0484-10'
        result = Request(query=query, offset=0, limit=10)
        self.assertTrue(len(result.results))

    def test_request_only_ids(self):
        query = 'all_metadata=TCGA-04-1337-01A-01W-0484-10'
        result = Request(query=query, only_ids=True)
        self.assertTrue(len(result.results))
        self.assertEqual(len(result.results), result.hits)

    def test_request_with_callback(self):
        query = 'all_metadata=TCGA-04-1337-01A-01W-0484-10'
        data = []
        def callback(attributes):
            data.append(attributes)
        result = Request(query=query, callback=callback)
        self.assertTrue(len(data))
        self.assertEqual(len(data), result.hits)
        self.assertTrue(data[0]['files'][0]['checksum']['@type'])
        self.assertFalse(result.xml)

    def test_request_full_and_xml(self):
        analysis_id = '916d1bd2-f503-4775-951c-20ff19dfe409'
        result = Request(
                        query='analysis_id=%s' % analysis_id,
                        full=True, with_xml=True)
        self.assertTrue(len(result.results))
        self.assertTrue(result.xml)
        self.assertIn('analysis_id', result.xml)
        self.assertIn('analysis_xml', result.xml)


if __name__ == '__main__':
    unittest.main()
