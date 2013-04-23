import time

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains

from cghub.apps.core.tests.ui_tests import TEST_SETTINGS as CORE_TEST_SETTINGS


TEST_SETTINGS = CORE_TEST_SETTINGS
TEST_SETTINGS.update({
    'HELP_HINTS': {
        'filter:Study': 'Filter by research study that generated the data set',
        'common:filters-reset-button': 'Reset the filters and search text to their default state',
        'Study:TCGA': 'The Cancer Genome Atlas',
        'Study:CCLE': 'Cancer Cell Line Encyclopedia',
        'Study:TCGA Benchmark': 'TCGA Mutation Calling Benchmark 4 (artificial data)',
        'Study': 'Research study that generated the data set',
    },
})


# TODO(nanvel): add tests for help hints and help popups here
# table headers, filters, selected filters, filters headers,
# details values, details headers, tooltips for header links,
# details table on details page


class HelpHintsTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(HelpHintsTestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(HelpHintsTestCase, self).tearDownClass()

    def get_column_number_by_name(self, name):
        counter = 0
        for col in TEST_SETTINGS['TABLE_COLUMNS']:
            if TEST_SETTINGS['COLUMN_STYLES'][col]['default_state'] == 'hidden':
                continue
            counter += 1
            if col == name:
                return counter + 1

    def test_help_hints(self):
        """
        Check that tooltip appears
        1. Go to search page (default query)
        2. Move cursor to Study header
        3. Wait
        4. Check that tooltip visible
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            ac = ActionChains(driver)
            study_header = driver.find_element_by_xpath(
                "//div[@class='hDivBox']/table/thead/tr/th[{0}]/div/a".format(
                                self.get_column_number_by_name('Study')))
            # check that no tooltips displayed
            assert not driver.find_elements_by_css_selector('.js-tooltip')
            ac.move_to_element(study_header)
            ac.perform()
            time.sleep(3)
            tooltip = driver.find_element_by_css_selector('.js-tooltip')
            assert tooltip.is_displayed()
