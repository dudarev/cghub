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
        response = request(file_name='tests/test_data/aliquot_id.xml')
        experiment = response[0].EXPERIMENT[1]
        self.assertEqual(experiment.TITLE, 
                'Whole Exome Sequencing of TCGA Lung Squamous tumor/normal pairs')

if __name__ == '__main__':
    unittest.main()
