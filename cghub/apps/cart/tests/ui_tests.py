import time, os

from wsapi.api import request as api_request

from django.test import LiveServerTestCase
from django.conf import settings

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

from cghub.apps.core.tests.ui_tests import TEST_SETTINGS
from cghub.apps.core.templatetags.search_tags import (
                            get_name_by_code, get_sample_type_by_code,
                            file_size)


class LinksNavigationsTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = webdriver.Firefox()
        self.selenium.implicitly_wait(5)
        super(LinksNavigationsTestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(LinksNavigationsTestCase, self).tearDownClass()

    def test_cart_link(self):
        with self.settings(**TEST_SETTINGS):
            self.selenium.get(self.live_server_url)
            self.selenium.find_element_by_partial_link_text("Cart").click()
            time.sleep(2)

    def test_home_link(self):
        with self.settings(**TEST_SETTINGS):
            # FIXME(nanvel): merge with previous test
            self.selenium.get("{url}/{path}".format(url=self.live_server_url,
                                        path="help"))
            self.selenium.find_element_by_partial_link_text("Search").click()
            time.sleep(2)

    def test_help_link(self):
        with self.settings(**TEST_SETTINGS):
            # FIXME(nanvel): merge in one test with previous
            self.selenium.get(self.live_server_url)
            self.selenium.find_element_by_partial_link_text("Help").click()
            time.sleep(2)


class CartUITestCase(LiveServerTestCase):
    wsapi_cache_files = (
                    '9e46b6f29ecc2c5282143a1fdf24f76b.xml',
                    '128a4ee167e9c3eacf2e5943b93b6b53.xml',
                    '4d3fee9f8557fc0de585af248b598c44.xml',
                    )
    cart_cache_files = (
                    '30dcdc5a-172f-4fa2-b9d2-6d50ee8f3a58',
                    '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1',
                    )

    selected = [
        '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1',
        '30dcdc5a-172f-4fa2-b9d2-6d50ee8f3a58'
    ]
    unselected = [
        'beddd009-4efb-471f-bc4e-d872b50daa0f',
    ]
    query = "6d50"

    @classmethod
    def setUpClass(self):
        # presetup Firefox for file downloads
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", settings.WSAPI_CACHE_DIR)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml,text/tsv")

        self.selenium = webdriver.Firefox(firefox_profile=fp)
        self.selenium.implicitly_wait(5)
        super(CartUITestCase, self).setUpClass()
        # FIXME(nanvel): is this used ?
        # calculate uuid for items on the first page
        lxml = api_request(file_name=settings.WSAPI_CACHE_DIR + self.wsapi_cache_files[0])._lxml_results
        analysis_id = lxml.xpath('/ResultSet/Result/analysis_id')
        self.page_analysis_ids = analysis_id[:settings.DEFAULT_PAGINATOR_LIMIT - 1]

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(CartUITestCase, self).tearDownClass()

    def test_cart(self):
        """
        1. Go to search page
        2. Check that no selected files in table
        3. Click on 'Select all' checkbox
        4. Check that all checkboxes in table checked
        5. Click on 'Select all' checkbox once more (uncheck all checkboxes)
        6. Select ferst two items
        7. Click on 'Add to cart' button
        8. Check that files were really added to cart
        9. Check that no other files were added to cart
        10. Check that dosplayed right files count and size
        11. Remove downloaded before manifest, metadata and summary if exists
        12. Try to download manifest.xml
        13. Try to download metadata.xml
        14. Try to download summary.tsv
        15. Get cart stats
        16. Click 'Remove files from cart'
        17. Get cart stats, check that files count was decremented by 1
        18. Click on 'Clear cart'
        19. Check that cart is empty
        """
        with self.settings(**TEST_SETTINGS):
            # FIXME(nanvel): may be rename test ?
            # test adding item to cart
            driver = self.selenium
            driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

            # check that no selected items
            for analysis_id in self.page_analysis_ids:
                checkbox = driver.find_element_by_css_selector(
                        'input[value="%s"]' % analysis_id)
                assert not checkbox.is_selected()

            # toggle 'Select all' checkbox
            btn = driver.find_element_by_css_selector('input.js-select-all')
            btn.click()

            # check that all checkboxes in table checked
            for analysis_id in self.page_analysis_ids:
                checkbox = driver.find_element_by_css_selector(
                        'input[value="%s"]' % analysis_id)
                assert checkbox.is_selected()

            # toggle 'Select all' checkbox (uncheck)
            btn = driver.find_element_by_css_selector('input.js-select-all')
            btn.click()

            # Select two items for adding to cart
            # FIXME(nanvel): is self.selected exists in results ?
            # FIXME(nanvel): maybe simply select first 2 items ?
            for analysis_id in self.selected:
                checkbox = driver.find_element_by_css_selector(
                        'input[value="%s"]' % analysis_id)
                checkbox.click()

            # click on 'Add to cart'
            btn = driver.find_element_by_css_selector('button.add-to-cart-btn')
            btn.click()
            time.sleep(3)
            assert driver.current_url == '%s/cart/' % self.live_server_url

            # check that files were added to cart and analysis_ids of them exists in table 
            for analysis_id in self.selected:
                checkbox = driver.find_element_by_css_selector(
                        'input[value="%s"]' % analysis_id)
            # check that other files were not added to the cart
            for analysis_id in self.unselected:
                try:
                    checkbox = driver.find_element_by_css_selector(
                            'input[value="%s"]' % analysis_id)
                    assert False, "Element mustn't be found on the page"
                except NoSuchElementException:
                    pass

            stat = driver.find_element_by_xpath('//div[@class="cart-content"]//div//span')
            # FIXME(nanvel): files size can be changed, can we make it constant while testing ?
            assert stat.text == 'Files in your cart: 2 (9,68 GB)'
            cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
            assert cart_link.text == 'Cart (2)'

            # 'Select all' feature tested on search page, and it uses the same js

            # check files downloading
            try:
                os.remove(settings.WSAPI_CACHE_DIR + 'manifest.xml')
                os.remove(settings.WSAPI_CACHE_DIR + 'metadata.xml')
                os.remove(settings.WSAPI_CACHE_DIR + 'summary.tsv')
            except OSError:
                pass

            # download Manifest XML
            btn = driver.find_element_by_class_name('cart-download-manifest')
            btn.click()
            driver.implicitly_wait(5)
            try:
                os.remove(settings.WSAPI_CACHE_DIR + 'manifest.xml')
            except OSError:
                assert False, "File manifest.xml wasn't downloaded"

            # download Metadata XML
            btn = driver.find_element_by_class_name('cart-download-metadata')
            btn.click()
            driver.implicitly_wait(5)
            try:
                os.remove(settings.WSAPI_CACHE_DIR + 'metadata.xml')
            except OSError:
                assert False, "File metadata.xml wasn't downloaded"

            # download Summary TSV
            btn = driver.find_element_by_class_name('cart-download-summary')
            btn.click()
            driver.implicitly_wait(5)
            try:
                os.remove(settings.WSAPI_CACHE_DIR + 'summary.tsv')
            except OSError:
                assert False, "File summary.tsv wasn't downloaded"

            # select first file in table
            checkbox = driver.find_element_by_css_selector(
                    'input[value="%s"]' % self.selected[0])
            checkbox.click()

            # remove seleted files
            stat = driver.find_element_by_xpath('//div[@class="cart-content"]//div//span')
            assert 'Files in your cart: {0}'.format(len(self.selected)) in stat.text

            cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
            assert cart_link.text == 'Cart ({0})'.format(len(self.selected))

            btn = driver.find_element_by_class_name('cart-remove')
            btn.click()

            stat = driver.find_element_by_xpath('//div[@class="cart-content"]//div//span')
            assert 'Files in your cart: {0}'.format(len(self.selected) - 1) in stat.text

            cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
            assert cart_link.text == 'Cart ({0})'.format(len(self.selected) - 1)

            # test 'clear cart' button
            btn = driver.find_element_by_class_name('cart-clear')
            btn.click()
            stat = driver.find_element_by_xpath('//div[@class="cart-content"]//div//span')
            assert stat.text == 'Files in your cart: 0 (0 Bytes)'

            cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
            assert cart_link.text == 'Cart (0)'

            message = driver.find_element_by_xpath('//form[@action="/cart/action/"]//p')
            assert message.text == 'Your cart is empty!'


class SortWithinCartTestCase(LiveServerTestCase):

    query = "6d711"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SortWithinCartTestCase, self).setUpClass()
        lxml = api_request(file_name=settings.WSAPI_CACHE_DIR + self.wsapi_cache_files[4])._lxml_results
        self.items_count = lxml.Hits

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SortWithinCartTestCase, self).tearDownClass()

    def test_sort_within_cart(self):
        with self.settings(**TEST_SETTINGS):
            # add first 10 items to cart for sorting
            driver = self.selenium
            driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

            driver.find_element_by_css_selector('input.js-select-all').click()
            driver.find_element_by_css_selector('button.add-to-cart-btn').click()

            # FIXME(nanvel): make it simple, check only few columns, not all
            attrs = [
                'analysis_id', 'study', 'disease_abbr', 'disease_abbr',
                'library_strategy', 'platform', 'refassem_short_name', 'center_name',
                'center_name', 'analyte_code', 'upload_date', 'last_modified',
                'sample_type', 'sample_type', 'state', 'legacy_sample_id',
                'sample_accession', 'files_size']

            for i, attr in enumerate(attrs):
                if i in (3, 8, 12):
                    continue

                # scroll table
                if i > 5:
                    time.sleep(1)
                    driver.execute_script("$('.viewport')"
                            ".scrollLeft($('.sort-link[href*=%s]')"
                            ".parents('th').position().left);" % attr)
                time.sleep(3)
                sort_link = driver.find_element_by_xpath(
                        '//div[@class="hDivBox"]//table//thead//tr//th//div//a[@href="/cart/?sort_by=%s"]' % attr)
                sort_link.click()
                # get list with sorted attributes
                results = api_request(file_name=settings.WSAPI_CACHE_DIR + self.wsapi_cache_files[1], sort_by=attr).Result
                sorted_attr = [getattr(r, attr) for r in results]

                for j in range(self.items_count):
                    text = driver.find_element_by_xpath(
                            '//div[@class="bDiv"]//table//tbody//tr[%d]//td[%d]/div' % (j + 1, i + 2)).text
                    if attr == 'sample_type':
                        self.assertEqual(text, get_sample_type_by_code(sorted_attr[j], 'full'))
                    elif attr in ('analyte_code', 'study', 'state'):
                        self.assertEqual(text, get_name_by_code(attr, sorted_attr[j]))
                    elif attr == 'files_size':
                        self.assertEqual(text.strip(), file_size(sorted_attr[j]))
                    elif attr in ('upload_date', 'last_modified'):
                        self.assertEqual(text.strip(), str(sorted_attr[j]).split('T')[0])
                    else:
                        self.assertEqual(text.strip(), str(sorted_attr[j]))
                # reverse sorting
                time.sleep(1)
                driver.execute_script("$('.viewport')"
                        ".scrollLeft($('.sort-link[href*=%s]')"
                        ".parents('th').position().left);" % attr);
                sort_link = driver.find_element_by_xpath(
                        '//div[@class="hDivBox"]//table//thead//tr//th//div//a[@href="/cart/?sort_by=-%s"]' % attr)
                sort_link.click()

                sorted_attr.reverse()
                for j in range(self.items_count):
                    text = driver.find_element_by_xpath(
                            '//div[@class="bDiv"]//table//tbody//tr[%d]//td[%d]//div' % (j + 1, i + 2)).text
                    if attr == 'sample_type':
                        self.assertEqual(text, get_sample_type_by_code(sorted_attr[j], 'full'))
                    elif attr in ('analyte_code', 'study', 'state'):
                        self.assertEqual(text, get_name_by_code(attr, sorted_attr[j]))
                    elif attr == 'files_size':
                        self.assertEqual(text.strip(), file_size(sorted_attr[j]))
                    elif attr in ('upload_date', 'last_modified'):
                        self.assertEqual(text.strip(), str(sorted_attr[j]).split('T')[0])
                    else:
                        self.assertEqual(text.strip(), str(sorted_attr[j]))
