import sys
import os.path

from django.utils import simplejson as json

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.simplejson import OrderedDict


JSON_FILTERS_FILE_NAME = os.path.join(
                            os.path.dirname(__file__),
                            'filters_storage.json')


class Filters(object):
    DATE_FILTERS_HTML_IDS = {}
    ALL_FILTERS = {}

    @classmethod
    def update(self):
        if 'test' in sys.argv:
            json_data_file = open('%s.test' % JSON_FILTERS_FILE_NAME, 'r')
        elif os.path.exists(JSON_FILTERS_FILE_NAME):
            json_data_file = open(JSON_FILTERS_FILE_NAME, 'r')
        else:
            json_data_file = open('%s.default' % JSON_FILTERS_FILE_NAME, 'r')

        json_data = json.load(json_data_file, object_pairs_hook=OrderedDict)
        self.DATE_FILTERS_HTML_IDS = json_data[0]
        self.ALL_FILTERS = json_data[1]


Filters.update()
