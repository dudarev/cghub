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
    procesor = FiltersProcessor(stdout=sys.stdout, selectfilters=False)
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

    :param stdout: sys.stdout
    """

    def __init__(self, stdout):
        self.stdout = stdout
        self.CHARACTERS = string.ascii_uppercase + '0123456789' + string.ascii_lowercase

    def process(self, filter_name, options, selectfilters=False):
        """
        1. Run selectfilters algorithm is selectfilters == True
        2. Process hierarchieal structures
        3. Transorm option/query to query/option

        :param selectfilters: boolean, set to True if need to run selectfilters algorithm
        """

        if selectfilters:
            self.find_all_options(filter_name)
            options = self.select_options(filter_name, options)

        new_dict, all_val = self.open_hierarchieal_structures(options)
        return OrderedDict(new_dict)

    def open_hierarchieal_structures(self, options, depth=0):
        result = []
        val = []
        for option_name, option_value in options.iteritems():
            if isinstance(option_value, OrderedDict):
                if not option_value:
                    # remove empty substructures
                    continue
                new_dict, v = self.open_hierarchieal_structures(
                        option_value, depth=depth + 1)
                val.append(v)
                result.append((' OR '.join(val), option_name))
                for d in new_dict:
                    result.append(d)
            else:
                result.append((
                    option_value,
                    '%s%s' % ('- ' * depth, option_name)))
                val.append(option_value)
        return result, ' OR '.join(val)

    def select_options(self, filter_name, options):
        """
        Remove unused filters and add not existent

        :param filter_name: filter name
        :param filter_values: list of filter options values
        """

        result = []

        for option_name, option_value in options.iteritems():
            if isinstance(option_value, OrderedDict):
                sub_result = self.select_options(filter_name, option_value)
                if not result:
                    continue
                result.append((option_name, sub_result))
            else:
                # check is option was used
                for o in option_value.split(' OR '):
                    if o in self.all_options:
                        break
                else:
                    continue
                result.append((option_name, option_value))
        return OrderedDict(result)

    def find_all_options(self, filter_name):
        api_request = RequestID(query={filter_name: '*'}, limit=5)
        try:
            result = api_request.call().next()
            all_count = api_request.hits
        except StopIteration:
            all_count = 0
        self.all_options = self._all_options(
                filter_name=filter_name,
                all_count=all_count)

    def _all_options(self, filter_name, start='', all_count=None):
        options = []
        count = 0
        for c in self.CHARACTERS:
            query = {filter_name: '%s%s*' % (start, c)}
            api_request = RequestDetail(
                    query=query, limit=5, sort_by=filter_name)
            try:
                result = api_request.call().next()
            except StopIteration:
                continue
            count += api_request.hits
            if api_request.hits:
                options.append(result.get(filter_name))
                if all_count and all_count == count:
                    return options
                api_request = RequestDetail(
                        query=query, limit=5, sort_by='-%s' % filter_name)
                try:
                    result = api_request.call().next()
                except StopIteration:
                    result = None
                # if some other filters which starts from start+c exists
                if result and result.get(filter_name) not in options:
                    for f in self._all_options(
                            filter_name=filter_name,
                            start='%s%s' % (start, c),
                            all_count=api_request.hits):
                        if f not in options:
                            options.append(f)
        return options


class Command(BaseCommand):
    help = 'Check what filters are used.'

    def handle(self, *args, **options):

        processor = FiltersProcessor(stdout=self.stdout)

        for filter_name, filter_data in ALL_FILTERS.iteritems():
            if filter_name in DATE_ATTRIBUTES:
                continue
            options = processor.process(
                    filter_name=filter_name,
                    options=filter_data['filters'],
                    selectfilters=filter_data.get('selectFilter', True))
            filter_data['filters'] = options

        # write filters found to filters_storage.json
        json_filters = open(JSON_FILTERS_FILE_NAME, 'w')
        json.dump([DATE_FILTERS_HTML_IDS, ALL_FILTERS], json_filters, indent=2)
        json_filters.close()
        self.stdout.write('\nWrote to %s.\n' % JSON_FILTERS_FILE_NAME)
