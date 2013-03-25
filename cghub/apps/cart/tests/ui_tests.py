import time, os

from wsapi.api import request as api_request

from django.test import LiveServerTestCase
from django.conf import settings

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

from cghub.apps.core.tests.ui_tests import (
                            wsapi_cache_copy,
                            wsapi_cache_remove)
from cghub.apps.core.templatetags.search_tags import (
                            get_name_by_code,
                            get_sample_type_by_code,
                            file_size)


class LinksNavigationsTestCase(LiveServerTestCase):
    cache_files = ('28e1cf619d26bdab58fcab5e7a2b9e6c.xml',)

    @classmethod
    def setUpClass(self):
        self.selenium = webdriver.Firefox()
        self.selenium.implicitly_wait(5)
        super(LinksNavigationsTestCase, self).setUpClass()
        wsapi_cache_copy(self.cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(LinksNavigationsTestCase, self).tearDownClass()
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


class CartUITestCase(LiveServerTestCase):
    cache_files = (
                    '3b687dc26053309770100fd85a0dcfe8.xml',
                    '4d3fee9f8557fc0de585af248b598c44.xml',
                    '4d3fee9f8557fc0de585af248b598c44.xml-no-attr',
                    '9e46b6f29ecc2c5282143a1fdf24f76b.xml',
                    '128a4ee167e9c3eacf2e5943b93b6b53.xml',
                    '128a4ee167e9c3eacf2e5943b93b6b53.xml-no-attr',
                    'b28367eb5d8e8d30c33b4cb47ac5b0b3.xml',
                    )
    selected = [
        '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1',
        '30dcdc5a-172f-4fa2-b9d2-6d50ee8f3a58'
    ]
    unselected = [
        'beddd009-4efb-471f-bc4e-d872b50daa0f',
    ]
    query = "6d50*"

    @classmethod
    def setUpClass(self):
        # Presetup Firefox for file downloads
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", settings.WSAPI_CACHE_DIR)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml,text/tsv")

        self.selenium = webdriver.Firefox(firefox_profile=fp)
        self.selenium.implicitly_wait(5)
        super(CartUITestCase, self).setUpClass()
        wsapi_cache_copy(self.cache_files)
        # Calculate uuid for items on the first page
        lxml = api_request(file_name=settings.WSAPI_CACHE_DIR + self.cache_files[0])._lxml_results
        uuids = lxml.xpath('/ResultSet/Result/analysis_id')
        self.page_uuids = uuids[:settings.DEFAULT_PAGINATOR_LIMIT - 1]

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(CartUITestCase, self).tearDownClass()
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
        time.sleep(7)
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
        assert stat.text == 'Files in your cart: 2 (9.68 GB)'

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
            os.remove(settings.WSAPI_CACHE_DIR + 'manifest.xml')
            os.remove(settings.WSAPI_CACHE_DIR + 'metadata.xml')
            os.remove(settings.WSAPI_CACHE_DIR + 'summary.tsv')
        except OSError:
            pass

        checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % self.selected[0])
        checkbox.click()

        # Download Manifest in XML file
        btn = driver.find_element_by_class_name('cart-download-manifest')
        btn.click()
        driver.implicitly_wait(5)
        try:
            os.remove(settings.WSAPI_CACHE_DIR + 'manifest.xml')
        except OSError:
            assert False, "File manifest.xml wasn't downloaded"

        # Download Metadata XML file
        btn = driver.find_element_by_class_name('cart-download-metadata')
        btn.click()
        driver.implicitly_wait(5)
        try:
            os.remove(settings.WSAPI_CACHE_DIR + 'metadata.xml')
        except OSError:
            assert False, "File metadata.xml wasn't downloaded"

        # Download Summary TSV file
        btn = driver.find_element_by_class_name('cart-download-summary')
        btn.click()
        driver.implicitly_wait(5)
        try:
            os.remove(settings.WSAPI_CACHE_DIR + 'summary.tsv')
        except OSError:
            assert False, "File summary.tsv wasn't downloaded"

        # Remove selected from cart
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

        # Test 'clear cart' button
        btn = driver.find_element_by_class_name('cart-clear')
        btn.click()
        stat = driver.find_element_by_xpath('//div[@class="cart-content"]//div//span')
        assert stat.text == 'Files in your cart: {0} (0 Bytes)'.format(len(self.selected) - 2)

        cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
        assert cart_link.text == 'Cart ({0})'.format(len(self.selected) - 2)

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
        lxml = api_request(file_name=settings.WSAPI_CACHE_DIR + self.cache_files[1])._lxml_results
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
            results = api_request(file_name=settings.WSAPI_CACHE_DIR + self.cache_files[1], sort_by=attr).Result
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
                elif attr in ('upload_date', 'last_modified'):
                    self.assertEqual(text.strip(), str(sorted_attr[j]).split('T')[0])
                else:
                    self.assertEqual(text.strip(), str(sorted_attr[j]))


class AddAllToCartButtonTestCase(LiveServerTestCase):
    cache_files = (
                    '3b687dc26053309770100fd85a0dcfe8.xml',
                    '9e46b6f29ecc2c5282143a1fdf24f76b.xml',
                    'b28367eb5d8e8d30c33b4cb47ac5b0b3.xml',
                    )
    query = "6d50*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(AddAllToCartButtonTestCase, self).setUpClass()
        wsapi_cache_copy(self.cache_files)
        # Calculate uuid for items on the first page
        lxml2 = api_request(file_name=settings.WSAPI_CACHE_DIR + self.cache_files[0])._lxml_results
        uuids2 = lxml2.xpath('/ResultSet/Result/analysis_id')
        self.page_uuids = uuids2[:settings.DEFAULT_PAGINATOR_LIMIT - 1]

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(AddAllToCartButtonTestCase, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

    def test_addalltocart_button(self):
        driver = self.selenium
        driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

        # Make sure no checkboxes are selected
        for uuid in self.page_uuids:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
            assert not checkbox.is_selected()

        # Get the number of results found
        found_num = driver.find_element_by_css_selector(
            'div.pagination-results').text.split(' ')[1]
        # Make sure cart is empty
        cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
        assert cart_link.text == 'Cart (0)'

        driver.find_element_by_css_selector(
            'button.add-all-to-cart-btn').click()
        time.sleep(10)
        assert driver.current_url == '%s/cart/' % self.live_server_url

        # Make sure exact number of files was added to cart
        cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
        self.assertTrue(found_num in cart_link.text)
        stat = driver.find_element_by_xpath('//div[@class="cart-content"]//div//span')
        self.assertTrue(found_num in stat.text)

        # Make sure all elements from first page are present
        for uuid in self.page_uuids:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
            assert checkbox.is_displayed()
