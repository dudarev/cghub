# TODO(nanvel): add tests for help hints and help popups here

'''
class HelpHintsTestCase(LiveServerTestCase):
    # FIXME(nanvel): move this tests to apps.help.tests.ui_tests.py

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(HelpHintsTestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(HelpHintsTestCase, self).tearDownClass()

    # FIXME(nanvel): more tests for different tooltips (in table cells,
    # table headers, filters, selected filters, filters headers,
    # details values, details headers, tooltips for header links)

    def test_help_hints(self):
        """
        Check that tooltip appears
        1. Move cursor to element
        2. Wait
        3. Check that tooltip visible
        """
        with self.settings(HELP_HINTS = { 'Study': 'Help for Study'}):
            # FIXME(nanvel): use TEST_SETTINGS here
            driver = self.selenium
            driver.get(self.live_server_url)
            analysis_ids = driver.find_elements_by_xpath("//div[@class='hDivBox']/table/thead/tr/th")
            ac = ActionChains(driver)
            analysis_id = driver.find_element_by_xpath(
                "//div[@class='hDivBox']/table/thead/tr/th[{0}]/div/a".format(2))
            ac.move_to_element(analysis_id)
            ac.perform()
            time.sleep(3)
            tooltip = driver.find_element_by_css_selector('.js-tooltip')
            assert tooltip.is_displayed()
'''
