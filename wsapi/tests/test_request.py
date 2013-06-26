#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from wsapi.api import (request_page, request_ids, request_details,
                                                item_details, item_xml)


class RequestTest(unittest.TestCase):
    """
    Just smoke tests.
    """

    # TODO: mock urlopen
    '''
    def test_request_page(self):
        query = 'all_metadata=TCGA-04-1337-01A-01W-0484-10'
        hits, results = request_page(query=query)

    def test_request_ids(self):
        query = 'all_metadata=TCGA-04-1337-01A-01W-0484-10'
        hits, results = request_ids(query=query)

    def test_request_details(self):
        query = 'all_metadata=TCGA-04-1337-01A-01W-0484-10'
        data = []
        def callback(attributes):
            data.append(attributes)
        hits = request_details(query, callback)
        self.assertTrue(len(data))
        self.assertTrue(data[0]['last_modified'])

    def test_item_details(self):
        analysis_id = '916d1bd2-f503-4775-951c-20ff19dfe409'
        result = item_details(analysis_id=analysis_id)
        result = item_details(analysis_id=analysis_id, with_xml=True)
    
    def test_item_xml(self):
        analysis_id = '916d1bd2-f503-4775-951c-20ff19dfe409'
        xml = item_xml(analysis_id=analysis_id)
        xml, short_xml = item_xml(analysis_id=analysis_id, with_short=True)
        self.assertIn('analysis_id', xml)
        self.assertIn('analysis_xml', xml)
        self.assertIn('analysis_id', short_xml)
        self.assertNotIn('analysis_xml', short_xml)
    '''

if __name__ == '__main__':
    unittest.main()
