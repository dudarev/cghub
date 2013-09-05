import os
import shutil
import codecs

from mock import patch
from StringIO import StringIO

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.utils import timezone, simplejson as json
from django.conf import settings
from django.contrib.sessions.models import Session

from cghub.apps.core import browser_text_search
from cghub.apps.core.tests import create_session, get_request

from ..utils import (
                    manifest, metadata, summary, Cart,
                    analysis_xml_iterator, summary_tsv_iterator)
from ..forms import SelectedItemsForm, AllItemsForm
from ..cache import (
                    AnalysisException, get_cart_cache_file_path,
                    save_to_cart_cache, get_analysis_path, get_analysis,
                    get_analysis_xml, is_cart_cache_exists)
from ..models import Cart as CartModel, CartItem, Analysis
from .factories import AnalysisFactory, CartItemFactory


class CartModelsTestCase(TestCase):

    def test_cart_creation(self):
        # cart created on session creation
        self.assertFalse(CartModel.objects.exists())
        self.assertFalse(Session.objects.exists())
        create_session(self)
        session = Session.objects.get(
                session_key=self.client.session.session_key)
        cart = session.cart
        self.assertTrue(cart)
        # add some items to cart
        analysis = Analysis.objects.create(
                analysis_id='017a4d4e-9f4b-4904-824e-060fde3ca223',
                last_modified='2013-05-16T20:43:40Z',
                state='live',
                files_size=4666849442)
        CartItem.objects.create(
                cart=cart,
                analysis=analysis)
        analysis = Analysis.objects.create(
                analysis_id='016b792f-e659-4143-b833-163141e21363',
                last_modified='2013-05-16T20:43:40Z',
                files_size=388596051,
                state='live')
        CartItem.objects.create(
                cart=cart,
                analysis=analysis)
        self.assertEqual(cart.items.count(), 2)
        self.assertEqual(CartItem.objects.count(), 2)
        self.assertTrue(cart.items.filter(
                analysis__files_size=4666849442).exists())
        # cart remove on sesion remove
        session.delete()
        self.assertFalse(Session.objects.filter(
                session_key=self.client.session.session_key).exists())
        self.assertFalse(CartModel.objects.filter(id=cart.id).exists())
        self.assertEqual(CartItem.objects.count(), 0)


class CartUtilsTestCase(TestCase):

    def test_cart_class(self):
        create_session(self)
        session = Session.objects.get(
                session_key=self.client.session.session_key)
        cart = session.cart
        my_cart = Cart(self.client.session)
        self.assertEqual(cart.items.count(), 0)
        # Analysises already created
        analysis1 = AnalysisFactory.create()
        analysis2 = AnalysisFactory.create()
        analysis1_result = {
                'analysis_id': analysis1.analysis_id,
                'last_modified': analysis1.last_modified}
        analysis2_result = {
                'analysis_id': analysis2.analysis_id,
                'last_modified': analysis2.last_modified}
        my_cart.add(analysis1_result)
        my_cart.add(analysis2_result)
        self.assertEqual(cart.items.count(), 2)
        # remove
        my_cart.remove(analysis2.analysis_id)
        self.assertEqual(cart.items.count(), 1)
        # check update_stats
        analysis3 = AnalysisFactory.create(state='somestate')
        analysis3_result = {
                'analysis_id': analysis3.analysis_id,
                'last_modified': analysis3.last_modified}
        my_cart.add(analysis3_result)
        self.assertEqual(my_cart.size, 0)
        my_cart.update_stats()
        self.assertEqual(
                my_cart.size,
                analysis1.files_size + analysis3.files_size)
        self.assertEqual(my_cart.all_count, 2)
        self.assertEqual(my_cart.live_count, 1)
        # Analysis id not exist
        result = {
                'analysis_id': '01810b1a-84e4-43d5-8a1e-42b132a1126f',
                'last_modified': '2012-05-16T20:43:41Z',
                'state': 'live',
                'files_size': 12345}
        my_cart.add(result)
        # Analysis was modified
        result = {
                'analysis_id': analysis1.analysis_id,
                'last_modified': '3000-01-01T11:11:11Z',
                'state': 'bad',
                'files_size': 54321}
        self.assertNotEqual(analysis1.last_modified, result['last_modified'])
        self.assertNotEqual(analysis1.state, result['state'])
        self.assertNotEqual(analysis1.files_size, result['files_size'])
        my_cart.add(result)
        analysis1 = Analysis.objects.get(analysis_id=analysis1.analysis_id)
        self.assertEqual(analysis1.last_modified, result['last_modified'])
        self.assertEqual(analysis1.state, result['state'])
        self.assertEqual(analysis1.files_size, result['files_size'])

    def test_clear_cart(self):
        create_session(self)
        cart = Cart(session=self.client.session)
        CartItemFactory.create(cart=cart.cart)
        CartItemFactory.create(cart=cart.cart)
        cart.update_stats()
        self.assertEqual(cart.live_count, 2)
        self.assertEqual(cart.all_count, 2)
        cart.clear()
        self.assertEqual(cart.all_count, 0)
        self.assertEqual(cart.live_count, 0)

    def test_cart_page(self):
        create_session(self)
        cart = Cart(session=self.client.session)
        cart_item1 = CartItemFactory.create(cart=cart.cart)
        cart_item2 = CartItemFactory.create(cart=cart.cart)
        analysis = cart_item1.analysis
        analysis.last_modified = '2000-01-01T01:01:01Z'
        analysis.save()
        page = cart.page()
        self.assertEqual(len(page), 2)
        self.assertTrue(
                ((cart_item1.analysis.analysis_id == page[0]['analysis_id']) and
                (cart_item2.analysis.analysis_id == page[1]['analysis_id'])) or
                ((cart_item1.analysis.analysis_id == page[1]['analysis_id']) and
                (cart_item2.analysis.analysis_id == page[0]['analysis_id'])))
        self.assertIn('platform', page[0])
        self.assertIn('refassem_short_name', page[0])
        # check is last_modified is the same as in Result
        self.assertNotEqual(analysis.last_modified, page[0]['last_modified'])
        # test sorting
        page1 = cart.page(sort_by='analysis_id')
        page2 = cart.page(sort_by='-analysis_id')
        self.assertEqual(page1[0], page2[1])
        self.assertEqual(page1[1], page2[0])


class CartTestCase(TestCase):
    RANDOM_IDS = [
            {
                'analysis_id': '017a4d4e-9f4b-4904-824e-060fde3ca223',
                'state': 'live',
                'last_modified': '2013-05-16T20:43:40Z',
                'files_size': 12345
            }, {
                'analysis_id': '016b792f-e659-4143-b833-163141e21363',
                'state': 'live',
                'last_modified': '2013-05-16T20:43:40Z',
                'files_size': 12346
            }, {
                'analysis_id': '01810b1a-84e4-43d5-8a1e-42b132a1126f',
                'state': 'live',
                'last_modified': '2013-05-16T20:43:40Z',
                'files_size': 12347
            }]

    def setUp(self):
        self.cart_page_url = reverse('cart_page')

    def test_cart_add_files(self):
        url = reverse('cart_add_remove_files', args=['add'])

        self.client.post(
                        url, {'selected_items': json.dumps(self.RANDOM_IDS)},
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.assertEqual(response.status_code, 200)

        # make sure counter in header is OK
        self.assertContains(response, 'Cart (3)')
        self.assertContains(response, 'Files in your cart: 3')

        # make sure we have 3 files in cart
        self.assertEqual(len(response.context['results']), 3)

        # make sure we have files we've posted
        for f in self.RANDOM_IDS:
            self.assertIn(f['analysis_id'], response.content)

    def test_cart_remove_files(self):
        # add files
        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(
                        url, {'selected_items': json.dumps(self.RANDOM_IDS)},
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # remove files
        rm_selected_files = [
                self.RANDOM_IDS[0]['analysis_id'],
                self.RANDOM_IDS[1]['analysis_id']]
        url = reverse('cart_add_remove_files', args=['remove'])
        self.client.post(
                        url, {'ids': ' '.join(rm_selected_files)},
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.assertEqual(len(response.context['results']), 1)

        # make sure counter in header is OK
        self.assertContains(response, 'Cart (1)')
        self.assertContains(response, 'Files in your cart: 1')

        # make sure we do not have removed files in cart
        for f in rm_selected_files:
            self.assertEqual(f in response.content, False)

    def test_cart_pagination(self):
        # add 3 files to cart
        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(
                        url, {'selected_items': json.dumps(self.RANDOM_IDS)},
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Items per page:')

        # 2 items per page
        response = self.client.get(reverse('cart_page') +
                                   '?offset={offset}&limit={limit}'.format(
                                       offset=0, limit=2))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1')
        self.assertContains(response, '2')
        self.assertContains(response, 'Prev')
        self.assertContains(response, 'Next')
        self.assertContains(response, 'Items per page:')

        # 2 items per page, 2nd page
        response = self.client.get(reverse('cart_page') +
                                   '?offset={offset}&limit={limit}'.format(
                                       offset=2, limit=2))
        self.assertEqual(response.status_code, 200)
        # test limit saved to cookies
        self.assertEqual(
            response.cookies[settings.PAGINATOR_LIMIT_COOKIE].value, '2')

    def test_cart_sorting(self):
        # add 3 files to cart
        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(
                        url, {'selected_items': json.dumps(self.RANDOM_IDS)},
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.assertEqual(response.status_code, 200)
        # check sort by analysis_id
        for attr in ('analysis_id',):
            val1 = str(self.RANDOM_IDS[0][attr])
            val2 = str(self.RANDOM_IDS[1][attr])
            response = self.client.get(
                    self.cart_page_url,
                    {'sort_by': attr})
            self.assertEqual(response.status_code, 200)
            result1 = response.content.find(val1) > response.content.find(val2)
            response = self.client.get(
                    self.cart_page_url,
                    {'sort_by': '-%s' % attr})
            self.assertEqual(response.status_code, 200)
            result2 = response.content.find(val1) > response.content.find(val2)
            self.assertNotEqual(result1, result2)

    def test_cart_add_raise_http_404_when_get(self):
        """
        Only POST method allowed for 'cart_add_remove_files' url
        """
        url = reverse('cart_add_remove_files', args=['add'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class CartAddItemsTestCase(TestCase):

    def test_cart_add_files_with_q(self):
        oldUseAllMetadataIndex = browser_text_search.useAllMetadataIndex
        browser_text_search.useAllMetadataIndex = True
        create_session(self)
        data = {
            'filters': json.dumps({
                        'state': '(live)',
                        'q': '(00b27c0f-acf5-434c-8efa-25b1f3c4f506)'
                    })}
        url = reverse('cart_add_remove_files', args=('add',))
        response = self.client.post(
                url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['action'], 'redirect')
        cart_model = CartModel.objects.get(
                session__session_key=self.client.session.session_key)
        self.assertTrue(cart_model.items.filter(
                analysis__analysis_id='00b27c0f-acf5-434c-8efa-25b1f3c4f506')
                .exists())
        browser_text_search.useAllMetadataIndex = oldUseAllMetadataIndex

    def test_cart_add_files_with_q_without_metadata_index(self):
        """
        with  cghub.wsapi.browser_text_search.useAllMetadataIndex = False
        """
        oldUseAllMetadataIndex = browser_text_search.useAllMetadataIndex
        browser_text_search.useAllMetadataIndex = False
        create_session(self)
        data = {
            'filters': json.dumps({
                    'state': '(live)',
                    'q': '00b27c0f-acf5-434c-8efa-25b1f3c4f506'
                })}
        url = reverse('cart_add_remove_files', args=('add',))
        response = self.client.post(
                url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['action'], 'redirect')
        cart_model = CartModel.objects.get(
                session__session_key=self.client.session.session_key)
        self.assertTrue(cart_model.items.filter(
                analysis__analysis_id='00b27c0f-acf5-434c-8efa-25b1f3c4f506')
                .exists())
        browser_text_search.useAllMetadataIndex = oldUseAllMetadataIndex

    def test_cart_add_files_without_q(self):
        create_session(self)
        data = {
            'filters': json.dumps({
                        'state': '(live)',
                        'upload_date': '[NOW-1DAY TO NOW]',
                        'study': '(*Other_Sequencing_Multiisolate)'
                    })}
        url = reverse('cart_add_remove_files', args=('add',))
        response = self.client.post(
                url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['action'], 'redirect')
        self.assertTrue(CartModel.objects.filter(
                session__session_key=self.client.session.session_key).exists())


class CartCacheTestCase(TestCase):

    """
    Cached files will be used
    04578995-3609-4f09-bc12-7100a04ebc92 - 2013-06-03T20:58:55Z
    549571a3-98a7-4601-adb1-6951d770cc0e - 2013-06-03T20:59:49Z
    """
    analysis_id = '04578995-3609-4f09-bc12-7100a04ebc92'
    last_modified = '2013-06-03T20:58:55Z'
    analysis_id2 = '549571a3-98a7-4601-adb1-6951d770cc0e'
    last_modified2 = '2013-06-03T20:59:49Z'
    DATA_SET = {
            analysis_id: {
                    'analysis_id': analysis_id,
                    'last_modified': last_modified,
                    'state': 'live',
                    'files_size': 12345},
            analysis_id2: {
                    'analysis_id': analysis_id2,
                    'last_modified': last_modified2,
                    'state': 'live',
                    'files_size': 12345}}

    def test_get_cache_file_path(self):
        self.assertEqual(
                get_cart_cache_file_path(
                        '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1',
                        '2012-10-29T21:56:12Z'),
                os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        '7b/9c/7b9cd36a-8cbb-4e25-9c08-d62099c15ba1/2012-10-29T21:56:12Z/analysis.xml'))

    def test_save_to_cart_cache(self):
        path = os.path.join(
                            settings.FULL_METADATA_CACHE_DIR,
                            self.analysis_id[:2],
                            self.analysis_id[2:4],
                            self.analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        path_file = get_cart_cache_file_path(self.analysis_id, self.last_modified)
        # check is_cart_cache_exists
        self.assertFalse(is_cart_cache_exists(self.analysis_id, self.last_modified))
        result = save_to_cart_cache(self.analysis_id, self.last_modified)
        self.assertTrue(os.path.exists(path_file))
        self.assertTrue(is_cart_cache_exists(self.analysis_id, self.last_modified))
        shutil.rmtree(path)
        # check exception raises when file does not exists
        bad_analysis_id = 'badanalysisid'
        path = os.path.join(
                    settings.FULL_METADATA_CACHE_DIR,
                    bad_analysis_id[:2],
                    bad_analysis_id[2:4],
                    bad_analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        try:
            save_to_cart_cache(bad_analysis_id, self.last_modified)
        except AnalysisException as e:
            self.assertEqual(unicode(e), 'Analysis for analysis_id=badanalysisid '
            'that was last modified %s. '
            'Analysis with specified analysis_id does not exists' % self.last_modified)
        else:
            raise False, 'AnalysisException doesn\'t raised'
        if os.path.isdir(path):
            shutil.rmtree(path)
        # check case when file was updated
        path = os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        self.analysis_id[:2],
                        self.analysis_id[2:4],
                        self.analysis_id)
        try:
            save_to_cart_cache(self.analysis_id, '1900-10-29T21:56:12Z')
        except AnalysisException:
            assert False, 'Most recent file was not downloaded'
        if os.path.isdir(path):
            shutil.rmtree(path)
        # check access denied to files outside cache dir
        try:
            save_to_cart_cache(self.analysis_id, '../../same_outside_dir')
        except AnalysisException as e:
            self.assertEqual(
                unicode(e),
                'Analysis for analysis_id=%s '
                'that was last modified ../../same_outside_dir. '
                'Bad analysis_id or last_modified' % self.analysis_id)
        else:
            raise False, 'AnalysisException doesn\'t raised'

    def test_get_analysis(self):
        # test get_analysis_path
        path = os.path.join(
                            settings.FULL_METADATA_CACHE_DIR,
                            self.analysis_id[:2],
                            self.analysis_id[2:4],
                            self.analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        analysis_path = get_analysis_path(self.analysis_id, self.last_modified)
        self.assertEqual(
            analysis_path,
            get_cart_cache_file_path(self.analysis_id, self.last_modified))
        self.assertTrue(os.path.exists(analysis_path))
        # now using cache
        analysis_path = get_analysis_path(self.analysis_id, self.last_modified)
        self.assertEqual(
            analysis_path,
            get_cart_cache_file_path(self.analysis_id, self.last_modified))
        # test get_analysis
        # with cache
        analysis = get_analysis(self.analysis_id, self.last_modified)
        self.assertIn('analysis_xml', analysis['xml'])

    def test_get_analysis_xml(self):
        xml, files_size = get_analysis_xml(
            analysis_id=self.analysis_id,
            last_modified=self.last_modified)
        self.assertNotIn('Result', xml)
        self.assertIn('analysis_id', xml)
        self.assertIn('analysis_xml', xml)
        self.assertTrue(files_size)
        # short
        xml, files_size = get_analysis_xml(
            analysis_id=self.analysis_id,
            last_modified=self.last_modified, short=True)
        self.assertNotIn('Result', xml)
        self.assertNotIn('<doc>', xml)
        self.assertIn('analysis_id', xml)
        self.assertNotIn('analysis_xml', xml)
        self.assertNotIn('experiment_xml', xml)

    def test_iterators(self):
        request = get_request()
        cart = Cart(session=request.session)
        analysis = AnalysisFactory.create(
                analysis_id=self.analysis_id,
                last_modified=self.last_modified)
        CartItemFactory.create(
                cart=cart.cart,
                analysis=analysis)
        analysis = AnalysisFactory.create(
                analysis_id=self.analysis_id2,
                last_modified=self.last_modified2)
        CartItemFactory.create(
                cart=cart.cart,
                analysis=analysis)

        # summary tsv iterator
        iterator = summary_tsv_iterator(request)
        result = ''
        for i in iterator:
            result += i
        self.assertIn('center', result)
        self.assertIn('analysis_id', result)
        self.assertIn(self.last_modified[:10], result)
        self.assertIn(self.analysis_id, result)
        self.assertIn(self.analysis_id2, result)
        self.assertNotIn('Error!', result)

        # analysis_xml iterator
        iterator = analysis_xml_iterator(request)
        result = ''
        for i in iterator:
            result += i
        self.assertIn('ResultSet', result)
        self.assertIn('Result id="1"', result)
        self.assertIn('Result id="2"', result)
        self.assertNotIn('Error!', result)

        # test error when some analysis was not found

        self.assertEqual(cart.cart.items.count(), 2)
        # add one bad analysis_id
        analysis = cart.cart.items.all()[1].analysis
        analysis.analysis_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        analysis.save()

        self.assertNotIn('messages', request.session)

        # summary tsv iterator
        iterator = summary_tsv_iterator(request)
        result = ''
        for i in iterator:
            result += i
        self.assertIn('center', result)
        self.assertIn('analysis_id', result)
        self.assertIn(self.last_modified[:10], result)
        self.assertIn(self.analysis_id, result)
        self.assertNotIn(self.analysis_id2, result)
        self.assertIn('Error!', result)
        # test message added on error
        self.assertIn('messages', request.session)

        # analysis_xml iterator
        iterator = analysis_xml_iterator(request)
        result = ''
        for i in iterator:
            result += i
        self.assertIn('ResultSet', result)
        self.assertIn('Result id="1"', result)
        self.assertNotIn('Result id="2"', result)
        self.assertNotIn('Error!', result)
        self.assertEqual(len(request.session['messages']), 2)

    def test_metadata_views(self):
        request = get_request()
        request.session.save()
        cart = Cart(session=request.session)
        analysis = AnalysisFactory.create(
                analysis_id=self.analysis_id,
                last_modified=self.last_modified)
        CartItemFactory.create(
                cart=cart.cart,
                analysis=analysis)
        analysis = AnalysisFactory.create(
                analysis_id=self.analysis_id2,
                last_modified=self.last_modified2)
        CartItemFactory.create(
                cart=cart.cart,
                analysis=analysis)

        # test summary
        response = summary(request)
        content = response.content
        self.assertTrue(all(field.lower().replace(' ', '_') in content
                            for field in settings.TABLE_COLUMNS))
        self.assertTrue(self.analysis_id in content)
        self.assertTrue(self.analysis_id2 in content)
        self._check_content_type_and_disposition(response, type='text/tsv', filename='summary.tsv')

        # test metadata view
        response = metadata(request)
        content = response.content
        self.assertTrue(
                ('<analysis_id>%s</analysis_id>' % self.analysis_id in content) or
                ('<str name="analysis_id">%s</str>' % self.analysis_id in content))
        self.assertTrue(
                ('<analysis_id>%s</analysis_id>' % self.analysis_id2 in content) or
                ('<str name="analysis_id">%s</str>' % self.analysis_id2 in content))
        self._check_content_type_and_disposition(response, type='text/xml', filename='metadata.xml')

        # test manifest
        response = manifest(request)
        content = response.content
        self.assertTrue(
                ('<analysis_id>%s</analysis_id>' % self.analysis_id in content) or
                ('<str name="analysis_id">%s</str>' % self.analysis_id in content))
        self.assertTrue(
                ('<analysis_id>%s</analysis_id>' % self.analysis_id2 in content) or
                ('<str name="analysis_id">%s</str>' % self.analysis_id2 in content))
        self._check_content_type_and_disposition(response, type='text/xml', filename='manifest.xml')

    def _check_content_type_and_disposition(self, response, type, filename):
        self.assertEqual(response['Content-Type'], type)
        self.assertIn('attachment; filename=%s' % filename, response['Content-Disposition'])


class CartFormsTestCase(TestCase):

    def test_selected_items_form(self):

        test_data_set = [{
            'selected_items': json.dumps([
                    {
                        'analysis_id': '7850f073-642a-40a8-b49d-e328f27cfd66',
                        'state': 'live'
                    }, {
                        'analysis_id': '796e11c8-b873-4c37-88cd-18dcd7f287ec',
                        'state': 'live'
                    }]),
            'is_valid': True,
            }, {
            'selected_items': json.dumps([
                    {
                        'analysis_id': '7850f073-642a-40a8-b49d-e328f27cfd66',
                        'state': 'live'
                    },
                        '796e11c8-b873-4c37-88cd-18dcd7f287ec',
                    ]),
            'is_valid': False,
            }, {
            'selected_items': 123,
            'is_valid': False,
            }, {
            'selected_items': json.dumps({'study': 'TCGA', 'size': 10}),
            'is_valid': False}]

        for data in test_data_set:
            form = SelectedItemsForm(data)
            self.assertEqual(form.is_valid(), data['is_valid'])

        form = SelectedItemsForm(test_data_set[0])
        form.is_valid()
        self.assertEqual(
            form.cleaned_data['selected_items'][0]['analysis_id'],
            '7850f073-642a-40a8-b49d-e328f27cfd66')

    def test_all_items_form(self):

        test_data_set = [{
            'filters': json.dumps({'center': '(1,2)', 'state': '(live)'}),
            'is_valid': True,
        }, {
            'filters': json.dumps(['bad', 'filters']),
            'is_valid': False,
        }]

        for data in test_data_set:
            form = AllItemsForm(data)
            self.assertEqual(form.is_valid(), data['is_valid'])

        form = AllItemsForm(test_data_set[0])
        form.is_valid()
        self.assertEqual(
            form.cleaned_data['filters'],
            {'center': '(1,2)', 'state': '(live)'})


class CartCommandsTestCase(TestCase):

    """
    detail_2items.xml contains:
    015fd6a5-a77e-4bd1-9430-b44d1c043b54 2013-05-16T20:43:40Z
    015090b8-86f3-4e60-a1ec-89b16d0be113 2013-05-16T20:43:40Z
    """
    analysis_id = '015fd6a5-a77e-4bd1-9430-b44d1c043b54'
    last_modified = '2013-05-16T20:43:40Z'

    def get_xml_file(self, url):
        path = os.path.join(
                os.path.dirname(__file__),
                'test_data/minimal_2items_%s.xml' % settings.API_TYPE.lower())
        return codecs.open(path, 'r', encoding='utf-8')

    @patch('cghub.apps.core.requests.RequestMinimal.get_xml_file', get_xml_file)
    def test_update_full_metadata_cache(self):
        # remove existed cache
        path = get_cart_cache_file_path(
                analysis_id=self.analysis_id,
                last_modified=self.last_modified)
        if os.path.exists(path):
            os.remove(path)
        # remove analysis
        try:
            analysis = Analysis.objects.get(analysis_id=self.analysis_id)
            analysis.delete()
        except Analysis.DoesNotExist:
            pass
        stdout = StringIO()
        stderr = StringIO()
        try:
            call_command(
                    'update_full_metadata_cache',
                    stdout=stdout, stderr=stderr)
        except SystemExit:
            pass
        stdout.seek(0)
        stdout = stdout.read()
        stderr.seek(0)
        stderr = stderr.read()
        self.assertIn('cache files were updated', stdout)
        self.assertIn(': Done', stderr)
        self.assertIn('was created', stderr)
        self.assertIn(self.analysis_id, stderr)
        self.assertTrue(os.path.exists(path))
