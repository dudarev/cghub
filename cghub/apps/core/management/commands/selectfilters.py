import string

try:
    from collections import OrderedDict
except ImportError:
    from celery.utils.compat import OrderedDict

from django.core.management.base import BaseCommand
from django.utils import simplejson as json

from cghub.apps.core.filters_storage_full import ALL_FILTERS, DATE_FILTERS_HTML_IDS
from cghub.apps.core.filters_storage import JSON_FILTERS_FILE_NAME
from cghub.apps.core.utils import get_wsapi_settings, WSAPIRequest


CHARACTERS = string.ascii_uppercase + '0123456789' + string.ascii_lowercase
WSAPI_SETTINGS = get_wsapi_settings()


def get_all_filters(key, start='', count_all=None):
    filters = []
    count = 0
    for c in CHARACTERS:
        query = '%s=%s%s*' % (key, start, c)
        print 'Searching [%s]' % query
        result = WSAPIRequest(
                query=query, limit=5, sort_by=key, settings=WSAPI_SETTINGS)
        print '- Found %d' % result.hits
        count += result.hits
        if result.hits:
            filters.append(result.results[0][key])
            if count_all and count_all == count:
                return filters
            result = WSAPIRequest(
                    query=query, limit=5, sort_by='-%s' % key,
                    settings=WSAPI_SETTINGS)
            # if some other filters which starts from start+c exists
            if result.results[0][key] not in filters:
                for f in get_all_filters(
                            key=key, start='%s%s' % (start, c),
                            count_all=result.hits):
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
            result = WSAPIRequest(
                    query='%s=*' % key, limit=5, only_ids=True,
                    settings=WSAPI_SETTINGS)
            count_all = result.hits

            self.stdout.write('Checking %s filters\n' % key)

            used_filters[key] = []
            unused_filters[key] = []
            new_filters[key] = []
            count = 0

            for filter in ALL_FILTERS[key]['filters']:
                self.stdout.write('- Filter %s ... ' % filter)
                result = WSAPIRequest(
                            query='%s=%s' % (key, filter), limit=5,
                            only_ids=True, settings=WSAPI_SETTINGS)
                count += result.hits
                if result.hits:
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
                        set(get_all_filters(key, count_all=count_all)) -
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
