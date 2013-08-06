import string

try:
    from collections import OrderedDict
except ImportError:
    from celery.utils.compat import OrderedDict

from django.core.management.base import BaseCommand
from django.utils import simplejson as json

from cghub.apps.core.filters_storage_full import ALL_FILTERS, DATE_FILTERS_HTML_IDS
from cghub.apps.core.filters_storage import JSON_FILTERS_FILE_NAME
from cghub.apps.core.utils import RequestDetail, RequestIDs


CHARACTERS = string.ascii_uppercase + '0123456789' + string.ascii_lowercase


def get_all_filters(stdout, key, start='', count_all=None):
    filters = []
    count = 0
    for c in CHARACTERS:
        query = {key: '%s%s*' % (start, c)}
        stdout.write('Searching [%s]' % query)
        api_request = RequestDetail(query=query, limit=5, sort_by=key)
        stdout.write('- Found %d\n' % result.hits)
        try:
            result = api_request.call().next()
        except StopIteration:
            pass
        count += api_request.hits
        if api_request.hits:
            filters.append(getattr(result, key))
            if count_all and count_all == count:
                return filters
            api_request = RequestDetail(query=query, limit=5, sort_by='-%s' % key)
            try:
                result = api_request.call().next()
            except StopIteration:
                result = None
            # if some other filters which starts from start+c exists
            if result and getattr(result, key) not in filters:
                for f in get_all_filters(
                            stdout=stdout, key=key,
                            start='%s%s' % (start, c),
                            count_all=api_request.hits):
                    if f not in filters:
                        filters.append(f)
    return filters


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
            api_request = RequestIDs(query={key: '*'}, limit=5)
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

            for filter in ALL_FILTERS[key]['filters']:
                self.stdout.write('- Filter %s ... ' % filter)
                api_request = RequestIDs(query={key: filter}, limit=5)
                try:
                    result = api_request.call().next()
                except StopIteration:
                    pass
                count += api_request.hits
                if api_request.hits:
                    self.stdout.write('added\n')
                    used_filters[key].append(filter)
                else:
                    self.stdout.write('removed\n')
                    unused_filters[key].append(filter)
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
            for filter in unused_filters[key]:
                del ALL_FILTERS[key]['filters'][filter]
                self.stdout.write('- Removed %s:%s\n' % (key, filter))

        # add new filters that are not present in filters_storage_full.py
        self.stdout.write('Adding new filters ...\n')
        for key in ALL_FILTERS:
            if not ALL_FILTERS[key].get('selectFilter', True):
                continue
            for filter in new_filters[key]:
                ALL_FILTERS[key]['filters'][filter] = filter
                self.stdout.write('- Added new filter %s:%s\n' % (key, filter))
                self.stdout.write('! Please add this filter to filters_storage_full.py')
            # sorting by key
            ALL_FILTERS[key]['filters'] = OrderedDict(
                            sorted(ALL_FILTERS[key]['filters'].items()))

        # write filters found to filters_storage.json
        json_filters = open(JSON_FILTERS_FILE_NAME, 'w')
        json.dump([DATE_FILTERS_HTML_IDS, ALL_FILTERS], json_filters, indent=2)
        json_filters.close()
        self.stdout.write('\nWrote to %s.\n' % JSON_FILTERS_FILE_NAME)
