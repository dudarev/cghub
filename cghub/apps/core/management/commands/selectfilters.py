try:
    from collections import OrderedDict
except ImportError:
    from celery.utils.compat import OrderedDict

from django.core.management.base import BaseCommand

from cghub.apps.core.filters_storage_full import ALL_FILTERS


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

    def handle(self, *args, **options):
        self.stdout.write('Checking filters\n')
        for k in ALL_FILTERS:
            self.stdout.write(k)
            self.stdout.write('\n')
            for f in ALL_FILTERS[k]['filters']:
                self.stdout.write('  %s' % f)
                self.stdout.write('\n')
        self.stdout.write(str(ALL_FILTERS))
        print format_dict(ALL_FILTERS)
        filters_storage = open('cghub/apps/core/filters_storage_full.py', 'r').read()
        all_filters_index = filters_storage.index('ALL_FILTERS')
        filters_storage = ''.join([
            filters_storage[:all_filters_index],
            'ALL_FILTERS = ',
            format_dict(ALL_FILTERS),
        ])
        f = open('cghub/apps/core/filters_storage_short.py', 'w')
        f.write(filters_storage)
        f.close()
        self.stdout.write('File cghub/apps/core/filters_storage_short.py is created\n')
