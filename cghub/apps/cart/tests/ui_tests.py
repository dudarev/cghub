import time, os

from wsapi.api import request as api_request

from django.test import LiveServerTestCase
from django.conf import settings

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

from cghub.apps.core.tests.ui_tests import TEST_SETTINGS, TEST_CACHE_DIR
from cghub.apps.core.templatetags.search_tags import (
                            get_name_by_code, get_sample_type_by_code,
                            file_size)


class NavigationLinksTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = webdriver.Firefox()
        self.selenium.implicitly_wait(5)
        super(NavigationLinksTestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(NavigationLinksTestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def test_lins(self):
        """
        1. Go to search page (default query)
        2. Click on 'Cart' link
        3. Check url
        4. Click on 'Help' link
        5. Check url
        6. Clcik on 'Search' link
        7. Check url
        """
        driver = self.selenium
        with self.settings(**TEST_SETTINGS):
            # search page
            driver.get(self.live_server_url)
            assert '/cart/' not in driver.current_url
            assert '/help/' not in driver.current_url
            # go to cart page
            driver.find_element_by_partial_link_text("Cart").click()
            time.sleep(3)
            assert '/cart/' in driver.current_url
            # go to help page
            driver.find_element_by_partial_link_text("Help").click()
            time.sleep(3)
            assert '/help/' in driver.current_url
            # got back to search page
            driver.find_element_by_partial_link_text("Browser").click()
            time.sleep(3)
            assert '/cart/' not in driver.current_url
            assert '/help/' not in driver.current_url


class CartUITestCase(LiveServerTestCase):

    query = "6d50"

    @classmethod
    def setUpClass(self):
        # presetup Firefox for file downloads
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", TEST_CACHE_DIR)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml,text/tsv")

        self.selenium = webdriver.Firefox(firefox_profile=fp)
        self.selenium.implicitly_wait(5)
        super(CartUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(CartUITestCase, self).tearDownClass()

    def test_cart(self):
        """
        1. Go to search page (with q = self.query)
        2. Click on 'Select all' checkbox
        3. Check that all checkboxes in table checked
        4. Click on 'Select all' checkbox once more (uncheck all checkboxes)
        5. Select ferst two items
        6. Click on 'Add to cart' button
        7. Check that files were really added to cart
        8. Check that no other files were added to cart
        9. Check that dosplayed right files count
        10. Remove downloaded manifest, metadata and summary downloaded before if exists
        11. Try to download manifest.xml
        12. Try to download metadata.xml
        13. Try to download summary.tsv
        14. Get cart stats
        15. Click 'Remove files from cart'
        16. Get cart stats, check that files count was decremented by 1
        17. Click on 'Clear cart'
        18. Check that cart is empty
        """
        with self.settings(**TEST_SETTINGS):
            # test adding items to cart
            driver = self.selenium
            driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

            # get all analysis_ids on the page
            page_analysis_ids = []
            for i in driver.find_elements_by_css_selector('.data-table-checkbox'):
                page_analysis_ids.append(i.get_attribute('value'))
            assert len(page_analysis_ids) > 4

            # check that no selected items
            for analysis_id in page_analysis_ids:
                checkbox = driver.find_element_by_css_selector(
                        'input[value="%s"]' % analysis_id)
                assert not checkbox.is_selected()

            # toggle 'Select all' checkbox
            btn = driver.find_element_by_css_selector('input.js-select-all')
            btn.click()

            # check that all checkboxes in table checked
            for analysis_id in page_analysis_ids:
                checkbox = driver.find_element_by_css_selector(
                        'input[value="%s"]' % analysis_id)
                assert checkbox.is_selected()

            # toggle 'Select all' checkbox (uncheck)
            btn = driver.find_element_by_css_selector('input.js-select-all')
            btn.click()

            # Select two items for adding to cart
            selected = page_analysis_ids[:2]
            unselected = page_analysis_ids[-2:]
            for analysis_id in selected:
                checkbox = driver.find_element_by_css_selector(
                        'input[value="%s"]' % analysis_id)
                checkbox.click()

            # click on 'Add to cart'
            btn = driver.find_element_by_css_selector('button.add-to-cart-btn')
            btn.click()
            time.sleep(3)
            assert driver.current_url == '%s/cart/' % self.live_server_url

            # check that files were added to cart and analysis_ids of them exists in table 
            for analysis_id in selected:
                checkbox = driver.find_element_by_css_selector(
                        'input[value="%s"]' % analysis_id)
            # check that other files were not added to the cart
            for analysis_id in unselected:
                assert not driver.find_elements_by_css_selector(
                            'input[value="%s"]' % analysis_id)

            stat = driver.find_element_by_xpath('//div[@class="cart-content"]//div//span')
            assert 'Files in your cart: 2' in stat.text
            cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
            assert cart_link.text == 'Cart (2)'

            # 'Select all' feature tested on search page, and it uses the same js

            # check files downloading
            try:
                os.remove(os.path.join(TEST_CACHE_DIR, 'manifest.xml'))
                os.remove(os.path.join(TEST_CACHE_DIR, 'metadata.xml'))
                os.remove(os.path.join(TEST_CACHE_DIR, 'summary.tsv'))
            except OSError:
                pass

            # download Manifest XML
            btn = driver.find_element_by_class_name('cart-download-manifest')
            btn.click()
            driver.implicitly_wait(5)
            try:
                os.remove(os.path.join(TEST_CACHE_DIR, 'manifest.xml'))
            except OSError:
                assert False, "File manifest.xml wasn't downloaded"

            # download Metadata XML
            btn = driver.find_element_by_class_name('cart-download-metadata')
            btn.click()
            driver.implicitly_wait(5)
            try:
                os.remove(os.path.join(TEST_CACHE_DIR, 'metadata.xml'))
            except OSError:
                assert False, "File metadata.xml wasn't downloaded"

            # download Summary TSV
            btn = driver.find_element_by_class_name('cart-download-summary')
            btn.click()
            driver.implicitly_wait(5)
            try:
                os.remove(os.path.join(TEST_CACHE_DIR, 'summary.tsv'))
            except OSError:
                assert False, "File summary.tsv wasn't downloaded"

            # select first file in table
            checkbox = driver.find_element_by_css_selector(
                    'input[value="%s"]' % selected[0])
            checkbox.click()

            stat = driver.find_element_by_xpath('//div[@class="cart-content"]//div//span')
            assert 'Files in your cart: {0}'.format(len(selected)) in stat.text

            cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
            assert cart_link.text == 'Cart ({0})'.format(len(selected))

            # remove seleted files
            btn = driver.find_element_by_class_name('cart-remove')
            btn.click()

            stat = driver.find_element_by_xpath('//div[@class="cart-content"]//div//span')
            assert 'Files in your cart: {0}'.format(len(selected) - 1) in stat.text

            cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
            assert cart_link.text == 'Cart ({0})'.format(len(selected) - 1)

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
