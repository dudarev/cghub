#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test some utility methods such as:
    - convertion to string
    - abbreviation to attributes
"""

import unittest
from lxml import objectify, etree

from wsapi.api import request, merge_results


class SortingTest(unittest.TestCase):
    """Test functions that do sorting."""

    def test_tostring(self):
        """
        Tests that tostring method works.
        """
        results = request(file_name='tests/test_data/search.xml')
        self.assertTrue('ResultSet' in results.tostring())

    def test_remove_attributes(self):
        """
        Tests that attributes are removed with `remove_attributes`.
        """
        results = request(file_name='tests/test_data/aliquot_id.xml')
        results.remove_attributes()
        attributes_to_remove = ['sample_accession', 'legacy_sample_id', 
                'disease_abbr', 'tss_id', 'participant_id', 'sample_id',
                'analyte_code', 'sample_type', 'library_strategy',
                'platform', 'analysis_xml', 'run_xml', 'experiment_xml',]
        for a in attributes_to_remove:
            self.assertRaises(AttributeError, getattr, results.Result, a)
        # new attribute that must be there
        self.assertEqual(
                results.Result.analysis_attribute_uri,
                "https://cghub.ucsc.edu/cghub/metadata/analysisAttributes/e29aa109-d508-4621-9a92-9f7ff7e0018f"
                )

class XMLMergeTestCase(unittest.TestCase):
    """
    Tests for wsapi.api.merge_results utility
    """
    def test_merge_results(self):
        res1 = request(file_name='tests/test_data/unmerged_1.xml')
        res2 = request(file_name='tests/test_data/unmerged_2.xml')
        xml = merge_results([res1, res2])
        self.assertEqual(5, xml.Hits)
        self.assertEqual(8, xml.countchildren()) # 8 for 5 result, 2 query and 1 hits tags
        self.assertEqual(xml.xpath('/ResultSet/Query'), ['xml_text:6d5*', 'xml_text:6d7*'])

    def test_errors(self):
        try:
            merge_results({})
            assert 'No exception raised when merge_results takes wrong arguments'
        except Exception as e:
            self.assertEqual(e.message, 'xml_results must be tuple or list')

        try:
            merge_results([])
            assert 'No exception raised when merge_results takes wrong arguments'
        except Exception as e:
            self.assertEqual(e.message, 'Nothing to merge!')

    def test_merging_empty_results(self):
        res1 = objectify.fromstring('<ResultSet><Query>query1</Query><Hits>0</Hits></ResultSet>')
        res2 = objectify.fromstring('<ResultSet><Query>query2</Query><Hits>0</Hits></ResultSet>')
        result = merge_results([res1, res2])

        date = result.get('date')
        self.assertEqual(etree.tostring(result),
            '<ResultSet date="%s"><Hits>0</Hits><Query>query2</Query><Query>query1</Query></ResultSet>' % date)

if __name__ == '__main__':
    unittest.main()
