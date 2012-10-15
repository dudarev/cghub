import os
import time
import shutil

from wsapi.settings import CACHE_DIR
from wsapi.api import request as api_request

from django.test import LiveServerTestCase
from django.conf import settings

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

from cghub.apps.core.templatetags.search_tags import (get_name_by_code,
    get_sample_type_by_code)


class LinksNavigationsTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(5)
        super(LinksNavigationsTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(LinksNavigationsTests, cls).tearDownClass()

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
    cache_file = '0aab3523a4352c73abf8940e7c9ae7a5.xml'
    selected = [
        'a15b7a89-0085-4879-9715-a37a460ff26d',
        'd1cc01ad-951b-424a-9860-2f400d3e0282'
    ]
    unselected = [
        'f9570c3d-31ab-4356-96f0-d5788a4fb5b4',
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
        TEST_DATA_DIR = 'cghub/test_data/'
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        shutil.copy(
            os.path.join(TEST_DATA_DIR, self.cache_file),
            os.path.join(CACHE_DIR, self.cache_file)
        )
        # Calculate uuid for items on the first page
        lxml = api_request(file_name=CACHE_DIR + self.cache_file)._lxml_results
        uuids = lxml.xpath('/ResultSet/Result/analysis_id')
        self.page_uuids = uuids[:settings.DEFAULT_PAGINATOR_LIMIT - 1]

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(CartUITests, self).tearDownClass()
        os.remove(os.path.join(CACHE_DIR, self.cache_file))

    def test_cart(self):
        # Testing proper item adding
        driver = self.selenium
        driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

        # Test Select all link
        for uuid in self.page_uuids:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
            assert not checkbox.is_selected()

        btn = driver.find_element_by_css_selector('button.select_all_items')
        btn.click()

        for uuid in self.page_uuids:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
            assert checkbox.is_selected()

        btn = driver.find_element_by_css_selector('button.select_all_items')
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
        assert stat.text == 'Files in your cart: 2 (60764.00 Mb)'

        cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
        assert cart_link.text == 'Cart (2)'

        # Testing 'Select all' button
        for uuid in self.selected:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
            assert not checkbox.is_selected()

        btn = driver.find_element_by_css_selector('button.select_all_items')
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
        assert stat.text == 'Files in your cart: 0 (0.00 Mb)'

        cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
        assert cart_link.text == 'Cart (0)'

        message = driver.find_element_by_xpath('//form[@action="/cart/action/"]//p')
        assert message.text == 'Your cart is empty!'


class SortWithinCartTestCase(LiveServerTestCase):
    cache_file = '376f9b98cb2e63cb7dddfbbd5647bcf7.xml'
    query = "6d53*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SortWithinCartTestCase, self).setUpClass()
        TEST_DATA_DIR = 'cghub/test_data/'
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        shutil.copy(
            os.path.join(TEST_DATA_DIR, self.cache_file),
            os.path.join(CACHE_DIR, self.cache_file)
        )
        lxml = api_request(file_name=CACHE_DIR + self.cache_file)._lxml_results
        self.items_count = lxml.Hits

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SortWithinCartTestCase, self).tearDownClass()
        os.remove(os.path.join(CACHE_DIR, self.cache_file))

    def test_sort_within_cart(self):
        # Adding first 10 items to cart for sorting
        driver = self.selenium
        driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))
        btn = driver.find_element_by_css_selector('button.select_all_items')
        btn.click()
        btn = driver.find_element_by_css_selector('button.add-to-cart-btn')
        btn.click()
        driver.implicitly_wait(1)

        attrs = [
            'legacy_sample_id', 'analysis_id', 'sample_accession', 'files_size',
            'last_modified', 'disease_abbr', 'sample_type', 'analyte_code',
            'library_strategy', 'center_name']

        for i, attr in enumerate(attrs):
            # IMPORTANT
            # fix for extra 'full name' columns, their sorting links are duplicates anyway
            # after changing the columns' set check attrs list above
            if i in (6, 8, 12):
                continue

            sort_link = driver.find_element_by_xpath(
                '//div[@class="hDivBox"]//table//thead//tr//th//div//a[@href="/cart/?sort_by=%s"]' % attr)
            sort_link.click()
            # Getting list with sorted attributes
            results = api_request(file_name=CACHE_DIR + self.cache_file, sort_by=attr).Result
            sorted_attr = [getattr(r, attr) for r in results]

            for j in range(self.items_count):
                text = driver.find_element_by_xpath(
                    '//div[@class="bDiv"]//table//tbody//tr[%d]//td[%d]//div' % (j + 1, i + 2)).text
                if attr == 'sample_type':
                    self.assertEqual(text, get_sample_type_by_code(sorted_attr[j], 'shortcut'))
                elif attr == 'analyte_code':
                    self.assertEqual(text, get_name_by_code(attr, sorted_attr[j]))
                else:
                    self.assertEqual(text.strip(), str(sorted_attr[j]))
            # Reverse sorting
            sort_link = driver.find_element_by_xpath(
                '//div[@class="hDivBox"]//table//thead//tr//th//div//a[@href="/cart/?sort_by=-%s"]' % attr)
            sort_link.click()

            sorted_attr.reverse()
            for j in range(self.items_count):
                text = driver.find_element_by_xpath(
                    '//div[@class="bDiv"]//table//tbody//tr[%d]//td[%d]//div' % (j + 1, i + 2)).text
                if attr == 'sample_type':
                    self.assertEqual(text, get_sample_type_by_code(sorted_attr[j], 'shortcut'))
                elif attr == 'analyte_code':
                    self.assertEqual(text, get_name_by_code(attr, sorted_attr[j]))
                else:
                    self.assertEqual(text.strip(), str(sorted_attr[j]))
