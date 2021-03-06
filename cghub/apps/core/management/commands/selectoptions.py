import string

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.simplejson import OrderedDict
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils import simplejson as json

from cghub.apps.core.attributes import DATE_ATTRIBUTES
from cghub.apps.core.filters_storage import JSON_FILTERS_FILE_NAME
from cghub.apps.core.requests import RequestDetail, RequestID
from cghub.settings.filters import ALL_FILTERS, DATE_FILTERS_HTML_IDS


class FiltersProcessor(object):
    """
    procesor = FiltersProcessor(stdout=sys.stdout, stderr=sys.stderr, verbosity=1)
    options = processor.process(filter_name='refassem_short_name', options=OrderedDict([
        ('NCBI37/HG19', OrderedDict([
            ('HG19', 'HG19'),
            ('HG19_Broad_variant', 'HG19_Broad_variant'),
        ])),
        ('GRCh37', 'GRCh37'),
    ]), select_options=False)
    assert options == OrderedDict([
        ('HG19 OR HG19_Broad_variant', 'NCBI37/HG19'),
        ('HG19', ' - HG19'),
        ('HG19_Broad_variant', ' - HG19_Broad_variant'),
        ('GRCh37', 'GRCh37'),
    ])

    :param stdout: sys.stdout
    :param stderr: sys.stderr
    :param verbosity: verbosity level (1,2,3)
    """

    def __init__(self, stdout, stderr, verbosity):
        self.stdout = stdout
        self.stderr = stderr
        self.verbosity = verbosity
        self.new_options_count = 0
        self.CHARACTERS = string.ascii_uppercase + '-_+0123456789' + string.ascii_lowercase

    def process(self, filter_name, options, select_options=False):
        """
        1. Run select options algorithm is select_options == True
        2. Process hierarchieal structures
        3. Transorm option/query to query/option

        :param select_options: boolean, set to True if need to run select_options algorithm
        :param search_for_new_options: boolean, set to True, if need all options be scanned and displayed missing ones
        """

        if select_options:
            self.find_all_options(filter_name)
            self.used_options = []
            options = self.select_options(filter_name, options)
            options = OrderedDict(options)

        new_dict, all_val = self.open_hierarchical_structures(options)
        return OrderedDict(new_dict)

    def find_new_options(self, filter_name, options):
        """
        Search for new options.
        """
        self.find_all_options(filter_name)
        self.used_options = []
        self.select_options(filter_name, options)
        new_options = set(self.all_options) - set(self.used_options)
        for option in new_options:
            self.new_options_count += 1
            self.stderr.write('! New option %s:%s. Please add this option to cghub/settings/filters.py\n' % (filter_name, option))

    def open_hierarchical_structures(self, options, depth=0):
        result = []
        val = []
        for option_name, option_value in options.iteritems():
            if isinstance(option_value, OrderedDict):
                if not option_value:
                    # remove empty substructures
                    continue
                new_dict, v = self.open_hierarchical_structures(
                        option_value, depth=depth + 1)
                val.append(v)
                result.append((
                    v,
                    '%s%s' % ('-' * depth, option_name)))
                for d in new_dict:
                    result.append(d)
            else:
                result.append((
                    option_value,
                    '%s%s' % ('-' * depth, option_name)))
                val.append(option_value)
        return result, ' OR '.join(val)

    def check_in_all_options(self, query):
        """
        self.all_options == ['CGTEST', 'Homo sapiens Other_Sequencing_Multiisolate', 'phs000467', ...]
        contains *Other_Sequencing_Multiisolate.
        """
        found = []
        for o in self.all_options:
            if o == query:
                found.append(o)
            if query.startswith('*'):
                if o.endswith(query[1:]):
                    found.append(o)
            if query.endswith('*'):
                if o.startswith(query[:-1]):
                    found.append(o)
        return found

    def select_options(self, filter_name, options):
        """
        Remove unused filters

        :param filter_name: filter name
        :param filter_values: list of filter options values
        """

        result = []

        for option_name, option_value in options.iteritems():
            if isinstance(option_value, OrderedDict):
                sub_result = self.select_options(filter_name, option_value)
                if not sub_result:
                    continue
                result.append((option_name, OrderedDict(sub_result)))
            else:
                # check is option was used
                used = False
                for o in option_value.split(' OR '):
                    found = self.check_in_all_options(o)
                    if found:
                        used = True
                        for f in found:
                            if f not in self.used_options:
                                self.used_options.append(f)
                # options with name.startswith('INVISIBLE') will be not included in result
                if used and not option_name.startswith('INVISIBLE'):
                    result.append((option_name, option_value))
        return result

    def find_all_options(self, filter_name):
        self.all_options = self._all_options(filter_name=filter_name)

    def _all_options(self, filter_name, start=''):
        options = []
        for c in self.CHARACTERS:
            if not start and c in ('-', '+'):
                continue
            query = {filter_name: '%s%s*' % (start, c)}
            api_request = RequestDetail(
                    query=query, limit=5, sort_by=filter_name)
            try:
                result = api_request.call().next()
            except StopIteration:
                continue
            if api_request.hits:
                api_request = RequestDetail(
                        query=query, limit=5, sort_by='-%s' % filter_name)
                result2 = api_request.call().next()
                if result.get(filter_name) == result2.get(filter_name):
                    options.append(result.get(filter_name))
                else:
                    # if option is exact
                    api_request = RequestID(
                            query={filter_name: '%s%s' % (start, c)},
                            limit=5)
                    try:
                        api_request.call().next()
                        options.append(result.get(filter_name))
                    except StopIteration:
                        pass
                    # if some other filters which starts from start+c exists
                    for f in self._all_options(
                            filter_name=filter_name,
                            start='%s%s' % (start, c)):
                        if f not in options:
                            options.append(f)
        return options

class Command(BaseCommand):
    """
    Verbosity levels (manage.py --verbosity 0):
    0: print nothing (only errors)
    1 or greater: print basic information
    2 or greater: print as much information as possible (typically for debugging)
    """

    help = 'Process filters from settings/filters.py. Removes unused options for filters.'

    def handle(self, *args, **options):
        verbosity = int(options['verbosity'])

        processor = FiltersProcessor(
                stdout=self.stdout,
                stderr=self.stderr,
                verbosity=verbosity)

        for filter_name, filter_data in ALL_FILTERS.iteritems():
            if verbosity > 0:
                self.stderr.write('Processing %s filter\n' % filter_name)
            if filter_name in DATE_ATTRIBUTES:
                continue
            options = processor.process(
                    filter_name=filter_name,
                    options=filter_data['filters'],
                    select_options=filter_data.get('selectOptions', True))
            filter_data['filters'] = options

        # write filters found to filters_storage.json
        with open(JSON_FILTERS_FILE_NAME, 'w') as f:
            json.dump([DATE_FILTERS_HTML_IDS, ALL_FILTERS], f, indent=2)
        if verbosity > 0:
            self.stderr.write('\nWrote to %s.\n' % JSON_FILTERS_FILE_NAME)
