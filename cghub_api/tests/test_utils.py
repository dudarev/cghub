#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test some utility methods such as:
    - convertion to string
    - abbreviation to attributes
"""

import unittest

from cghub_api.api import request


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
        results = request(file_name='tests/test_data/search.xml')
        results.remove_attributes()
        removed_attributes = ['sample_accession', 'legacy_sample_id', 
                'disease_abbr', 'tss_id', 'participant_id', 'sample_id',
                'analyte_code', 'sample_type', 'library_strategy',
                'platform', 'analysis_xml', 'run_xml', 'experiment_xml',]
        for a in removed_attributes:
            self.assertRaises(AttributeError, getattr(results, a))
        # new attribute that must be there
        self.assertTrue(results.analysis_attribute_uri)


if __name__ == '__main__':
    unittest.main()
