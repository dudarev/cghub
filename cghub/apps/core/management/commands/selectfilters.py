from django.core.management.base import BaseCommand

from cghub.apps.core.filters_storage import ALL_FILTERS

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
