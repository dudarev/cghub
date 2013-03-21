import sys
import os.path

from django.utils import simplejson as json

try:
    from collections import OrderedDict
except ImportError:
    from celery.utils.compat import OrderedDict


JSON_FILTERS_FILE_NAME = os.path.join(
                            os.path.dirname(__file__),
                            'filters_storage.json')

if os.path.exists(JSON_FILTERS_FILE_NAME) and not 'test' in sys.argv:
    json_data_file = open(JSON_FILTERS_FILE_NAME, 'r')
else:
    json_data_file = open('%s.default' % JSON_FILTERS_FILE_NAME, 'r')

json_data = json.load(json_data_file, object_pairs_hook=OrderedDict)
DATE_FILTERS_HTML_IDS = json_data[0]
ALL_FILTERS = json_data[1]
