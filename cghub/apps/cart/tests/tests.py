import os
import shutil

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.utils import timezone
from django.conf import settings

from cghub.apps.core import browser_text_search
from cghub.apps.core.tests import create_session

from ..utils import (
                    manifest, metadata, summary,
                    analysis_xml_iterator, summary_tsv_iterator)
from ..forms import SelectedFilesForm, AllFilesForm
from ..cache import (
                    AnalysisFileException, get_cart_cache_file_path, 
                    save_to_cart_cache, get_analysis_path, get_analysis,
                    get_analysis_xml, is_cart_cache_exists)


class CartTestCase(TestCase):
    RANDOM_IDS = [
                '017a4d4e-9f4b-4904-824e-060fde3ca223',
                '016b792f-e659-4143-b833-163141e21363',
                '01810b1a-84e4-43d5-8a1e-42b132a1126f']

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
            self.assertEqual(f in response.content, True)

    def test_cart_remove_files(self):
        # add files
        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(
                        url, {'selected_items': json.dumps(self.RANDOM_IDS)},
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # remove files
        rm_selected_files = [self.RANDOM_IDS[0], self.RANDOM_IDS[1]]
        url = reverse('cart_add_remove_files', args=['remove'])
        self.client.post(
                        url, {'selected_files': rm_selected_files},
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

        # test removing doesn't loses sorting
        rm_selected_files = [self.RANDOM_IDS[2]]
        params = '?sort_by=analysis_id'
        url = reverse('cart_add_remove_files', args=['remove']) + params
        response = self.client.post(
                    url,
                    {'selected_files': rm_selected_files},
                    **{'HTTP_REFERER':'http://somepage.com/%s' % params,
                    'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertRedirects(response, reverse('cart_page') + params)

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

    def test_cart_add_raise_http_404_when_get(self):
        """
        Only POST method allowed for 'cart_add_remove_files' url
        """
        url = reverse('cart_add_remove_files', args=['add'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class CartClearTestCase(TestCase):
    IDS_IN_CART = [
                    '017a4d4e-9f4b-4904-824e-060fde3ca223',
                    '016b792f-e659-4143-b833-163141e21363',
                    '01810b1a-84e4-43d5-8a1e-42b132a1126f']

    def setUp(self):
        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(
                        url, {'selected_items': json.dumps(self.IDS_IN_CART)},
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_cart_clear(self):
        url = reverse('cart_clear')
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Files in your cart: 0 (0 Bytes)")
        self.assertContains(response, "Your cart is empty!")


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
        self.assertTrue(self.client.session.session_key)
        self.assertIn(
                '00b27c0f-acf5-434c-8efa-25b1f3c4f506',
                self.client.session['cart'])
        self.assertEqual(
                len(self.client.session['cart']['00b27c0f-acf5-434c-8efa-25b1f3c4f506']),
                1)
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
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['action'], 'redirect')
        self.assertTrue(self.client.session.session_key)
        self.assertIn(
                '00b27c0f-acf5-434c-8efa-25b1f3c4f506',
                self.client.session['cart'])
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
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['action'], 'redirect')
        self.assertTrue(self.client.session.session_key)
        self.assertTrue(isinstance(self.client.session['cart'], dict))


class CartCacheTestCase(TestCase):

    """
    Cached files will be used
    7b9cd36a-8cbb-4e25-9c08-d62099c15ba1 - 2013-05-16T20:50:58Z
    8cab937e-115f-4d0e-aa5f-9982768398c2 - 2013-04-27T01:47:09Z
    """
    analysis_id = '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1'
    last_modified = '2013-05-16T20:50:58Z'
    analysis_id2 = '8cab937e-115f-4d0e-aa5f-9982768398c2'
    last_modified2 = '2013-05-16T20:51:58Z'

    def test_get_cache_file_path(self):
        self.assertEqual(
                get_cart_cache_file_path(
                        '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1',
                        '2012-10-29T21:56:12Z'),
                os.path.join(
                        settings.CART_CACHE_DIR,
                        '7b/9c/7b9cd36a-8cbb-4e25-9c08-d62099c15ba1/2012-10-29T21:56:12Z/analysisFull.xml'))
        self.assertEqual(
                get_cart_cache_file_path(
                        '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1',
                        '2012-10-29T21:56:12Z',
                        short=True),
                os.path.join(
                        settings.CART_CACHE_DIR,
                        '7b/9c/7b9cd36a-8cbb-4e25-9c08-d62099c15ba1/2012-10-29T21:56:12Z/analysisShort.xml'))

    def test_save_to_cart_cache(self):
        path = os.path.join(
                            settings.CART_CACHE_DIR,
                            self.analysis_id[:2],
                            self.analysis_id[2:4],
                            self.analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        path_full = get_cart_cache_file_path(self.analysis_id, self.last_modified)
        path_short = get_cart_cache_file_path(self.analysis_id, self.last_modified, short=True)
        # check is_cart_cache_exists
        self.assertFalse(is_cart_cache_exists(self.analysis_id, self.last_modified))
        result = save_to_cart_cache(self.analysis_id, self.last_modified)
        self.assertTrue(os.path.exists(path_full))
        self.assertTrue(os.path.exists(path_short))
        self.assertTrue(is_cart_cache_exists(self.analysis_id, self.last_modified))
        shutil.rmtree(path)
        # check exception raises when file does not exists
        bad_analysis_id = 'badanalysisid'
        path = os.path.join(
                    settings.CART_CACHE_DIR,
                    bad_analysis_id[:2],
                    bad_analysis_id[2:4],
                    bad_analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        try:
            save_to_cart_cache(bad_analysis_id, self.last_modified)
        except AnalysisFileException as e:
            self.assertEqual(unicode(e), 'File for analysis_id=badanalysisid '
            'that was last modified 2013-05-16T20:50:58Z. '
            'File with specified analysis_id does not exists')
        else:
            raise False, 'AnalysisFileException doesn\'t raised'
        if os.path.isdir(path):
            shutil.rmtree(path)
        # check case when file was updated
        path = os.path.join(
                        settings.CART_CACHE_DIR,
                        self.analysis_id[:2],
                        self.analysis_id[2:4],
                        self.analysis_id)
        try:
            save_to_cart_cache(self.analysis_id, '1900-10-29T21:56:12Z')
        except AnalysisFileException:
            assert False, 'Most recent file was not downloaded'
        if os.path.isdir(path):
            shutil.rmtree(path)
        # check access denied to files outside cache dir
        try:
            save_to_cart_cache(self.analysis_id, '../../same_outside_dir')
        except AnalysisFileException as e:
            self.assertEqual(
                unicode(e),
                'File for analysis_id=7b9cd36a-8cbb-4e25-9c08-d62099c15ba1 '
                'that was last modified ../../same_outside_dir. '
                'Bad analysis_id or last_modified')
        else:
            raise False, 'AnalysisFileException doesn\'t raised'

    def test_get_analysis(self):
        # test get_analysis_path
        path = os.path.join(
                            settings.CART_CACHE_DIR,
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
        analysis = get_analysis(self.analysis_id, self.last_modified, short=False)
        self.assertIn('analysis_xml', analysis['xml'])
        # short version
        analysis = get_analysis(self.analysis_id, self.last_modified, short=True)
        self.assertNotIn('analysis_xml', analysis['xml'])

    def test_get_analysis_xml(self):
        xml, size = get_analysis_xml(
            analysis_id=self.analysis_id,
            last_modified=self.last_modified)
        self.assertNotIn('Result', xml)
        self.assertIn('analysis_id', xml)
        self.assertEqual(size, 172861573)

    def test_analysis_xml_iterator(self):
        data = {
            self.analysis_id: {'last_modified': self.last_modified, 'state': 'live'},
            self.analysis_id2: {'last_modified': self.last_modified2, 'state': 'live'}}
        iterator = analysis_xml_iterator(data)
        result = ''
        for i in iterator:
            result += i
        self.assertIn('ResultSet', result)
        self.assertIn('Result id="1"', result)
        self.assertIn('Result id="2"', result)

    def test_summary_tsv_iterator(self):
        data = {
            self.analysis_id: {'last_modified': self.last_modified, 'state': 'live'},
            self.analysis_id2: {'last_modified': self.last_modified2, 'state': 'live'}}
        iterator = summary_tsv_iterator(data)
        result = ''
        for i in iterator:
            result += i
        self.assertIn('center', result)
        self.assertIn('analysis_id', result)
        self.assertIn(self.last_modified[:10], result)
        self.assertIn(self.analysis_id, result)
        self.assertIn(self.analysis_id2, result)

    def test_manifest(self):
        data = {
            self.analysis_id: {'analysis_id': self.analysis_id},
            self.analysis_id2: {'analysis_id': self.analysis_id2}}
        response = manifest(data)
        content = response.content
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.analysis_id in content)
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.analysis_id2 in content)
        self._check_content_type_and_disposition(response, type='text/xml', filename='manifest.xml')

    def test_metadata(self):
        data = {
            self.analysis_id: {'analysis_id': self.analysis_id},
            self.analysis_id2: {'analysis_id': self.analysis_id2}}
        response = metadata(data)
        content = response.content
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.analysis_id in content)
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.analysis_id2 in content)
        self._check_content_type_and_disposition(response, type='text/xml', filename='metadata.xml')

    def test_summary(self):
        data = {
            self.analysis_id: {'analysis_id': self.analysis_id},
            self.analysis_id2: {'analysis_id': self.analysis_id2}}
        response = summary(data)
        content = response.content
        self.assertTrue(all(field.lower().replace(' ', '_') in content
                            for field in settings.TABLE_COLUMNS))
        self.assertTrue(self.analysis_id in content)
        self.assertTrue(self.analysis_id2 in content)
        self._check_content_type_and_disposition(response, type='text/tsv', filename='summary.tsv')

    def _check_content_type_and_disposition(self, response, type, filename):
        self.assertEqual(response['Content-Type'], type)
        self.assertIn('attachment; filename=%s' % filename, response['Content-Disposition'])


class CartFormsTestCase(TestCase):

    def test_selected_files_form(self):

        test_data_set = [{
            'selected_items': json.dumps([
                    '7850f073-642a-40a8-b49d-e328f27cfd66',
                    '796e11c8-b873-4c37-88cd-18dcd7f287ec']),
            'is_valid': True,
            }, {
            'selected_items': json.dumps([
                    '7850f073-642a-40a8-b49d-e328f27cfd66',
                    '796e11c8b8734c3788cd18dcd7f287ec']),
            'is_valid': False,
            },{
            'selected_items': 123,
            'is_valid': False,
            }, {
            'selected_items': json.dumps({'study': 'TCGA', 'size': 10}),
            'is_valid': False }]

        for data in test_data_set:
            form = SelectedFilesForm(data)
            self.assertEqual(form.is_valid(), data['is_valid'])

        form = SelectedFilesForm(test_data_set[0])
        form.is_valid()
        self.assertEqual(
            form.cleaned_data['selected_items'][0],
            '7850f073-642a-40a8-b49d-e328f27cfd66')

    def test_all_files_form(self):

        test_data_set = [{
            'filters': json.dumps({'center': '(1,2)', 'state': '(live)'}),
            'is_valid': True,
        }, {
            'filters': json.dumps(['bad', 'filters']),
            'is_valid': False,
        }]

        for data in test_data_set:
            form = AllFilesForm(data)
            self.assertEqual(form.is_valid(), data['is_valid'])

        form = AllFilesForm(test_data_set[0])
        form.is_valid()
        self.assertEqual(
            form.cleaned_data['filters'],
            {'center': '(1,2)', 'state': '(live)'})
