import logging

from django.core.management.base import BaseCommand

from cghub.apps.core.requests import RequestMinimal, RequestID

from ...models import Analysis
from ...cache import is_cart_cache_exists, save_to_cart_cache


cart_logger = logging.getLogger('cart')


class Command(BaseCommand):
    help = 'Updates cghub browser cart xml cache.'

    def handle(self, *args, **options):
        self.stdout.write('Searching for outdated analysises ...\n')

        api_request = RequestMinimal(query={}, limit=100)
        for result in api_request.call():
            analysis, created = Analysis.objects.get_or_create(
                    analysis_id=result['analysis_id'],
                    defaults={
                        'last_modified': result['last_modified'],
                        'state': result['state'],
                        'files_size': result['files_size']
                    })
            if created:
                self.stdout.write('- %s was created\n' % analysis.analysis_id)
            elif analysis.last_modified != result['last_modified']:
                analysis.last_modified = result['last_modified']
                analysis.state = result['state']
                analysis.files_size = result['files_size']
                analysis.save()
                self.stdout.write('- %s was updated\n' % analysis.analysis_id)

        self.stdout.write('Downloading not existent cache ...\n')
        counter = 0
        for analysis in Analysis.objects.all():
            try:
                if not is_cart_cache_exists(
                        analysis_id=analysis.analysis_id,
                        last_modified=analysis.last_modified):
                    self.stdout.write('- Downloading cache for %s\n' % analysis.analysis_id)
                    save_to_cart_cache(
                            analysis_id=analysis.analysis_id,
                            last_modified=analysis.last_modified)
                    counter += 1
            except UnicodeEncodeError as e:
                self.stdout.write(u'- %s error: %s\n' % (
                        analysis.analysis_id,
                        unicode(e)))
                cart_logger.error(u'%s error: %s' % (
                        analysis.analysis_id,
                        unicode(e)))
        self.stdout.write('---\nDone! %d cache files were updated.\n' % counter)
