import time, os

from wsapi.api import request as api_request
from wsapi.settings import CACHE_DIR

from django.test import LiveServerTestCase
from django.conf import settings

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

from cghub.apps.core.tests.ui_tests import (
                            wsapi_cache_copy, wsapi_cache_remove)
from cghub.apps.core.templatetags.search_tags import (
                            get_name_by_code, get_sample_type_by_code,
                            file_size)


class LinksNavigationsTests(LiveServerTestCase):
    cache_files = ('f6d938fbf161765df8d8d7cd1ef87428.xml',)

    @classmethod
    def setUpClass(self):
        self.selenium = webdriver.Firefox()
        self.selenium.implicitly_wait(5)
        super(LinksNavigationsTests, self).setUpClass()
        wsapi_cache_copy(self.cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(LinksNavigationsTests, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

    def test_cart_link(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_partial_link_text("Cart").click()

    def test_home_link(self):
        self.selenium.get("{url}/{path}".format(url=self.live_server_url,
                                        path="help"))
        self.selenium.find_element_by_partial_link_text("Search").click()

    def test_help_link(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_partial_link_text("Help").click()


class CartUITests(LiveServerTestCase):
    cache_files = (
                '0aab3523a4352c73abf8940e7c9ae7a5.xml',
                '33b4441ffd0d7ab7ec21f0cff9a53d95.xml',
                '427dcd2c78d4be27efe3d0cde008b1f9.xml',
                '10fec8ea2505e24d4e5705b76461f649.xml',
                '10fec8ea2505e24d4e5705b76461f649.xml-no-attr',
                '72eaed3637a5d9aca2c36dc3c8db14b7.xml',
                '72eaed3637a5d9aca2c36dc3c8db14b7.xml-no-attr',
                'f6d938fbf161765df8d8d7cd1ef87428.xml')
    selected = [
        '49d8aaef-72e0-4165-9c1f-d21da1dc6107',
        'abf14d92-2bbe-4393-95a8-9f1f51d57f5d'
    ]
    unselected = [
        '4bd7ad2f-d72d-443c-88f1-bd921fd0c5c8',
    ]
    query = "6d5*"

    @classmethod
    def setUpClass(self):
        # Presetup Firefox for file downloads
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", CACHE_DIR)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml")

        self.selenium = webdriver.Firefox(firefox_profile=fp)
        self.selenium.implicitly_wait(5)
        super(CartUITests, self).setUpClass()
        wsapi_cache_copy(self.cache_files)
        # Calculate uuid for items on the first page
        lxml = api_request(file_name=CACHE_DIR + self.cache_files[0])._lxml_results
        uuids = lxml.xpath('/ResultSet/Result/analysis_id')
        self.page_uuids = uuids[:settings.DEFAULT_PAGINATOR_LIMIT - 1]

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(CartUITests, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

    def test_cart(self):
        # Testing proper item adding
        driver = self.selenium
        driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

        # Test Select all link in search results
        for uuid in self.page_uuids:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
            assert not checkbox.is_selected()

        btn = driver.find_element_by_css_selector('input.js-select-all')
        btn.click()

        for uuid in self.page_uuids:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
            assert checkbox.is_selected()

        btn = driver.find_element_by_css_selector('input.js-select-all')
        btn.click()

        # Select two items for adding to cart
        for uuid in self.selected:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
            checkbox.click()

        btn = driver.find_element_by_css_selector('button.add-to-cart-btn')
        btn.click()
        time.sleep(1)
        assert driver.current_url == '%s/cart/' % self.live_server_url

        for uuid in self.selected:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
        for uuid in self.unselected:
            try:
                checkbox = driver.find_element_by_css_selector(
                    'input[value="%s"]' % uuid)
                assert False, "Element mustn't be found on the page"
            except NoSuchElementException:
                pass

        stat = driver.find_element_by_xpath('//div[@class="cart-content"]//div//span')
        assert stat.text == 'Files in your cart: 2 (26.44 GB)'

        cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
        assert cart_link.text == 'Cart (2)'

        # Testing 'Select all' button in the cart
        for uuid in self.selected:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
            assert not checkbox.is_selected()

        btn = driver.find_element_by_css_selector('input.js-select-all')
        btn.click()
        driver.implicitly_wait(1)

        for uuid in self.selected:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
            assert checkbox.is_selected()

        # Checking file downloading
        # Check there are no pre-existed files in /tmp/wsapi/
        try:
            os.remove(CACHE_DIR + 'manifest.xml')
            os.remove(CACHE_DIR + 'metadata.xml')
        except OSError:
            pass
        # Download Manifest file
        btn = driver.find_element_by_class_name('cart-form-download-manifest')
        btn.click()
        driver.implicitly_wait(5)
        try:
            os.remove(CACHE_DIR + 'manifest.xml')
        except OSError:
            assert False, "File manifest.xml wasn't downloaded"

        # Download Metadata file
        btn = driver.find_element_by_class_name('cart-form-download-xml')
        btn.click()
        driver.implicitly_wait(5)
        try:
            os.remove(CACHE_DIR + 'metadata.xml')
        except OSError:
            assert False, "File metadata.xml wasn't downloaded"

        # Remove selected from cart
        btn = driver.find_element_by_class_name('cart-form-remove')
        btn.click()

        stat = driver.find_element_by_xpath('//div[@class="cart-content"]//div//span')
        assert stat.text == 'Files in your cart: 0 (0 Bytes)'

        cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
        assert cart_link.text == 'Cart (0)'

        message = driver.find_element_by_xpath('//form[@action="/cart/action/"]//p')
        assert message.text == 'Your cart is empty!'


class SortWithinCartTestCase(LiveServerTestCase):
    cache_files = (
                    'cb712a7b93a6411001cbc34cfb883594.xml',
                    'ecbf7eaaf5b476df08b2997afd675701.xml',
                    '376f9b98cb2e63cb7dddfbbd5647bcf7.xml'
                    )
    query = "6d53*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SortWithinCartTestCase, self).setUpClass()
        wsapi_cache_copy(self.cache_files)
        lxml = api_request(file_name=CACHE_DIR + self.cache_files[1])._lxml_results
        self.items_count = lxml.Hits

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SortWithinCartTestCase, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

    def test_sort_within_cart(self):
        # Adding first 10 items to cart for sorting
        driver = self.selenium
        driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

        driver.find_element_by_css_selector('input.js-select-all').click()
        driver.find_element_by_css_selector('button.add-to-cart-btn').click()

        attrs = [
            'analysis_id', 'study', 'disease_abbr', 'disease_abbr',
            'library_strategy', 'refassem_short_name', 'center_name',
            'center_name', 'analyte_code', 'upload_date', 'last_modified',
            'sample_type', 'sample_type', 'state', 'legacy_sample_id',
            'sample_accession', 'files_size']

        for i, attr in enumerate(attrs):
            if i in (3, 7, 11):
                continue

            # scroll table
            if i > 5:
                driver.execute_script("$('.flexigrid div')"
                        ".scrollLeft($('.sort-link[href*=%s]')"
                        ".parents('th').position().left);" % attr)
            time.sleep(5)
            sort_link = driver.find_element_by_xpath(
                '//div[@class="hDivBox"]//table//thead//tr//th//div//a[@href="/cart/?sort_by=%s"]' % attr)
            sort_link.click()
            # Getting list with sorted attributes
            results = api_request(file_name=CACHE_DIR + self.cache_files[1], sort_by=attr).Result
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
                else:
                    self.assertEqual(text.strip(), str(sorted_attr[j]))
            # Reverse sorting
            driver.execute_script("$('.flexigrid div')"
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
                else:
                    self.assertEqual(text.strip(), str(sorted_attr[j]))
