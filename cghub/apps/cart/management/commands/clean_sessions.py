from django.core.management.base import BaseCommand, CommandError

from django.contrib.sessions.models import Session

from ...models import Analysis


class Command(BaseCommand):
    help = 'Removes user session data, including carts.'

    def handle(self, *args, **options):
        self.stderr.write('Removing sessions ...\n')
        Session.objects.all().delete()
        self.stderr.write('Removing analysises ...\n')
        Analysis.objects.all().delete()
        self.stderr.write('Done\n')
