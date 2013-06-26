#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os.path

from xml.sax import parseString

from wsapi.parsers import IDsParser, AttributesParser


class ParsersTestCase(unittest.TestCase):

    def test_ids_parser(self):
        current_dir = os.path.dirname(__file__)
        xml = open(os.path.join(
                current_dir, 'test_data/analysisid.xml'), 'r').read()
        ids = []
        def callback(value):
            ids.append(value)
        parser = IDsParser(callback)
        parseString(xml, parser)
        self.assertEqual(parser.hits, 2)
        self.assertEqual(len(ids), 2)
        self.assertTrue('916d1bd2-f503-4775-951c-20ff19dfe409' in ids)

    def test_attributes_padser(self):
        current_dir = os.path.dirname(__file__)
        xml = open(os.path.join(
                current_dir, 'test_data/analysisdetail.xml'), 'r').read()
        data = []
        def callback(attributes):
            data.append(attributes)
        parser = AttributesParser(callback)
        parseString(xml, parser)
        self.assertEqual(parser.hits, 2)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['analysis_id'], '55c0d3e7-b6e8-40d4-8a3e-73771a747c95')
        self.assertTrue('center_name' in data[0])


if __name__ == '__main__':
    unittest.main()
