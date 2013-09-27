import logging

from django.core.management.base import BaseCommand, CommandError

from django.contrib.sessions.models import Session

from ...models import Analysis


cart_logger = logging.getLogger('cart')


class Command(BaseCommand):
    help = 'Updates full-metadata cache.'

    def handle(self, *args, **options):
        self.stderr.write('Removing sessions ...\n')
        Session.objects.all().delete()
        self.stderr.write('Removing analysises ...\n')
        Analysis.objects.all().delete()
        self.stderr.write('Done\n')
