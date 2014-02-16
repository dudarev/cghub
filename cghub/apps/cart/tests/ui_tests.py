import os
import time

from django.conf import settings
from django.test import LiveServerTestCase

from selenium import webdriver

from cghub.apps.core.tests.ui_tests import TEST_SETTINGS, back_to_bytes
from cghub.apps.core.attributes import COLUMN_NAMES


class AddToCartUITestCase(LiveServerTestCase):

    query = "6d50"

    @classmethod
    def setUpClass(self):
        self.selenium = webdriver.Firefox()
        self.selenium.set_window_size(1280, 800)
        self.selenium.set_window_position(0, 0)
        self.selenium.implicitly_wait(5)
        super(AddToCartUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(AddToCartUITestCase, self).tearDownClass()

    def test_add_all_to_cart(self):
        """
        Check that confirmation popup appears when trying to add
        more than settings.MANY_FILES files count.
        1. Go to search page (with q=query - 7 results)
        2. Set settings.MANY_FILES == 1
        3. Try to add all items to cart
        4. Check that confirmation popup is visible
        """
        custom_settings = dict(TEST_SETTINGS)
        custom_settings['MANY_FILES'] = 1
        with self.settings(**custom_settings):
            driver = self.selenium
            driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))
            driver.find_element_by_class_name('add-all-to-cart-btn').click()
            time.sleep(1)
            self.assertTrue(driver.find_element_by_id(
                    'manyItemsModal').is_displayed())

    def test_add_nothing_to_cart(self):
        """
        1. Go to search page
        2. Click on 'Add to cart' button
        3. Check that popup with right message is visible
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))
            driver.find_element_by_class_name('add-to-cart-btn').click()
            time.sleep(1)
            self.assertTrue(driver.find_element_by_id('messageModal').is_displayed())
            self.assertEqual(
                    driver.find_element_by_css_selector('#messageModal .modal-body').text,
                    u'Please select some files to add them to cart')


class CartUITestCase(LiveServerTestCase):

    query = "6d50"

    @classmethod
    def setUpClass(self):
        # presetup Firefox for file downloads
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", settings.FULL_METADATA_CACHE_DIR)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml,text/tsv,application/x-gzip")

        self.selenium = webdriver.Firefox(firefox_profile=fp)
        self.selenium.set_window_size(1280, 800)
        self.selenium.set_window_position(0, 0)
        self.selenium.implicitly_wait(5)
        super(CartUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(CartUITestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

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
        14. Open download manifest dropdown
        15. Try to download manifest.xml.gz
        16. Get cart stats
        17. Click 'Remove files from cart'
        18. Get cart stats, check that files count was decremented by 1
        19. Click on 'Clear cart'
        20. Check that cart is empty
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

            stat = driver.find_element_by_xpath('//span[@id="results-summary"]')
            assert 'Files in your cart: 2' in stat.text
            cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
            assert cart_link.text == 'Cart (2)'

            # 'Select all' feature tested on search page, and it uses the same js

            # check files downloading
            try:
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'manifest.xml'))
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'urls.xml'))
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'metadata.xml'))
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'summary.tsv'))
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'manifest.xml.gz'))
            except OSError:
                pass

            # download Manifest XML
            btn = driver.find_element_by_xpath('//div[@class="btn-toolbar"]/div[2]/button[1]')
            btn.click()
            driver.implicitly_wait(5)
            try:
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'manifest.xml'))
            except OSError:
                assert False, "File manifest.xml wasn't downloaded"

            # download data urls
            btn = driver.find_element_by_xpath('//div[@class="btn-toolbar"]/div[2]/button[2]')
            btn.click()
            driver.implicitly_wait(5)
            try:
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'urls.tsv'))
            except OSError:
                assert False, "File urls.tsv wasn't downloaded"

            # download Metadata XML
            btn = driver.find_element_by_xpath('//div[@class="btn-toolbar"]/div[2]/button[3]')
            btn.click()
            driver.implicitly_wait(5)
            try:
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'metadata.xml'))
            except OSError:
                assert False, "File metadata.xml wasn't downloaded"

            # download Summary TSV
            btn = driver.find_element_by_xpath('//div[@class="btn-toolbar"]/div[2]/button[4]')
            btn.click()
            driver.implicitly_wait(5)
            try:
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'summary.tsv'))
            except OSError:
                assert False, "File summary.tsv wasn't downloaded"

            # download gunzipped Manifest XML
            driver.find_element_by_xpath('//div[@class="btn-toolbar"]/div[2]/input').click()
            driver.find_element_by_xpath('//div[@class="btn-toolbar"]/div[2]/button[1]').click()
            driver.implicitly_wait(5)
            try:
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'manifest.xml.gz'))
            except OSError:
                assert False, "File manifest.xml.gz wasn't downloaded"
            driver.find_element_by_xpath('//div[@class="btn-toolbar"]/div[2]/input').click()

            # select first file in table
            checkbox = driver.find_element_by_css_selector(
                    'input[value="%s"]' % selected[0])
            checkbox.click()

            stat = driver.find_element_by_xpath('//span[@id="results-summary"]')
            assert 'Files in your cart: {0}'.format(len(selected)) in stat.text

            cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
            assert cart_link.text == 'Cart ({0})'.format(len(selected))

            # remove seleted files
            btn = driver.find_element_by_class_name('cart-remove')
            btn.click()

            time.sleep(1)

            stat = driver.find_element_by_xpath('//span[@id="results-summary"]')
            assert 'Files in your cart: {0}'.format(len(selected) - 1) in stat.text

            cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
            assert cart_link.text == 'Cart ({0})'.format(len(selected) - 1)

            # test 'clear cart' button
            btn = driver.find_element_by_class_name('cart-clear')
            btn.click()

            time.sleep(1)

            stat = driver.find_element_by_xpath('//span[@id="results-summary"]')
            assert stat.text == 'Files in your cart: 0 (0 Bytes)'

            cart_link = driver.find_element_by_xpath('//a[@href="/cart/"]')
            assert cart_link.text == 'Cart (0)'

            message = driver.find_element_by_xpath('//form[@action="/cart/action/"]//p')
            assert message.text == 'Your cart is empty!'


class SortWithinCartUITestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = webdriver.Firefox()
        self.selenium.set_window_size(1280, 800)
        self.selenium.set_window_position(0, 0)
        self.selenium.implicitly_wait(5)
        super(SortWithinCartUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(SortWithinCartUITestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def test_sort_within_cart(self):
        """
        1. Go to search page (default query)
        2. Select all files in table
        3. Click 'Add files to cart' (user will be redirected to cart page)
        4. Walk throw table columns
        5. Click on column header to select descending ordering
        6. Get top value in clumn
        7. Click on column header once more to select ascending ordering
        8. Get top value in column and compare it with previous
        9. Repeat 5..8 for every column
        """
        with self.settings(**TEST_SETTINGS):
            # go to search page
            driver = self.selenium
            driver.get(self.live_server_url)

            # add first 10 items to cart for sorting
            driver.find_element_by_css_selector('input.js-select-all').click()
            driver.find_element_by_css_selector('button.add-to-cart-btn').click()
            time.sleep(3)

            for i, column in enumerate(TEST_SETTINGS['TABLE_COLUMNS']):
                # walk over all visible table columns
                if TEST_SETTINGS['COLUMN_STYLES'][column]['default_state'] == 'hidden':
                    continue
                if column == 'Sample Type':
                    continue
                attr = COLUMN_NAMES[column]
                # scroll table
                self.selenium.execute_script("$('.bDiv')"
                        ".scrollLeft($('th[axis=col{0}]')"
                        ".position().left);".format(i + 2))
                # after first click element element is asc sorted
                self.selenium.find_element_by_partial_link_text(column).click()

                # getting top element in the column
                selector = "//div[@class='bDiv']/fieldset/table/tbody/tr[1]/td[{}]".format(i + 3)
                first = self.selenium.find_element_by_xpath(selector).text

                # scroll table
                self.selenium.execute_script("$('.bDiv')"
                        ".scrollLeft($('th[axis=col{0}]')"
                        ".position().left);".format(i + 2))
                # resort
                self.selenium.find_element_by_partial_link_text(column).click()
                second = self.selenium.find_element_by_xpath(selector).text

                if not (first == 'None' or second == 'None' or
                        first == ' ' or second == ' '):
                    if column == 'Files Size':
                        # GB == GB, MB == MB, etc.
                        first = back_to_bytes(first)
                        second = back_to_bytes(second)
                        self.assertLessEqual(first, second)
                    else:
                        self.assertLessEqual(first, second)
