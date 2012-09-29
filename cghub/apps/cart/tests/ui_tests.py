import os
import shutil

from wsapi.settings import CACHE_DIR

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException


class LinksNavigationsTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
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

class AddItemsToCartTestCase(LiveServerTestCase):
    cache_files = [
        '0aab3523a4352c73abf8940e7c9ae7a5.xml'
    ]
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
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(AddItemsToCartTestCase, self).setUpClass()
        TEST_DATA_DIR = 'cghub/test_data/'
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        for f in self.cache_files:
            shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(CACHE_DIR, f)
            )

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(AddItemsToCartTestCase, self).tearDownClass()

    def test_cart(self):
        # Testing proper item adding
        driver = self.selenium
        driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

        for uuid in self.selected:
            checkbox = driver.find_element_by_css_selector(
                'input[value="%s"]' % uuid)
            checkbox.click()

        btn = driver.find_element_by_css_selector('button.add-to-cart-btn')
        btn.click()
        driver.implicitly_wait(1)
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
