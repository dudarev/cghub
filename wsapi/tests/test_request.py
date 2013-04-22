#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import shutil

from lxml import objectify

from wsapi.exceptions import QueryRequired
from wsapi.api import request, multiple_request
from wsapi.cache import get_cache_file_name
from wsapi.utils import get_setting, makedirs_group_write


class RequestTest(unittest.TestCase):
    """Test request."""

    def test_query_required(self):
        """Test that QuerryRequired exception is raised 
        when function request is called without query and file_name."""
        self.assertRaises(QueryRequired, request)

    def test_invalid_query(self):
        """
        Test that ValueError is raised when not a valid query is passed.
        """
        # test is the first parameter of request() (not valid)
        self.assertRaises(ValueError, request, 'test')

    def test_no_file_exists(self):
        """
        Test that exception is raised when file does not exist.
        """
        self.assertRaises(IOError, request, None, file_name="no_such_file.xml")

    def test_no_exeption_for_existing_file(self):
        """
        Test that no exception is raised when file exists.
        """
        request(file_name='tests/test_data/aliquot_id.xml')

    def test_number_of_items(self):
        """
        Test number of items in one response.
        """
        self.assertEqual(len(request(file_name='tests/test_data/aliquot_id.xml').Result), 1)

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
        Test via EXPERIMENT_REF attribute.
        """
        results = request(file_name='tests/test_data/aliquot_id.xml')
        first_run_experiment_ref = results.Result[0].run_xml.RUN_SET[0].RUN[0].EXPERIMENT_REF
        self.assertEqual(first_run_experiment_ref.attrib['refname'], 
                '7290.WR24924.Catch-62054.B045FABXX110327.P')

    def test_get_cache_file_name(self):
        """
        Test cache file name is determening correctly despite
        the escaped query string
        """
        self.assertEqual(
            get_cache_file_name('last_modified=[NOW-1DAY%20TO%20NOW]',
                        get_attributes=True, full=False, settings={}),
            get_cache_file_name('last_modified=%5BNOW-1DAY%20TO%20NOW%5D',
                        get_attributes=True, full=False, settings={})
        )


class MultipleRequestTestCase(unittest.TestCase):
    cache_files = [
        '427dcd2c78d4be27efe3d0cde008b1f9.xml',
        '9f3c2c0b252739d9bc689d8a26f961d6.xml'
    ]
    extra_cache_file = '5db34dad5dd47469af56179a7d83ebfc.xml'

    def setUp(self):
        """
        Copy cached files to default cache directory.
        """

        TEST_DATA_DIR = 'tests/test_data/'
        cache_dir = get_setting('CACHE_DIR')
        if not os.path.exists(cache_dir):
            makedirs_group_write(cache_dir)
        for f in self.cache_files:
            shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(cache_dir, f)
            )
        self.default_results = objectify.fromstring(open(os.path.join(cache_dir, self.cache_files[0])).read())
        self.default_results_count = len(self.default_results.findall('Result'))

    def tearDown(self):
        for f in self.cache_files:
            os.remove(os.path.join(get_setting('CACHE_DIR'), f))
        os.remove(os.path.join(get_setting('CACHE_DIR'), self.extra_cache_file))

    def test_multiple_request(self):
        queries_list = ['xml_text=6d5%2A', 'xml_text=6d8%2A']
        results = multiple_request(queries_list)
        self.assertEqual(17, len(results.Result))


if __name__ == '__main__':
    unittest.main()
