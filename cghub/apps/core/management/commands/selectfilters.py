import os
import pickle
import json
from optparse import make_option


try:
    from collections import OrderedDict
except ImportError:
    from celery.utils.compat import OrderedDict

from django.core.management.base import BaseCommand

from cghub.wsapi.api import request as api_request

JSON_FILTERS_FILE_NAME = 'cghub/apps/core/filters_storage_full.json'
RESULT_FILTERS_FILE_NAME = 'cghub/apps/core/filters_storage.py'
FILTERS_USED_FILE_NAME = 'cghub/apps/core/is_filter_used.pkl'
DATE_RANGES = [
    'upload_date=[NOW-1DAY%20TO%20NOW]',
    'upload_date=[NOW-7DAY%20TO%20NOW]',
    'upload_date=[NOW-1MONTH%20TO%20NOW]',
    'upload_date=[NOW-2MONTH%20TO%20NOW]',
    'upload_date=[NOW-3MONTH%20TO%20NOW]',
    'upload_date=[NOW-6MONTH%20TO%20NOW]',
    'upload_date=[NOW-12MONTH%20TO%20NOW]',
    '',
]


def save_checked(is_filter_used):
    """
    Saves filters for which it is already checked if they exist.
    """
    f = open(FILTERS_USED_FILE_NAME, 'w')
    pickle.dump(is_filter_used, f)
    f.close()


def load_checked():
    """
    Loads already checked filters.
    """
    if os.path.exists(FILTERS_USED_FILE_NAME):
        f = open(FILTERS_USED_FILE_NAME, 'r')
        return pickle.load(f)
    else:
        return {}


def format_dict(d, tab=4 * ' ', padding=''):
    isOrderedDict = isinstance(d, OrderedDict)
    if isOrderedDict:
        s = ['OrderedDict([\n']
    else:
        s = ['{\n']
    for k, v in d.items():
        if isinstance(v, dict) or isinstance(v, OrderedDict):
            v = format_dict(v, tab, padding=padding + tab)
        else:
            v = repr(v)
        if isOrderedDict:
            s.append('%s(%r, %s),\n' % (padding + tab, k, v))
        else:
            s.append('%s%r: %s,\n' % (padding + tab, k, v))
    if isOrderedDict:
        s.append('%s])' % padding)
    else:
        s.append('%s}' % padding)
    return ''.join(s)


class Command(BaseCommand):
    help = 'Check what filters are used.'

    option_list = BaseCommand.option_list + (
        make_option(
            '-c',
            action='store_true',
            dest='clean',
            default=False,
            help='cleans previously pickled checked filters'),
    )

    def handle(self, *args, **options):
        self.stdout.write('Checking filters\n')
        if options['clean']:
            is_filter_used = {}
        else:
            is_filter_used = load_checked()

        json_data_file = open(JSON_FILTERS_FILE_NAME, 'r')
        json_data = json.load(json_data_file)
        ALL_FILTERS = json_data['ALL_FILTERS']
        DATE_FILTERS_HTML_IDS = json_data['DATE_FILTERS_HTML_IDS']

        # populate dict is_filter_used
        # { (filter_name, filter_value): True/False }
        for key in ALL_FILTERS.keys():
            if key in ('last_modified', 'upload_date'):
                continue
            self.stdout.write(key)
            self.stdout.write('\n')
            for filter in ALL_FILTERS[key]['filters']:
                self.stdout.write('  %s\n' % filter)
                if (key, filter) in is_filter_used:
                    self.stdout.write('this filter is already checked, is_used: %s\n' %
                                      is_filter_used[(key, filter)])
                else:
                    self.stdout.write('checking filter\n')
                    is_filter_used[(key, filter)] = False
                    for date in DATE_RANGES:
                        query = '%s=%s&%s' % (key, filter, date)
                        self.stdout.write('query: %s\n' % query)
                        results = api_request(query=query, get_attributes=False)
                        hits = int(results.Hits.text)
                        if hits:
                            is_filter_used[(key, filter)] = True
                            break
                    self.stdout.write('is_used: %s\n' %
                                      is_filter_used[(key, filter)])
                    save_checked(is_filter_used)
                self.stdout.write('\n')

        # delete those filters that are not used
        for key in ALL_FILTERS:
            if key in ('last_modified', 'upload_date'):
                continue
            self.stdout.write(key)
            self.stdout.write('\n')
            for filter in ALL_FILTERS[key]['filters'].keys():
                if not is_filter_used[(key, filter)]:
                    self.stdout.write('  deleting %s\n' % filter)
                    del ALL_FILTERS[key]['filters'][filter]

        filter = open(RESULT_FILTERS_FILE_NAME, 'w')
        filter.write(''.join([
            'DATE_FILTERS_HTML_IDS = ', format_dict(DATE_FILTERS_HTML_IDS),'\n',
            'ALL_FILTERS = ', format_dict(ALL_FILTERS)
        ]))
        filter.close()
        self.stdout.write('\n\nFile %s is created\n' % RESULT_FILTERS_FILE_NAME)
