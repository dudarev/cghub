import logging
import multiprocessing

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from cghub.apps.core.requests import RequestMinimal, RequestID

from ...cache import is_cart_cache_exists, save_to_cart_cache
from ...models import Analysis
from ...utils import update_analysis


cart_logger = logging.getLogger('cart')



def update_cache(analysis_id, last_modified):
    try:
        save_to_cart_cache(
                analysis_id=analysis_id,
                last_modified=last_modified)
    except Exception as e:
        return u'- %s: Error: %s\n' % (analysis_id, unicode(e))
    return u'- %s: Done\n' % analysis_id


class Command(BaseCommand):
    help = 'Updates full-metadata cache.'

    def process_tasks(self):
        results = [self.pool.apply_async(update_cache, t) for t in self.tasks]
        for result in results:
            output = result.get()
            self.stderr.write(output)
            if output and output.find('Error') == -1:
                self.done_count += 1
            else:
                self.error_count += 1
                cart_logger.error(output)
        self.tasks = []

    def handle(self, *args, **options):
        self.stdout.write('Searching for outdated analysises ...\n')
        self.stderr.write('Searching for outdated analysises ...\n')

        api_request = RequestMinimal(query={})
        for result in api_request.call():
            try:
                analysis = Analysis.objects.get(
                        analysis_id=result['analysis_id'],
                        last_modified=result['last_modified'])
                if analysis.last_modified != result['last_modified']:
                    analysis = update_analysis(result)
                    if analysis:
                        self.stderr.write('- %s was updated\n' % result['analysis_id'])
                    else:
                        self.stderr.write('- %s was skipped\n' % result['analysis_id'])
            except Analysis.DoesNotExist:
                analysis = update_analysis(result)
                if analysis:
                    self.stderr.write('- %s was created\n' % result['analysis_id'])
                else:
                    self.stderr.write('- %s was skipped\n' % result['analysis_id'])

        self.stderr.write('Downloading not existent cache ...\n')
        self.done_count = 0
        self.error_count = 0

        PROCESSES = getattr(settings, 'MULTIPROCESSING_CORES', None)
        if not PROCESSES:
            PROCESSES = int(multiprocessing.cpu_count() / 2) or 1

        self.pool = multiprocessing.Pool(PROCESSES)
        self.tasks = []

        for analysis in Analysis.objects.all():
            if not is_cart_cache_exists(
                    analysis_id=analysis.analysis_id,
                    last_modified=analysis.last_modified):
                self.tasks.append((
                        analysis.analysis_id,
                        analysis.last_modified))
                if len(self.tasks) >= PROCESSES * 5:
                    self.process_tasks()
        if len(self.tasks):
            self.process_tasks()

        self.stdout.write(
                '---\n%d cache files were updated.\n' % self.done_count)
        self.stderr.write(
                '---\n%d cache files were updated.\n' % self.done_count)
        if self.error_count:
            raise CommandError(
                    '%d errors occurred. You can find them in the logs.\n' % self.error_count)
