from django.core.management.base import BaseCommand

from cghub.apps.core.utils import RequestDetail

from ...models import Analysis
from ...cache import is_cart_cache_exists, save_to_cart_cache


class Command(BaseCommand):
    help = 'Updates cghub browser cart xml cache.'

    def handle(self, *args, **options):
        self.stdout.write('Searching for outdated analysises ...\n')

        api_request = RequestDetail(query={})
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
            if not is_cart_cache_exists(
                    analysis_id=analysis.analysis_id,
                    last_modified=analysis.last_modified):
                self.stdout.write('- Downloading cache for %s\n' % analysis.analysis_id)
                save_to_cart_cache(
                        analysis_id=analysis.analysis_id,
                        last_modified=analysis.last_modified)
                counter += 1
        self.stdout.write('---\nDone! %d cache files were updated.\n' % counter)