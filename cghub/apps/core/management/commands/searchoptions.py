from .selectoptions import FiltersProcessor

from django.core.management.base import BaseCommand, CommandError

from cghub.apps.core.attributes import DATE_ATTRIBUTES
from cghub.settings.filters import ALL_FILTERS


class Command(BaseCommand):
    """
    Verbosity levels (manage.py --verbosity 0):
    0: print nothing (only errors)
    1 or greater: print basic information
    2 or greater: print as much information as possible (typically for debugging)
    """

    help = 'Search for missing options for filters from settings/filters.py.'

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
            if filter_data.get('searchForNewOptions', False):
                processor.find_new_options(
                        filter_name=filter_name,
                        options=filter_data['filters'])

        if processor.new_options_count:
            # non zero exit code
            raise CommandError('%d new options were found.' % processor.new_options_count)
