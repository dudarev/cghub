import os
os.environ['DJANGO_SETTINGS_MODULE'] = "devtools.profile_settings"

import sys
import shutil
import datetime
import time

from cProfile import runctx
from StringIO import StringIO

from django.test.client import RequestFactory
from django.core.management import call_command

from cghub.apps.cart.utils import Cart, metadata, manifest, summary
from cghub.apps.cart.models import Analysis, Cart as CartModel
from cghub.apps.core.tests.tests import get_request
from cghub.apps.core.requests import RequestMinimal

from devtools.profile_settings import DATABASES, FULL_METADATA_CACHE_DIR


IDS = [
    'ef4fcd50-9575-4592-a4b1-733ffa95a963', '69631dfb-d2c8-4f2e-87e9-8e608291acb2',
    'abcf64f4-8dcc-4584-9095-c8f35851cf27', '70be5538-6d77-405c-95aa-6aaadfd9713a',
    '0cc1bf21-52e7-4bfe-b3df-09997814cb63', 'f06ee4c3-2143-4ef9-99f6-159f340626ca',
    '219e6fb6-846c-4229-9cdf-23b49d03ea9d', '67f2241f-c04a-48d8-9740-259652110400',
    'ec7c4686-10aa-471a-a207-967204e3b063', 'e3cd3123-c38a-4401-967a-5510c2b1bb94',
    '036d881f-4bbd-4a60-a409-323f5ac2caf7', 'd64013c7-d80d-4ee3-80d8-ee80250c40b5',
    'c6ea03ae-12eb-4d24-ab04-6670d28806f8', '6b87c9a3-1575-4426-866a-e2e8538d1d05',
    'f5b93357-9f1e-4673-812b-51e58f69cfea', 'd3af2a3a-af31-450e-b3c8-dfc82f4b9d89',
    'e901e923-4741-40d6-afbe-be8a41deee4e', '85ce2c9b-6ead-4797-a548-a494e4b0703c',
    '162c718c-b21a-4f49-bd91-933b9af36767', '26da50ca-b9d9-49d6-a8d5-89c3792d3882',
    'cab6a37b-9ebf-4eb5-bb5b-57a2c082f4ee', '788f2494-7466-42aa-9fcd-8ea6ec718268',
    '7547b5d8-ee5f-4b64-9372-deaf90ea2a5b', 'c56ebc51-fc57-4cab-9138-e95b37cbcb4e',
    'bb37f714-d137-49ef-897c-9013499a571a']

RUN_COUNT = 5


def remove_database():
    path = DATABASES['default']['NAME']
    if os.path.exists(path):
        os.remove(path)


def create_database():
    remove_database()
    stdout = sys.stdout
    sys.stdout = StringIO()
    call_command('syncdb', interactive=False)
    call_command('migrate')
    sys.stdout = stdout


def empty_database():
    CartModel.objects.all().delete()
    Analysis.objects.all().delete()


def empty_cache():
    if os.path.exists(FULL_METADATA_CACHE_DIR):
        shutil.rmtree(FULL_METADATA_CACHE_DIR)


def run_view(view, request):
    unicode(view(request))


def profile_view(view):
    empty_database()
    empty_cache()
    time.sleep(5)
    request = get_request()
    cart = Cart(request.session)
    # fill cart
    api_request = RequestMinimal(query={'analysis_id': IDS})
    for result in api_request.call():
        cart.add(result)
    cart.update_stats()
    # Call view RUN_COUNT times
    for i in range(RUN_COUNT):
        print 'Run #%d ...' % (i + 1)
        runctx('run_view(view, request)',
                {'run_view': run_view},
                {'view': view, 'request': request})
    print 'done'


def profile():
    print 'Creating database ...',
    create_database()
    print 'done'
    print 'Profiling metadata view ...'
    profile_view(metadata)
    print 'Profiling manifest view ...'
    profile_view(manifest)
    print 'Profiling summary view ...'
    profile_view(summary)
    empty_cache()
    remove_database()

if __name__ == '__main__':
    profile()
