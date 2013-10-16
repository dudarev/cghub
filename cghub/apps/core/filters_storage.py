import datetime
import os.path
import sys

from os import stat

from django.utils import timezone, simplejson as json

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.simplejson import OrderedDict


JSON_FILTERS_FILE_NAME = os.path.join(
                            os.path.dirname(__file__),
                            'filters_storage.json')


class Filters(object):
    _DATE_FILTERS_HTML_IDS = {}
    _ALL_FILTERS = {}
    LAST_TIMESTAMP = 0

    @classmethod
    def update(self):
        timestamp = stat(JSON_FILTERS_FILE_NAME).st_mtime
        if timestamp == self.LAST_TIMESTAMP:
            return
        if 'test' in sys.argv:
            json_data_file = open('%s.test' % JSON_FILTERS_FILE_NAME, 'r')
        elif os.path.exists(JSON_FILTERS_FILE_NAME):
            json_data_file = open(JSON_FILTERS_FILE_NAME, 'r')
        else:
            json_data_file = open('%s.default' % JSON_FILTERS_FILE_NAME, 'r')

        json_data = json.load(json_data_file, object_pairs_hook=OrderedDict)
        self._DATE_FILTERS_HTML_IDS = json_data[0]
        self._ALL_FILTERS = json_data[1]
        self.LAST_TIMESTAMP = timestamp

    @classmethod
    def get_date_filters_html_ids(self):
        self.update()
        return self._DATE_FILTERS_HTML_IDS

    @classmethod
    def get_all_filters(self):
        self.update()
        return self._ALL_FILTERS
