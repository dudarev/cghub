from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


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
