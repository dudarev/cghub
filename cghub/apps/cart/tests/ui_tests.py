from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class LinksNavigationsTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(LinksNavigationsTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(LinksNavigationsTests, cls).tearDownClass()
        cls.selenium.quit()

    def test_cart_link(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_partial_link_text("Cart").click()

    def test_home_link(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_partial_link_text("Home").click()

    def tes_help_link(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_partial_link_text("Help").click()

