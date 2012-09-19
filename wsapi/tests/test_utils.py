#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test some utility methods such as:
    - convertion to string
    - abbreviation to attributes
"""
import os
import unittest

from cghub.wsapi.api import request


TEST_DATA = os.path.join(os.path.dirname(__file__) + '/test_data')


class SortingTest(unittest.TestCase):
    """Test functions that do sorting."""

    def test_tostring(self):
        """
        Tests that tostring method works.
        """
        results = request(file_name=os.path.join(TEST_DATA, 'search.xml'))
        self.assertTrue('ResultSet' in results.tostring())

    def test_remove_attributes(self):
        """
        Tests that attributes are removed with `remove_attributes`.
        """
        results = request(file_name=os.path.join(TEST_DATA, 'aliquot_id.xml'))
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


if __name__ == '__main__':
    unittest.main()
