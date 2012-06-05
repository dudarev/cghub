#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from cghub_api.exceptions import QueryRequired
from cghub_api.api import request


class RequestTest(unittest.TestCase):
    """Test request."""

    def test_query_required(self):
        """Test that QuerryRequired exception is raised 
        when function request is called without query and file_name."""
        self.assertRaises(QueryRequired, request)

    def test_returns_something(self):
        """
        Test that something is returned when query is passed.
        TODO: re-write this test to raise exception if query is not allowed."""
        request(query='test')

    def test_no_file_exists(self):
        """
        Test that exception is raised when file does not exist.
        """
        self.assertRaises(IOError, request, None, "no_such_file.xml")

    def test_no_exeption_for_existing_file(self):
        """
        Test that no exception is raised when file exists.
        """
        request(file_name='tests/test_data/aliquot_id.xml')

    def test_number_of_items(self):
        """
        Test number of items in one response.
        """
        self.assertEqual(len(request(file_name='tests/test_data/aliquot_id.xml')), 1)

    def test_item_has_experiment_instance(self):
        """
        Test via experiment title of that instance.
        """
        results = request(file_name='tests/test_data/aliquot_id.xml')
        first_experiment_title = results.Result[0].experiment_xml.EXPERIMENT_SET[0].EXPERIMENT[0].TITLE
        self.assertEqual(first_experiment_title, 
                'Whole Exome Sequencing of TCGA Lung Squamous tumor/normal pairs')

    def test_item_has_analysis_instance(self):
        """
        Test via analysis title of that instance.
        """
        results = request(file_name='tests/test_data/aliquot_id.xml')
        first_analysis_title = results.Result[0].analysis_xml.ANALYSIS_SET[0].ANALYSIS[0].TITLE
        self.assertEqual(first_analysis_title, 
                'NHGRI_TCGA Sequence Alignment/Map for SAMPLE:TCGA:TCGA-55-1594-11A-01D-1040-01:SRS127193')

    def test_item_has_run_instance(self):
        """
        Test via analysis title of that instance.
        """
        results = request(file_name='tests/test_data/aliquot_id.xml')
        first_run_experiment_ref = results.Result[0].run_xml.RUN_SET[0].RUN[0].EXPERIMENT_REF
        self.assertEqual(first_run_experiment_ref.attrib['refname'], 
                '7290.WR24924.Catch-62054.B045FABXX110327.P')


if __name__ == '__main__':
    unittest.main()
