import json

try:
    from collections import OrderedDict
except ImportError:
    from celery.utils.compat import OrderedDict

JSON_FILTERS_FILE_NAME = 'cghub/apps/core/filters_storage.json'

json_data_file = open(JSON_FILTERS_FILE_NAME, 'r')
json_data = json.load(json_data_file, object_pairs_hook=OrderedDict)
DATE_FILTERS_HTML_IDS = json_data[0]
ALL_FILTERS = json_data[1]
