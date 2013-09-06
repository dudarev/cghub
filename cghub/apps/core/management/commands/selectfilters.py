import string

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.simplejson import OrderedDict

from django.core.management.base import BaseCommand
from django.utils import simplejson as json

from cghub.apps.core.attributes import DATE_ATTRIBUTES
from cghub.apps.core.filters_storage_full import ALL_FILTERS, DATE_FILTERS_HTML_IDS
from cghub.apps.core.filters_storage import JSON_FILTERS_FILE_NAME
from cghub.apps.core.requests import RequestDetail, RequestID


class FiltersProcessor(object):
    """
    procesor = FiltersProcessor()
    options = processor.process(filter_name='refassem_short_name', options=OrderedDict([
        ('NCBI37/HG19', OrderedDict([
            ('HG19', 'HG19'),
            ('HG19_Broad_variant', 'HG19_Broad_variant'),
        ])),
        ('GRCh37', 'GRCh37'),
    ]))
    assert options == OrderedDict([
        ('HG19 OR HG19_Broad_variant', 'NCBI37/HG19'),
        ('HG19', ' - HG19'),
        ('HG19_Broad_variant', ' - HG19_Broad_variant'),
        ('GRCh37', 'GRCh37'),
    ])
    options = processor.process(...)
    ...
    print processor.new_options
    """

    def __init__(self, stdout):
        self.stdout = stdout
        self.new_options = {}
        self.CHARACTERS = string.ascii_uppercase + '0123456789' + string.ascii_lowercase

    def filter_all_items(self, filter_name):
        api_request = RequestID(query={filter_name: '*'}, limit=5)
        try:
            result = api_request.call().next()
        except StopIteration:
            return 0
        return api_request.hits

    def process(self, filter_name, options):
        self.new_options[filter_name] = []
        used_options = []
        all_count = self.filter_all_items(filter_name=filter_name)
        count = 0

        for option_name, option_value in options.iteritems():
            api_request = RequestID(query={filter_name: option_value}, limit=5)
            try:
                result = api_request.call().next()
            except StopIteration:
                continue
            count += api_request.hits
            if api_request.hits:
                used_options.append(option_name)

        if count < count_all:
            self.new_options[filter_name] = list(
                    set(self.get_all_filters(filter_name=filter_name, count_all=count_all)) -
                    set(used_options))
        return used_options + self.new_options[filter_name]

    def get_all_filters(self, filter_name, start='', count_all=None):
        options = []
        count = 0
        for c in self.CHARACTERS:
            query = {key: '%s%s*' % (start, c)}
            api_request = RequestDetail(
                    query=query, limit=5, sort_by=filter_name)
            try:
                result = api_request.call().next()
            except StopIteration:
                continue
            count += api_request.hits
            if api_request.hits:
                options.append(result.get(filter_name))
                if count_all and count_all == count:
                    return options
                api_request = RequestDetail(
                        query=query, limit=5, sort_by='-%s' % key)
                try:
                    result = api_request.call().next()
                except StopIteration:
                    result = None
                # if some other filters which starts from start+c exists
                if result and result.get(key) not in options:
                    for f in self.get_all_filters(
                            filter_name=filter_name,
                            start='%s%s' % (start, c),
                            count_all=api_request.hits):
                        if f not in options:
                            options.append(f)
        return options


class Command(BaseCommand):
    help = 'Check what filters are used.'

    def handle(self, *args, **options):

        self.stdout.write('Checking filters\n')

        used_filters = {}
        unused_filters = {}
        new_filters = {}

        for key in ALL_FILTERS:
            if not ALL_FILTERS[key].get('selectFilter', True):
                continue

            # get all results count
            api_request = RequestID(query={key: '*'}, limit=5)
            try:
                result = api_request.call().next()
            except StopIteration:
                pass

            count_all = api_request.hits

            self.stdout.write('Checking %s filters\n' % key)

            used_filters[key] = []
            unused_filters[key] = []
            new_filters[key] = []
            count = 0

            for option_name, option_value in ALL_FILTERS[key]['filters'].iteritems():
                self.stdout.write('- Filter %s ... ' % option_name)
                api_request = RequestID(query={key: option_value}, limit=5)
                try:
                    result = api_request.call().next()
                except StopIteration:
                    pass
                count += api_request.hits
                if api_request.hits:
                    self.stdout.write('added\n')
                    used_filters[key].append(option_value)
                else:
                    self.stdout.write('removed\n')
                    unused_filters[key].append(option_name)
            if count < count_all:
                self.stdout.write(
                        'Some other filters for %s exists (%d from %d).\n' % (
                                        key, count_all - count, count_all))
                self.stdout.write('Searching for other filters ...\n')
                new_filters[key] = list(
                        set(get_all_filters(
                                stdout=self.stdout,
                                key=key, count_all=count_all)) -
                        set(used_filters[key]))

        # delete those filters that are not used
        self.stdout.write('Removing those filters that are not used ...\n')
        for key in ALL_FILTERS:
            if not ALL_FILTERS[key].get('selectFilter', True):
                continue
            for option in unused_filters[key]:
                del ALL_FILTERS[key]['filters'][option]
                self.stdout.write('- Removed %s:%s\n' % (key, option))

        # add new filters that are not present in filters_storage_full.py
        self.stdout.write('Adding new filters ...\n')
        for key in ALL_FILTERS:
            if not ALL_FILTERS[key].get('selectFilter', True):
                continue
            for option in new_filters[key]:
                ALL_FILTERS[key]['filters'][option] = option
                self.stdout.write('- Added new filter %s:%s\n' % (key, option))
                self.stdout.write('! Please add this filter to filters_storage_full.py\n')
            # sorting by key
            ALL_FILTERS[key]['filters'] = OrderedDict(
                            sorted(ALL_FILTERS[key]['filters'].items()))

        # modify filters dicts {name: query} -> {query: name}
        # add spaces for suboptions
        for key in ALL_FILTERS:
            if key in DATE_ATTRIBUTES:
                continue
            new_filters = []
            for name, value in ALL_FILTERS[key]['filters']:
                
                new_filters.append((value, name))

        # write filters found to filters_storage.json
        json_filters = open(JSON_FILTERS_FILE_NAME, 'w')
        json.dump([DATE_FILTERS_HTML_IDS, ALL_FILTERS], json_filters, indent=2)
        json_filters.close()
        self.stdout.write('\nWrote to %s.\n' % JSON_FILTERS_FILE_NAME)
