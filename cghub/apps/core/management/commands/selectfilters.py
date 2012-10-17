import os
import pickle
from optparse import make_option


try:
    from collections import OrderedDict
except ImportError:
    from celery.utils.compat import OrderedDict

from django.core.management.base import BaseCommand

from cghub.apps.core.filters_storage_full import ALL_FILTERS
from cghub.wsapi.api import request as api_request


FILE_NAME_FILTERS_USED = 'cghub/apps/core/is_filter_used.pkl'
DATE_RANGES = [
    'last_modified=[NOW-1DAY%20TO%20NOW]',
    'last_modified=[NOW-7DAY%20TO%20NOW]',
    'last_modified=[NOW-1MONTH%20TO%20NOW]',
    'last_modified=[NOW-2MONTH%20TO%20NOW]',
    'last_modified=[NOW-3MONTH%20TO%20NOW]',
    'last_modified=[NOW-6MONTH%20TO%20NOW]',
    'last_modified=[NOW-12MONTH%20TO%20NOW]',
    '',
]


def save_checked(is_filter_used):
    """
    Saves filters for which it is already checked if they exist.
    """
    f = open(FILE_NAME_FILTERS_USED, 'w')
    pickle.dump(is_filter_used, f)
    f.close()


def load_checked():
    """
    Loads already checked filters.
    """
    if os.path.exists(FILE_NAME_FILTERS_USED):
        f = open(FILE_NAME_FILTERS_USED, 'r')
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

        # populate dict is_filter_used
        # { (filter_name, filter_value): True/False }
        for k in ALL_FILTERS:
            if k == 'last_modified':
                continue
            self.stdout.write(k)
            self.stdout.write('\n')
            for f in ALL_FILTERS[k]['filters']:
                self.stdout.write('  %s\n' % f)
                if (k, f) in is_filter_used:
                    self.stdout.write('this filter is already checked, is_used: %s\n' %
                                      is_filter_used[(k, f)])
                else:
                    self.stdout.write('checking filter\n')
                    is_filter_used[(k, f)] = False
                    for d in DATE_RANGES:
                        query = '%s=%s&%s' % (k, f, d)
                        self.stdout.write('query: %s\n' % query)
                        results = api_request(query=query, get_attributes=False)
                        hits = int(results.Hits.text)
                        if hits:
                            is_filter_used[(k, f)] = True
                            break
                    self.stdout.write('is_used: %s\n' %
                                      is_filter_used[(k, f)])
                    save_checked(is_filter_used)
                self.stdout.write('\n')
                
        # delete those filters that are not used
        for k in ALL_FILTERS:
            if k == 'last_modified':
                continue
            self.stdout.write(k)
            self.stdout.write('\n')
            for f in ALL_FILTERS[k]['filters']:
                if not is_filter_used[(k, f)]:
                    self.stdout.write('  deleting %s\n' % f)
                    del ALL_FILTERS[k]['filters'][f]

        filters_storage = open('cghub/apps/core/filters_storage_full.py', 'r').read()
        all_filters_index = filters_storage.index('ALL_FILTERS')
        all_filters_end_index = filters_storage.index('# end of ALL_FILTERS')
        filters_storage = ''.join([
            filters_storage[:all_filters_index],
            'ALL_FILTERS = ',
            format_dict(ALL_FILTERS),
            '\n',
            filters_storage[all_filters_end_index:],
        ])
        f = open('cghub/apps/core/filters_storage_short.py', 'w')
        f.write(filters_storage)
        f.close()
        self.stdout.write('\n\nFile cghub/apps/core/filters_storage_short.py is created\n')
        self.stdout.write('Copy it to cghub/apps/core/filters_storage.py manually\n')
