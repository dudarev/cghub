import math
import os
import time

from datetime import datetime, date, timedelta
from urllib2 import unquote

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase

from cghub.apps.help.models import HelpText

from ..filters_storage import ALL_FILTERS
from ..attributes import DATE_ATTRIBUTES, COLUMN_NAMES
from .tests import create_session


TEST_SETTINGS = dict(
    TABLE_COLUMNS=(
        'Analysis Id',
        'Study',
        'State',
        'Disease',
        'Sample Type',
        'Experiment Type',
        'Library Type',
        'Center',
        'Center Name',
        'Assembly',
        'Files Size',
        'Uploaded',
        'Modified',
    ),
    DETAILS_FIELDS=(
        'Study',
        'Barcode',
        'Disease',
        'Disease Name',
        'Sample Type',
        'Sample Type Name',
        'Experiment Type',
        'Library Type',
        'Center',
        'Center Name',
        'Platform',
        'Platform Name',
        'Assembly',
        'Files Size',
        'Analysis Id',
        'Sample Accession',
        'Uploaded',
        'Modified',
        'State',
        'Aliquot id',
        'TSS id',
        'Participant id',
        'Sample id',
    ),
    COLUMN_STYLES={
        'Analysis Id': {
            'width': 220, 'align': 'left', 'default_state': 'visible',
        },
        'Assembly': {
            'width': 120, 'align': 'left', 'default_state': 'visible',
        },
        'Center': {
            'width': 100, 'align': 'left', 'default_state': 'visible',
        },
        'Center Name': {
            'width': 100, 'align': 'left', 'default_state': 'hidden',
        },
        'Checksum': {
            'width': 250, 'align': 'left', 'default_state': 'hidden',
        },
        'Disease': {
            'width': 65, 'align': 'left', 'default_state': 'visible',
        },
        'Experiment Type': {
            'width': 95, 'align': 'left', 'default_state': 'hidden',
        },
        'Filename': {
            'width': 300, 'align': 'left', 'default_state': 'hidden',
        },
        'Files Size': {
            'width': 75, 'align': 'right', 'default_state': 'visible',
        },
        'Library Type': {
            'width': 100, 'align': 'left', 'default_state': 'visible',
        },
        'Modified': {
            'width': 80, 'align': 'left', 'default_state': 'visible',
        },
        'Sample Type': {
            'width': 75, 'align': 'left', 'default_state': 'visible',
        },
        'State': {
            'width': 70, 'align': 'left', 'default_state': 'visible',
        },
        'Study': {
            'width': 100, 'align': 'left', 'default_state': 'visible',
        },
        'Uploaded': {
            'width': 80, 'align': 'left', 'default_state': 'hidden',
        },
    },
    DEFAULT_FILTERS={
        'study': ('phs000178', '*Other_Sequencing_Multiisolate'),
        'state': ('live',),
    },
)

def back_to_bytes(size_str):
    """
    Converts File Size back to bytes for comparing purposes.

    :param size_str: '10.11 GB', for example
    """
    float_result = float(size_str.split(' ')[0].replace(',', '.'))
    if size_str.endswith('GB'):
        return float_result * 1073741824.
    elif size_str.endswith('MB'):
        return float_result * 1048576.
    elif size_str.endswith('KB'):
        return float_result * 1024.
    return 0


def scroll_page_to_filter(driver, f):
    """
    Scroll page to element (makes it visible fo user).
    """
    driver.execute_script(
        "$(window).scrollTop($('#ddcl-id-{0}').offset().top - 100);".format(f))


class CoreUITestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        # http://selenium-python.readthedocs.org/en/latest/api.html#selenium.webdriver.remote.webdriver.implicitly_wait
        self.selenium.implicitly_wait(5)
        super(CoreUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(CoreUITestCase, self).tearDownClass()

    def test_access_without_trailing_slash(self):
        """
        Access application without trailing slash in URL.
        I.E. "https://stage-browser.cghub.ucsc.edu/search"
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            # default self.live_server_url == 'http://localhost:8081'
            driver.get('%s/search' % self.live_server_url)
            assert driver.find_elements_by_css_selector('.applied-filters')

    def test_search_field(self):
        """
        Entering a search term and hitting enter leads to correct page.
        Check it on search, cart and help pages.
        1. Go to search page
        2. Enter query with '*' or '?'
        3. Sumit
        4. Check that popup visible
        5. Close popup
        6. Enter query, submit
        7. Check for 'search' and 'q' in url
        8. Check that search box is empty
        9. Go to cart page
        10. Repeat 2-7
        11. Go to help page
        12. Repeat 2-7
        """
        def check_good_query(key='123'):
            driver = self.selenium
            search_field = driver.find_element_by_css_selector(
                    '.navbar-search .search-query')
            search_field.clear()
            search_field.send_keys(key)
            search_field.submit()
            time.sleep(3)
            assert 'search' in driver.current_url
            assert 'q=%s' % key in driver.current_url
            # check searchbox is empty
            search_field = driver.find_element_by_css_selector(
                    '.navbar-search .search-query')
            self.assertEqual(search_field.get_attribute('value'), '')

        def check_bad_query(key='bad*'):
            """
            Check use of unsupported metaseach characters in text box.
            """
            driver = self.selenium
            # check popup invisible
            popup = driver.find_element_by_id('messageModal')
            assert not popup.is_displayed()
            search_field = driver.find_element_by_css_selector(
                    '.navbar-search .search-query')
            search_field.clear()
            search_field.send_keys(key)
            search_field.submit()
            # check popup visible
            time.sleep(1)
            assert popup.is_displayed()
            popup.find_element_by_css_selector(".modal-header .close").click()
            time.sleep(1)

        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            for page in ('search', 'cart', 'search/batch', 'help', 'accessibility'):
                driver.get('%s/%s/' % (self.live_server_url, page))
                assert 'q=' not in driver.current_url
                check_bad_query()
                check_good_query()

    def test_messages(self):
        """
        1. Add 2 messages
        2. Go to home page
        3. Check that 2 messages are displayed
        4. Click on close button
        5. Check that only one message displayed
        6. Reload page
        7. Check that only one message displayed
        """
        with self.settings(**TEST_SETTINGS):
            # initialize browser
            self.selenium.get(self.live_server_url)
            time.sleep(3)
            # create messages
            create_session(self)
            self.session['messages'] = {
                1: {'level': 'error', 'content': 'Some error!'},
                2: {'level': 'info', 'content': 'All ok!'}}
            self.session.save()
            self.selenium.add_cookie({
                'name': settings.SESSION_COOKIE_NAME,
                'value': self.session.session_key})
            self.selenium.get(self.live_server_url)
            time.sleep(3)
            self.assertEqual(
                    len(self.selenium.find_elements_by_xpath(
                            '//div[@class="messages"]/div')),
                    2)            
            # close first message
            self.selenium.find_element_by_xpath(
                            '//div[@class="messages"]/div[1]/button').click()
            time.sleep(1)
            self.assertEqual(
                    len(self.selenium.find_elements_by_xpath(
                            '//div[@class="messages"]/div')),
                    1)
            # reload page
            self.selenium.get(self.live_server_url)
            time.sleep(3)
            self.assertEqual(
                    len(self.selenium.find_elements_by_xpath(
                            '//div[@class="messages"]/div')),
                    1)


class NavigationLinksUITestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = webdriver.Firefox()
        self.selenium.implicitly_wait(5)
        super(NavigationLinksUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(NavigationLinksUITestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def test_links(self):
        """
        1. Go to search page (default query)
        2. Click on 'Cart' link
        3. Check url
        4. Click on 'Batch search' link
        5. Check url
        6. Click on 'Help' link
        7. Check url
        8. Click on 'Accessibility' link
        9. Check url
        10. Clcik on 'Browser' link
        11. Check url
        """
        driver = self.selenium
        with self.settings(**TEST_SETTINGS):
            # search page
            driver.get(self.live_server_url)
            assert '/cart/' not in driver.current_url
            assert '/search/batch/' not in driver.current_url
            assert '/help/' not in driver.current_url
            assert '/accessibility/' not in driver.current_url
            # go to cart page
            driver.find_element_by_partial_link_text('Cart').click()
            time.sleep(3)
            assert '/cart/' in driver.current_url
            # got to batch search
            driver.find_element_by_partial_link_text('Batch search').click()
            time.sleep(3)
            assert '/search/batch/' in driver.current_url
            # go to help page
            driver.find_element_by_partial_link_text('Help').click()
            time.sleep(3)
            assert '/help/' in driver.current_url
            # got to accessibility page
            driver.find_element_by_partial_link_text('Accessibility').click()
            time.sleep(3)
            assert '/accessibility/' in driver.current_url
            # got back to search page
            driver.find_element_by_partial_link_text('Browser').click()
            time.sleep(3)
            assert '/cart/' not in driver.current_url
            assert '/search/batch/' not in driver.current_url
            assert '/help/' not in driver.current_url
            assert '/accessibility/' not in driver.current_url


class SidebarUITestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SidebarUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(SidebarUITestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def test_select_all(self):
        """
        1. Open 'By Center' filter (Selected all items by default)
        2. Click on '(Toggle all)'
        3. Check that all checkboxes unchecked
        4. Click on '(Toggle all)'
        5. Check that all checkboxes checked
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)

            self.selenium.find_element_by_id("ddcl-id-center_name").click()

            # get centers count
            centers_count = len(ALL_FILTERS['center_name']['filters'])
            # by center has <centers_count> centers, i0 - deselect all, i1-i<centers_count> - selections
            # click on 'All' to deselect all and check that no one selected
            driver.find_element_by_id("ddcl-id-center_name-i0").click()
            for i in range(1, centers_count + 1):
                cb = driver.find_element_by_id("ddcl-id-center_name-i{0}".format(i))
                self.assertFalse(cb.is_selected())

            # click again - select all
            # check that all centers selected
            driver.find_element_by_id("ddcl-id-center_name-i0").click()
            for i in range(1, centers_count + 1):
                cb = driver.find_element_by_id("ddcl-id-center_name-i{0}".format(i))
                self.assertTrue(cb.is_selected())

    def test_select_date(self):
        """
        1. Open 'By Modification Date' filter
        2. Select 'Any date' option
        3. Check that other options unchecked
        4. Click on 'Today' option
        5. Check that other unchecked
        6. Open 'By Upload Date' filter
        7. Go To 2
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            driver.find_element_by_css_selector("span.ui-dropdownchecklist-text").click()

            # Open 'By Modification Date' filter
            driver.find_element_by_xpath(
                "//span[@id='ddcl-id-last_modified']/span/span").click()

            # click the first selection
            i_click = 0
            driver.find_element_by_id("ddcl-id-last_modified-i{0}".format(i_click)).click()
            # check that other options are unselected
            for i in range(0, 5):
                if not i == i_click:
                    rb = driver.find_element_by_id("ddcl-id-last_modified-i{0}".format(i))
                    self.assertFalse(rb.is_selected())

            # click on first option
            i_click = 1
            driver.find_element_by_id("ddcl-id-last_modified-i{0}".format(i_click)).click()
            # check that other options unselected
            for i in range(0, 5):
                if not i == i_click:
                    rb = driver.find_element_by_id("ddcl-id-last_modified-i{0}".format(i))
                    self.assertFalse(rb.is_selected())

            # open 'By Upload Date' filter
            driver.find_element_by_xpath(
                "//span[@id='ddcl-id-upload_date']/span/span").click()

            # select first option
            z_click = 0
            driver.find_element_by_id("ddcl-id-upload_date-i{0}".format(z_click)).click()
            # check that other options are unselected
            for i in range(0, 5):
                if not i == z_click:
                    rb = driver.find_element_by_id("ddcl-id-upload_date-i{0}".format(i))
                    self.assertFalse(rb.is_selected())

            # select second option
            z_click = 1
            driver.find_element_by_id("ddcl-id-upload_date-i{0}".format(z_click)).click()
            # check that other options are unselected
            for i in range(0, 5):
                if not i == z_click:
                    rb = driver.find_element_by_id("ddcl-id-upload_date-i{0}".format(i))
                    self.assertFalse(rb.is_selected())

    def test_selection(self):
        """
        1. Walk over filters from filters_storage.
        2. Open every filter and select few items.
        3. Click on 'Apply filters'
        4. Check that only selected filters options exists in url
        5. Check 'Applied filter(s):' list
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            unselected_options = []
            selected_options_values = {}
            selected_options_ids = {}

            # create list of options to select
            for f in ALL_FILTERS:
                options = ALL_FILTERS[f]['filters']
                if f in DATE_ATTRIBUTES:
                    # select second option (Today - '[NOW-1DAY+TO+NOW]')
                    selected_options_ids[f] = [1]
                    selected_options_values[f] = ['[NOW-1DAY+TO+NOW]']
                elif len(options) > 3:
                    # select first 3 items
                    selected_options_ids[f] = [1, 2, 3]
                    selected_options_values[f] = []
                    for i in options:
                        selected_options_values[f].append(i)
                        if len(selected_options_values[f]) > 2:
                            break
                else:
                    # select select first item
                    selected_options_ids[f] = [1]
                    for i in options:
                        selected_options_values[f] = [i]
                        break
            # create list of unselected options:
            for f in ALL_FILTERS:
                for i in ALL_FILTERS[f]['filters']:
                    if i not in selected_options_values[f]:
                        unselected_options.append(i)

            # select filters options
            for f in selected_options_values:
                # open filter DDCL
                scroll_page_to_filter(driver, f)
                self.selenium.find_element_by_css_selector(
                        "#ddcl-id-{0} > span:first-child > span".format(f)).click()
                # if some items selected by default, select all
                if f in TEST_SETTINGS['DEFAULT_FILTERS']:
                    driver.find_element_by_id("ddcl-id-{0}-i0".format(f)).click()
                # unselect all
                driver.find_element_by_id("ddcl-id-{0}-i0".format(f)).click()
                # select necessary options
                for i in selected_options_ids[f]:
                    driver.find_element_by_id("ddcl-id-{0}-i{1}".format(f, i)).click()
                # and close filter DDCL
                self.selenium.find_element_by_css_selector(
                        "#ddcl-id-{0} > span:last-child > span".format(f)).click()

            # submit form
            driver.find_element_by_id("id_apply_filters").click()
            url = unquote(driver.current_url)

            # check that all selected filters options exists in url
            for f in selected_options_values:
                options = selected_options_values[f]
                for option in options:
                    self.assertIn(option.replace(' ', '+'), url)

            # check that no unselected options in url
            for option in unselected_options:
                self.assertNotIn('(%s+' % option, url)
                self.assertNotIn('+%s+' % option, url)
                self.assertNotIn('+%s)' % option, url)
                self.assertNotIn('(%s)' % option, url)

            # check that applied filters exists in 'Applied filter(s)' list
            applied_filters = self.selenium.find_element_by_xpath(
                                    "//div[@class='applied-filters']/ul").text
            for f in selected_options_values:
                if f in DATE_ATTRIBUTES:
                    return
                options = selected_options_values[f]
                for option in options:
                    self.assertIn(option, applied_filters)
            for option in unselected_options:
                self.assertIn(option, applied_filters)


class CustomPeriodUITestCase(LiveServerTestCase):

    year = date.today().year
    TEST_DATES = (
        {
            'start': date(year, 2, 10),
            'end': date(year, 2, 15),
            'res_start': date(year, 2, 10),
            'res_end': date(year, 2, 15)},
        {
            # another month
            'start': date(year, 1, 10),
            'end': date(year, 3, 15),
            'res_start': date(year, 1, 10),
            'res_end': date(year, 3, 15)},
        {
            # today
            'start': date(year, 2, 10),
            'end': date(year, 2, 10),
            'res_start': date(year, 2, 9),
            'res_end': date(year, 2, 10)},
        {
            # future
            'start': date(year, 2, 10),
            'end': date.today() + timedelta(days=10),
            'res_start': date(year, 2, 10),
            'res_end': date.today()},
        {
            # swapped
            'start': date(year, 2, 15),
            'end': date(year, 2, 10),
            'res_start': date(year, 2, 10),
            'res_end': date(year, 2, 15)},
    )

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(CustomPeriodUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(CustomPeriodUITestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def set_datepicker_date(self, start, end):
        """
        Select start and end dates in custom period popup

        :param start: start date (datetime.date object)
        :param end: end date (datetime.date object)
        """
        driver = self.selenium
        dp_start = driver.find_element_by_id('dp-start')
        dp_end = driver.find_element_by_id('dp-end')
        # set year
        dp_start.find_element_by_css_selector('.ui-datepicker-year').click()
        dp_start.find_element_by_css_selector("option[value='{0}']".format(start.year)).click()
        dp_end.find_element_by_css_selector('.ui-datepicker-year').click()
        dp_end.find_element_by_css_selector("option[value='{0}']".format(end.year)).click()
        # set month
        dp_start.find_element_by_css_selector('.ui-datepicker-month').click()
        dp_start.find_element_by_css_selector("option[value='{0}']".format(start.month - 1)).click()
        dp_end.find_element_by_css_selector('.ui-datepicker-month').click()
        dp_end.find_element_by_css_selector("option[value='{0}']".format(end.month - 1)).click()
        # set days
        dp_start.find_element_by_link_text("{}".format(start.day)).click()
        dp_end.find_element_by_link_text("{}".format(end.day)).click()

    def check_custom_date(self, filter_name, start, end):
        """
        Check that right date displayed in specified date filter.

        :param filter_name: 'last_modified' or 'upload_date'
        :param start: start date (datetime.date object)
        :param end: end date (datetime.date object)
        """
        driver = self.selenium

        # Check custom date is displayed in filter input
        filter_input = driver.find_element_by_id("ddcl-id-{0}".format(filter_name))
        filter_text = filter_input.find_element_by_css_selector(
                                    '.ui-dropdownchecklist-text').text
        text = "{0} - {1}".format(
                        datetime.strftime(start, '%Y/%m/%d'),
                        datetime.strftime(end, '%Y/%m/%d'))
        assert text in filter_text.strip()

    def test_custom_upload_date(self):
        """
        1. Open 'By Upload Date' filter
        2. Click on 'Custom period' button
        3. Check that custom period popup visible
        4. Click 'Cancel', check that popup closed
        5. Open filter, click 'Custom period'
        6. Select period
        7. Clcik 'Submit'
        8. Check that displayed right period as filter value
        9. Repeat 5-8 for different periods (TEST_DATES)
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            # scroll to 'By Upload Date' filter
            scroll_page_to_filter(driver, 'upload_date')

            # check popup displayed and cancel button works
            self.assertFalse(driver.find_elements_by_css_selector('.dp-container'))
            driver.find_element_by_id("ddcl-id-upload_date").click()
            driver.find_element_by_css_selector(
                        '#ddcl-id-upload_date-ddw .js-pick-period').click()
            # check that popup is visible
            self.assertTrue(driver.find_element_by_css_selector('.dp-container').is_displayed())
            # click 'Cancel'
            driver.find_element_by_css_selector('button.btn-cancel.btn').click()
            self.assertFalse(driver.find_elements_by_css_selector('.dp-container'))

            # check different periods submit
            for dates in self.TEST_DATES:
                # select period
                driver.find_element_by_id("ddcl-id-upload_date").click()
                driver.find_element_by_css_selector(
                        '#ddcl-id-upload_date-ddw .js-pick-period').click()
                self.set_datepicker_date(dates['start'], dates['end'])
                # click 'Submin' in custom period popup
                driver.find_element_by_css_selector("button.btn-submit.btn").click()
                # check that displayed right period
                self.check_custom_date('upload_date', dates['res_start'], dates['res_end'])

    def test_custom_last_modified(self):
        """
        1. Open 'By Modification Date' filter
        2. Click on 'Custom period' button
        3. Select period
        4. Clcik 'Submit'
        5. Check that displayed right period as filter value
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            # scroll to 'By Modification Date' filter
            scroll_page_to_filter(driver, 'last_modified')

            dates = self.TEST_DATES[0]
            # select period
            driver.find_element_by_id("ddcl-id-last_modified").click()
            driver.find_element_by_css_selector(
                        '#ddcl-id-last_modified-ddw .js-pick-period').click()
            self.set_datepicker_date(dates['start'], dates['end'])
            # click 'Submin' in custom period popup
            driver.find_element_by_css_selector("button.btn-submit.btn").click()
            # check that displayed right period
            self.check_custom_date('last_modified', dates['res_start'], dates['res_end'])


class DetailsUITestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference(
                "browser.download.manager.showWhenStarting", False)
        fp.set_preference(
                "browser.download.dir", settings.FULL_METADATA_CACHE_DIR)
        fp.set_preference(
                "browser.helperApps.neverAsk.saveToDisk", "text/xml")
        self.selenium = webdriver.Firefox(firefox_profile=fp)
        self.selenium.implicitly_wait(5)
        super(DetailsUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(DetailsUITestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def check_popup_shows(self):
        """
        Check that details popup appears when clicking on table cell or
        when select related item in table cell context menu.
        1. Check that details popup invisible
        2. Click on table cell
        3. Check that popup visible
        4. Click on 'Close' button in popup
        5. Check that popup invisible
        6. Open table cell context menu
        7. Check that details button exists in context menu
        """
        driver = self.selenium
        ac = ActionChains(driver)
        # check that popup not displayed yet
        popup = driver.find_element_by_css_selector('#itemDetailsModal')
        assert not popup.is_displayed()
        # click on table cell
        td = driver.find_element_by_xpath(
                    "//div[@class='bDiv']/fieldset/table/tbody/tr[1]/td[2]")
        td.click()
        # analysis_id consist in first column
        uuid = driver.find_element_by_xpath(
                    "//div[@class='bDiv']/fieldset/table/tbody/tr[1]").get_attribute('data-analysis_id')
        time.sleep(3)
        # check that popup displayed
        assert popup.is_displayed()
        assert uuid in driver.find_element_by_css_selector('#details-label').text
        # close popup
        driver.find_element_by_xpath("//button[@data-dismiss='modal']").click()
        time.sleep(1)
        assert not popup.is_displayed()
        # check context menu
        context_menu = driver.find_element_by_css_selector('#table-context-menu')
        assert not context_menu.is_displayed()
        ac.context_click(td)
        ac.perform()
        # check that context menu is visible
        assert context_menu.is_displayed()
        # check that details popup button visible
        assert driver.find_element_by_css_selector('.js-details-popup').is_displayed()

    def test_details_popups(self):
        """
        Check that details popup shows on search and cart page.
        1. Go to search page
        2. Check that popup shows (using check_popup_shows) on search page
        3. Check first checkbox in table
        4. Click 'Add to cart' button
        5. Check that popups shows on cart page
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            self.check_popup_shows()
            # add one file to cart (then user will be redirected to cart page)
            driver.find_element_by_xpath(
                    "//div[@class='bDiv']/fieldset/table/tbody/tr[1]/td[1]/div/input"
                    ).click()
            driver.find_element_by_css_selector('.add-to-cart-btn').click()
            time.sleep(5)
            self.check_popup_shows()

    def test_xml_display(self):
        """
        Go to details page and check 'Collapse all/Expand all' feature.
        1. Go to search page
        2. Click on link to item details page (cell context menu)
        3. Check that url contains #raw-xml
        4. Check that collapse/expand future works properly
        """
        with self.settings(**TEST_SETTINGS):
            # FIXME(nanvel): extend description ^
            driver = self.selenium
            driver.get(self.live_server_url)
            # Click on 'Metadata XML' in details popup
            td = driver.find_element_by_xpath(
                    "//div[@class='bDiv']/fieldset/table/tbody/tr[1]/td[2]")
            td.click()
            time.sleep(3)
            driver.find_element_by_css_selector('.raw-xml-link').click()
            time.sleep(3)
            assert '#raw-xml' in driver.current_url

            # test 'Collapse all' and 'Expand all' buttons
            driver.find_element_by_css_selector('#id-expand-all-button').click()
            xml_containers = driver.find_elements_by_css_selector('#XMLHolder > .Element')
            collapsed_xml = xml_containers[0].find_elements_by_class_name('Element')
            expanded_xml = xml_containers[1].find_elements_by_class_name('Element')
            assert len(expanded_xml) > len(collapsed_xml)
            assert not xml_containers[0].is_displayed()
            assert xml_containers[1].is_displayed()
            driver.find_element_by_css_selector('#id-collapse-all-button').click()
            assert xml_containers[0].is_displayed()
            assert not xml_containers[1].is_displayed()

    def test_details_page(self):
        """
        Go to details page and try to download metadata.
        1. Remove downloaded metadata.xml if exists
        2. Open row context menu and click 'Show details in new window'
        3. Click on 'Download XML' button
        4. Check that file downloaded
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            # remove saved metadata file if exists
            try:
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'metadata.xml'))
            except OSError:
                pass
            td = driver.find_element_by_xpath(
                    "//div[@class='bDiv']/fieldset/table/tbody/tr[1]/td[2]")
            analysis_id = driver.find_element_by_xpath(
                    "//div[@class='bDiv']/fieldset/table/tbody/tr[1]").get_attribute('data-analysis_id')
            # open row context menu and click 'Show details in new window'
            ac = ActionChains(driver)
            ac.context_click(td)
            ac.perform()
            driver.find_element_by_css_selector('.js-details-page').click()
            time.sleep(5)
            driver.switch_to_window(driver.window_handles[-1])
            page_header = driver.find_element_by_class_name('page-header').text
            assert (analysis_id in driver.current_url and 'details' in driver.current_url)
            assert (analysis_id in page_header and 'details' in page_header)
            # scroll page to Metadata download button (make it visible)
            driver.execute_script(
                "$(window).scrollTop($('#id-download-metadata').offset().top - 100);")
            # try to download analysis xml
            driver.find_element_by_id('id-download-metadata').click()
            time.sleep(3)
            # check that metadata file was downloaded
            try:
                os.remove(os.path.join(
                        settings.FULL_METADATA_CACHE_DIR,
                        'metadata.xml'))
            except OSError:
                assert False, "File metadata.xml wasn't downloaded"


class SearchUITestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SearchUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(SearchUITestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def test_no_results(self):
        """
        Enter bad query, submit, check that no results was found.
        1. Go to search page
        2. Enter query ('some text')
        3. Submit form
        4. Check that 'No results found.' displayed
        """
        with self.settings(**TEST_SETTINGS):
            self.selenium.get(self.live_server_url)
            element = self.selenium.find_element_by_name("q")
            element.clear()
            element.send_keys("some text")
            element.submit()
            time.sleep(3)
            result = self.selenium.find_element_by_xpath(
                "//div[contains(@class,'base-container')]/div/h4")
            assert result.text == "No results found."

    def test_filters_state_is_persistent(self):
        """
        1. Go to search page (used default query)
        2. Check that selected 'All' for center filter
        3. Check that first center name not exists in url
        4. Select first center
        5. Apply filters
        6. Check that first center name exists in url
        7. Check that first center selected
        8. Go to cart page
        9. Go to search page
        10. Check that first center selected
        11. Check that first center name not exists in url
        """
        with self.settings(**TEST_SETTINGS):
            self.selenium.get(self.live_server_url)
            time.sleep(3)
            filter_name = 'center_name'
            filter_object = ALL_FILTERS[filter_name]
            options = filter_object['filters']
            self.assertTrue(len(options) > 1)
            self.assertNotIn(filter_name, TEST_SETTINGS['DEFAULT_FILTERS'])
            # select first center
            scroll_page_to_filter(self.selenium, filter_name)
            self.selenium.find_element_by_css_selector(
                    "#ddcl-id-{0} > span:first-child > span".format(filter_name)).click()
            # unselect all
            self.selenium.find_element_by_id(
                    "ddcl-id-{0}-i{1}".format(filter_name, 0)).click()
            option_name = self.selenium.find_element_by_xpath(
                    "//label[@for='ddcl-id-{0}-i{1}']".format(filter_name, 1)).text
            option_attribute = None
            for key, value in options.iteritems():
                if value == option_name:
                    option_attribute = key
                    break
            self.assertTrue(option_attribute)
            # check url
            url = unquote(self.selenium.current_url)
            self.assertNotIn(option_attribute, url)
            # check selected options
            self.assertNotIn(
                    option_name,
                    self.selenium.find_element_by_id(
                            "id-{0}-ui-selector".format(filter_name)).text)
            # select first filter
            self.selenium.find_element_by_id(
                    "ddcl-id-{0}-i{1}".format(filter_name, 1)).click()
            # and close filter DDCL
            self.selenium.find_element_by_css_selector(
                    "#ddcl-id-{0} > span:last-child > span".format(filter_name)).click()
            # check selected options
            self.assertIn(
                    option_name,
                    self.selenium.find_element_by_id(
                            "id-{0}-ui-selector".format(filter_name)).text)
            # submit form
            self.selenium.find_element_by_id("id_apply_filters").click()
            # check url
            url = unquote(self.selenium.current_url)
            self.assertIn(option_attribute, url)
            # Go to cart page and back
            self.selenium.get(self.live_server_url + reverse('cart_page'))
            time.sleep(1)
            self.selenium.get(self.live_server_url)
            time.sleep(2)
            # check url
            url = unquote(self.selenium.current_url)
            self.assertNotIn(option_attribute, url)
            # check selected options
            self.assertIn(
                    option_name,
                    self.selenium.find_element_by_id(
                            "id-{0}-ui-selector".format(filter_name)).text)

    def test_save_last_query(self):
        """
        1. Go to home page (query by default)
        2. Unselect default filters
        3. Apply filters
        4. Go to home page
        5. Check that no filters applied
        6. Select one filter option
        7. Apply filters
        8. Go to home page
        9. Check that filter is applied
        """
        with self.settings(**TEST_SETTINGS):
            self.selenium.get(self.live_server_url)
            time.sleep(3)
            url = unquote(self.selenium.current_url)
            self.assertFalse(url.endswith(reverse('search_page')))
            self.assertNotIn(
                    'No applied filters',
                    self.selenium.find_element_by_xpath(
                            '//div[@class="applied-filters"]').text)
            # unselect default filters
            for f in TEST_SETTINGS['DEFAULT_FILTERS']:
                scroll_page_to_filter(self.selenium, f)
                self.selenium.find_element_by_css_selector(
                        "#ddcl-id-{0} > span:first-child > span".format(f)).click()
                # select all
                self.selenium.find_element_by_id(
                        "ddcl-id-{0}-i{1}".format(f, 0)).click()
                # close filter DDCL
                self.selenium.find_element_by_css_selector(
                        "#ddcl-id-{0} > span:last-child > span".format(f)).click()
            # submit form
            self.selenium.find_element_by_id("id_apply_filters").click()
            time.sleep(2)
            url = unquote(self.selenium.current_url)
            self.assertTrue(url.endswith(reverse('search_page')))
            self.assertIn(
                    'No applied filters',
                    self.selenium.find_element_by_xpath(
                            '//div[@class="applied-filters"]').text)
            # go to home page, check that filters are the same
            self.selenium.get(self.live_server_url)
            time.sleep(3)
            self.assertTrue(url.endswith(reverse('search_page')))
            self.assertIn(
                    'No applied filters',
                    self.selenium.find_element_by_xpath(
                            '//div[@class="applied-filters"]').text)
            # select one option in center_name filter
            filter_name = 'center_name'
            filter_object = ALL_FILTERS[filter_name]
            options = filter_object['filters']
            self.assertTrue(len(options) > 1)
            # select first option
            scroll_page_to_filter(self.selenium, filter_name)
            self.selenium.find_element_by_css_selector(
                    "#ddcl-id-{0} > span:first-child > span".format(filter_name)).click()
            # unselect all
            self.selenium.find_element_by_id(
                    "ddcl-id-{0}-i{1}".format(filter_name, 0)).click()
            option_name = self.selenium.find_element_by_xpath(
                    "//label[@for='ddcl-id-{0}-i{1}']".format(filter_name, 1)).text
            self.selenium.find_element_by_id(
                    "ddcl-id-{0}-i{1}".format(filter_name, 1)).click()
            # and close filter DDCL
            self.selenium.find_element_by_css_selector(
                    "#ddcl-id-{0} > span:last-child > span".format(filter_name)).click()
            self.assertNotIn(
                    option_name,
                    self.selenium.find_element_by_xpath(
                            '//div[@class="applied-filters"]').text)
            # submit form
            self.selenium.find_element_by_id("id_apply_filters").click()
            time.sleep(2)
            self.assertIn(
                    option_name,
                    self.selenium.find_element_by_xpath(
                            '//div[@class="applied-filters"]').text)
            # go to home page
            self.selenium.get(self.live_server_url)
            time.sleep(3)
            self.assertIn(
                    option_name,
                    self.selenium.find_element_by_xpath(
                            '//div[@class="applied-filters"]').text)

    def test_search_result(self):
        """
        Check results exists if right query entered.
        1. Go to search page (used default query)
        3. Check that results exists
        4. Check that table displayed
        """
        with self.settings(**TEST_SETTINGS):
            self.selenium.get(self.live_server_url)
            time.sleep(3)
            assert "Found" in self.selenium.find_element_by_xpath(
                        "//section[@id='results-summary']/div[1]").text
            # check that table displayed
            assert self.selenium.find_element_by_id('id_add_files_form')

    def test_count_pages(self):
        """
        Check 10, 25, 50 items per page links.
        1. Go to search page (with more than 50 results)
        2. Check that 10 rows in table
        3. Click 25
        4. Check that 25 rows in table
        5. Click 50
        6. Check that 50 rows in table
        """
        with self.settings(**TEST_SETTINGS):
            self.selenium.get(self.live_server_url)
            time.sleep(3)
            assert 10 == len(self.selenium.find_elements_by_xpath(
                        "//div[@class='bDiv']/fieldset/table/tbody/tr"))
            self.selenium.find_element_by_xpath(
                        "//div[@class='items-per-page-label']"
                        "//a[contains(text(), '25')]").click()
            assert 25 == len(self.selenium.find_elements_by_xpath(
                        "//div[@class='bDiv']/fieldset/table/tbody/tr"))
            self.selenium.find_element_by_xpath(
                        "//div[@class='items-per-page-label']"
                        "//a[contains(text(), '50')]").click()
            assert 50 == len(self.selenium.find_elements_by_xpath(
                        "//div[@class='bDiv']/fieldset/table/tbody/tr"))

    def test_pagination(self):
        """
        Check that pagination works.
        1. Go to search page
        2. Check that results exists
        3. Check that no offset in url
        4. Check that first page and 'Prev' links disabled
        5. Find link to second page in pagination and click it
        6. Check that table filled
        7. Check that url contains offset and limit
        8. Go throw few pages to last page
        9. Check that current page link disabled
        10. Click 'Prev'
        11. Check that pages_count - 1 page selected
        """

        def link_state(link):
            """
            Returns True if link is active
            """
            parent = link.find_element_by_xpath("..")
            # disabled buttons Next and Prev and
            # active page button counts disabled
            return not parent.get_attribute('class') in ('disabled', 'active',)

        with self.settings(**TEST_SETTINGS):
            self.selenium.get(self.live_server_url)
            time.sleep(3)

            # check that results exists
            assert 10 == len(self.selenium.find_elements_by_xpath(
                    "//div[@class='bDiv']/fieldset/table/tbody/tr"))
            assert 'offset' not in self.selenium.current_url

            # initially 'Prev' and '1' links should be disabled
            prev = self.selenium.find_element_by_partial_link_text('Prev')
            assert not link_state(prev)
            first = self.selenium.find_element_by_xpath(
                    '//div[@class="pagination-centered"]/ul/li[2]/a')
            assert not link_state(first)

            # got to second page
            self.selenium.find_element_by_xpath(
                    '//div[@class="pagination-centered"]/ul/li[3]/a').click()
            assert 10 == len(self.selenium.find_elements_by_xpath(
                    "//div[@class='bDiv']/fieldset/table/tbody/tr"))
            # check that url contains offset and limit
            assert 'offset=10&limit=10' in self.selenium.current_url

            found = self.selenium.find_element_by_xpath(
                                    "//section[@id='results-summary']/div[1]")
            pages_count = math.ceil(1.0 * int(found.text.split()[1]) / 10)

            # check 'Prev'
            self.selenium.find_element_by_xpath(
                        "//div[@class='pagination-centered']"
                        "//a[contains(text(), %s)]" % str(pages_count)).click()
            self.selenium.find_element_by_xpath(
                        "//div[@class='pagination-centered']"
                        "//a[contains(text(), 'Prev')]").click()
            current = self.selenium.find_element_by_xpath(
                        "//div[@class='pagination-centered']"
                        "//a[contains(text(), %s)]" % str(pages_count - 1))
            assert not link_state(current)

    def test_save_selection_while_pagination(self):
        """
        1. Go to home page
        2. Select first 2 items
        3. Go to 2-nd page
        4. Check that no items selected
        5. Go to 1-st page
        6. Check that first 2 items are selected
        """
        self.selenium.get(self.live_server_url)
        time.sleep(3)
        # select first 2 items
        self.assertFalse(self.selenium.find_element_by_xpath(
                "//div[@class='bDiv']/fieldset/table/tbody/tr[2]/td[1]/div/input"
                ).get_attribute('checked'))
        self.selenium.find_element_by_xpath(
                "//div[@class='bDiv']/fieldset/table/tbody/tr[1]/td[1]/div/input").click()
        self.selenium.find_element_by_xpath(
                "//div[@class='bDiv']/fieldset/table/tbody/tr[2]/td[1]/div/input").click()
        self.assertTrue(self.selenium.find_element_by_xpath(
                "//div[@class='bDiv']/fieldset/table/tbody/tr[2]/td[1]/div/input"
                ).get_attribute('checked'))
        # go to second page
        self.selenium.find_element_by_xpath(
                '//div[@class="pagination-centered"]/ul/li[3]/a').click()
        time.sleep(3)
        self.assertFalse(self.selenium.find_element_by_xpath(
                "//div[@class='bDiv']/fieldset/table/tbody/tr[2]/td[1]/div/input"
                ).get_attribute('checked'))
        # got to first page
        self.selenium.find_element_by_xpath(
                '//div[@class="pagination-centered"]/ul/li[2]/a').click()
        time.sleep(3)
        self.assertTrue(self.selenium.find_element_by_xpath(
                "//div[@class='bDiv']/fieldset/table/tbody/tr[2]/td[1]/div/input"
                ).get_attribute('checked'))

    def test_sorting_order(self):
        """
        Test that sorting works properly.
        1. Go to search page (default query)
        2. Walk throw table columns
        3. Click on column header to select descending ordering
        4. Get top value in clumn
        5. Click on column header once more to select ascending ordering
        6. Get top value in column and compare it with previous
        7. Repeat 3..6 for every column
        """
        with self.settings(**TEST_SETTINGS):
            self.selenium.get(self.live_server_url)
            for i, column in enumerate(TEST_SETTINGS['TABLE_COLUMNS']):
                # walk over all visible table columns
                if TEST_SETTINGS['COLUMN_STYLES'][column]['default_state'] == 'hidden':
                    continue
                # sorting by keys, not by names
                if 'Name' in column:
                    continue
                # codes uses here and ordering by full name
                if column == 'Sample Type':
                    continue
                attr = COLUMN_NAMES[column]
                # scroll table
                self.selenium.execute_script(
                        "$('.bDiv')"
                        ".scrollLeft($('th[axis=col{0}]')"
                        ".position().left);".format(i + 1))
                # after first click element element is asc sorted
                self.selenium.find_element_by_partial_link_text(column).click()

                # getting top element in the column
                selector = "//div[@class='bDiv']//table/tbody/tr[1]/td[{}]".format(i + 2)
                first = self.selenium.find_element_by_xpath(selector).text

                # scroll table
                self.selenium.execute_script("$('.bDiv')"
                        ".scrollLeft($('th[axis=col{0}]')"
                        ".position().left);".format(i + 1))
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


class ColumnSelectUITestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(ColumnSelectUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(ColumnSelectUITestCase, self).tearDownClass()

    def check_select_columns(self, location):
        """
        Check that displayed columns selection works.
        1. Uncheck all columns one by one
        2. After every click, check that all previous columns are hidden and all next are visible
        3. Also check that last column takes all free space
        4. Click on '(Toggle all)'
        5. Check that all columns visible
        6. Reset to defaults

        :param location: 'search' or 'cart'
        """
        driver = self.selenium
        # get columns count
        column_count = len(driver.find_elements_by_xpath(
                        "//div[@class='hDivBox']/table/thead/tr/th")) - 1
        # Find select on search or cart page
        if location == 'search':
            select = driver.find_element_by_xpath(
                        "//form[@id='id_add_files_form']/span/span\
                        /span[@class='ui-dropdownchecklist-text']")
        elif location == 'cart':
            select = driver.find_element_by_css_selector(
                        "#ddcl-id-columns-selector > span:first-child > span")
        select.click()

        # check all
        driver.find_element_by_xpath(
                "//label[@for='ddcl-id-columns-selector-i0']").click()
        time.sleep(2)

        # uncheck one by one
        r = range(column_count)
        for i in r:
            driver.find_element_by_xpath(
                    "//label[@for='ddcl-id-columns-selector-i%d']" % (i + 1)).click()
            # check that all previous columns are hidden
            for j in r[:(i + 1)]:
                driver.execute_script("$('.bDiv')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % j)
                assert not driver.find_element_by_xpath(
                        "//th[@axis='col%d']" % (j + 1)).is_displayed()
            # check that all next columns are visible
            for j in r[(i + 1):]:
                driver.execute_script("$('.bDiv')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % j)
                assert driver.find_element_by_xpath("//th[@axis='col%d']" % (j + 1)).is_displayed()
            # check that last column takes all free space
            if i < column_count - 1:
                full_width = driver.find_element_by_class_name('hDiv').value_of_css_property('width')[:-2]
                full_width = int(full_width.split('.')[0])
                all_columns_width = driver.find_element_by_xpath(
                        "//th[@axis='col0']").size.get('width', 0)
                for x in range(1, column_count + 1):
                    col = driver.find_element_by_xpath("//th[@axis='col%d']" % x)
                    if col.is_displayed():
                        all_columns_width += col.size.get('width', 0)
                self.assertTrue(full_width - all_columns_width < 3)
        # select (Toggle all) option
        driver.find_element_by_xpath(
                "//label[@for='ddcl-id-columns-selector-i0']").click()
        r2 = range(column_count)
        for x in r2:
            driver.execute_script("$('.bDiv')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % x)
            assert driver.find_element_by_xpath(
                    "//th[@axis='col%d']" % (x + 1)).is_displayed()
        # reset to defaults
        driver.find_element_by_class_name("js-default-columns").click()
        # close DDCL
        select.click()

    def test_column_select(self):
        """
        Check that select/unselect visible columns feature works properly
        1. Go to search page (default query)
        2. Check columns selection
        3. Select all items in cart and click 'Add to cart' (user will be redirected to cart page)
        4. Check columns selection on cart page
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            self.check_select_columns('search')
            time.sleep(5)
            self.check_select_columns('cart')

    def test_default_columns_button(self):
        """
        Check that 'Reset to defaults' button works properly.
        1. Open search page (default query)
        2. Make all columns visible (check '(Toggle all)')
        3. Count visible columns
        4. Click on 'Reset to defaults'
        5. Count visible columns
        6. Compare obtained numbers with settings
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            select = driver.find_element_by_xpath(
                        "//form[@id='id_add_files_form']/span/span\
                        /span[@class='ui-dropdownchecklist-text']")
            # select (Toggle all) option
            select.click()
            driver.find_element_by_xpath(
                    "//label[@for='ddcl-id-columns-selector-i0']").click()
            time.sleep(2)
            select.click()
            # count visible columns
            columns_count = len(driver.find_elements_by_xpath(
                        "//div[@class='hDivBox']/table/thead/tr/th")) - 1
            visible = 0
            for i in range(columns_count):
                driver.execute_script("$('.bDiv')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % i)
                if driver.find_element_by_xpath("//th[@axis='col%d']" % (i + 1)).is_displayed():
                    visible += 1
            self.assertEqual(visible, columns_count)
            # click on 'Reset to defaults'
            select.click()
            driver.find_element_by_class_name('js-default-columns').click()
            # recount columns
            visible = 0
            for i in range(columns_count):
                driver.execute_script("$('.flexigrid')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % i)
                if driver.find_element_by_xpath("//th[@axis='col%d']" % (i + 1)).is_displayed():
                    visible += 1
            default_count = 0
            for col in TEST_SETTINGS['TABLE_COLUMNS']:
                if TEST_SETTINGS['COLUMN_STYLES'][col]['default_state'] == 'visible':
                    default_count += 1
            self.assertEqual(visible, default_count)


class ResetFiltersUITestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(ResetFiltersUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(ResetFiltersUITestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def get_selected_filters(self):
        """
        Return selected filters as text.
        '(Toggle all)' skipped
        """
        texts = self.selenium.find_elements_by_css_selector(
                    '.base-sidebar .ui-dropdownchecklist-text > span')
        filters = ''
        for text in texts:
            filters += text.text
        return filters

    def test_reset_filters_button(self):
        """
        1. Go to search page (default query)
        2. Remember default filters
        3. Set not default filter
        4. Submit, check that some other filters are selected besides default
        5. Reset filters
        6. Compare filters with remembered ones
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)

            # remember filters
            default_filters = self.get_selected_filters()

            # find filter that not exists in defaults and set it
            for f in ALL_FILTERS:
                if (
                        f not in TEST_SETTINGS['DEFAULT_FILTERS'] and
                        f not in DATE_ATTRIBUTES and
                        len(ALL_FILTERS[f]['filters']) > 3):
                    filter_name = f
                    break

            # select first 2 options in filter
            driver.find_element_by_xpath("//span[@id='ddcl-id-{0}']/span/span".format(filter_name)).click()
            driver.find_element_by_id("ddcl-id-{0}-i0".format(filter_name)).click()
            driver.find_element_by_xpath("//label[@for='ddcl-id-{0}-i1']".format(filter_name)).click()
            driver.find_element_by_xpath("//label[@for='ddcl-id-{0}-i2']".format(filter_name)).click()
            driver.find_element_by_xpath("//span[@id='ddcl-id-{0}']/span/span".format(filter_name)).click()

            # apply filters
            driver.find_element_by_id("id_apply_filters").click()
            self.assertNotEqual(default_filters, self.get_selected_filters())

            # try to reset filters
            driver.find_element_by_id("id_reset_filters").click()
            self.assertEqual(default_filters, self.get_selected_filters())


class BatchSearchUITestCase(LiveServerTestCase):

    ids = (
            '04578995-3609-4f09-bc12-7100a04ebc92',
            '549571a3-98a7-4601-adb1-6951d770cc0e')

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(BatchSearchUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(BatchSearchUITestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def test_reset_form(self):
        """
        1. Go to batch search page
        2. Enter something into textarea and filefield
        3. Click on reset button
        4. Check that fields are empty
        """
        self.selenium.get('%s%s' % (
                self.live_server_url,
                reverse('batch_search_page')))
        time.sleep(1)
        textarea = self.selenium.find_element_by_xpath(
                '//textarea[@id="id_text"]')
        fileinput = self.selenium.find_element_by_xpath(
                '//input[@id="id_upload"]')
        textarea.send_keys('some text')
        fileinput.send_keys('/some/file.txt')
        time.sleep(1)
        self.assertTrue(textarea.get_attribute('value'))
        self.assertTrue(fileinput.get_attribute('value'))
        self.selenium.find_element_by_xpath(
                '//button[@type="reset"]').click()
        time.sleep(1)
        self.assertFalse(textarea.get_attribute('value'))
        self.assertFalse(fileinput.get_attribute('value'))

    def test_batch_search_form_error(self):
        """
        1. Go to batch search page
        2. Enter some bed id
        3. Click on 'Search' button
        4. Check that error message exists
        5. Enter not existent id
        6. Click on 'Search' button
        7. Check that error message exists
        """
        self.selenium.get('%s%s' % (
                self.live_server_url,
                reverse('batch_search_page')))
        time.sleep(1)
        textarea = self.selenium.find_element_by_xpath(
                '//textarea[@id="id_text"]')
        textarea.send_keys('bad id')
        self.selenium.find_element_by_xpath(
                '//button[@type="submit"]').click()
        time.sleep(1)
        error = self.selenium.find_element_by_xpath('//ul[@class="errorlist"]').text
        self.assertIn('No valid ids were found', error)
        # enter not existent id
        textarea = self.selenium.find_element_by_xpath(
                '//textarea[@id="id_text"]')
        textarea.send_keys(
                Keys.BACK_SPACE * 10 + '11111111-1111-1111-1111-111111111111');
        time.sleep(1)
        self.selenium.find_element_by_xpath(
                '//button[@type="submit"]').click()
        time.sleep(1)
        error = self.selenium.find_element_by_xpath('//ul[@class="errorlist"]').text
        self.assertIn('No results found', error)
        

    def test_batch_search_results_edit(self):
        """
        1. Go to batch search page
        2. Enter 2 analysis ids
        3. Click on 'Search' button
        4. Try to find items in table
        5. Select first item, click on 'Remove' button
        6. Check that only one item is available
        7. Click on 'Add 1 items to cart'
        8. Check that 'cart' in url
        9. Check cart items count
        """
        self.selenium.get('%s%s' % (
                self.live_server_url,
                reverse('batch_search_page')))
        time.sleep(1)
        textarea = self.selenium.find_element_by_xpath(
                '//textarea[@id="id_text"]')
        textarea.send_keys('\n'.join(self.ids))
        self.selenium.find_element_by_xpath(
                '//button[@type="submit"]').click()
        time.sleep(2)
        summary = self.selenium.find_element_by_id(
                'batch-search-summary').text
        self.assertIn('Submitted ids: 2', summary)
        self.assertIn('Found by analysis_id: 2', summary)
        # check rows count
        self.assertEqual(
                len(self.selenium.find_elements_by_xpath(
                        '//div[@class="bDiv"]/fieldset/table/tbody/tr')),
                2)
        checkbox = self.selenium.find_element_by_xpath(
                '//div[@class="bDiv"]/fieldset/table/tbody/tr[1]/td[1]/div/input')
        checkbox.click()
        time.sleep(1)
        # remove
        self.selenium.find_element_by_xpath(
                '//div[@class="cart-btn-group"]/button[1]').click()
        time.sleep(2)
        # check rows count
        self.assertEqual(
                len(self.selenium.find_elements_by_xpath(
                        '//div[@class="bDiv"]/fieldset/table/tbody/tr')),
                1)
        # add item to cart
        self.selenium.find_element_by_xpath(
                '//div[@class="cart-btn-group"]/button[2]').click()
        time.sleep(2)
        self.assertIn('cart', self.selenium.current_url)
        summary = self.selenium.find_element_by_id('results-summary').text
        self.assertIn('Files in your cart: 1', summary)

    def test_details_popup(self):
        """
        1. Go to batch search page
        2. Submit 2 analysis_ids
        3. Click on 'Search'
        4. Click on first table row
        5. Check popup is visible
        """
        self.selenium.get('%s%s' % (
                self.live_server_url,
                reverse('batch_search_page')))
        time.sleep(1)
        textarea = self.selenium.find_element_by_xpath(
                '//textarea[@id="id_text"]')
        textarea.send_keys('\n'.join(self.ids))
        self.selenium.find_element_by_xpath(
                '//button[@type="submit"]').click()
        time.sleep(2)
        # click on table row
        self.selenium.find_element_by_xpath(
                '//div[@class="bDiv"]/fieldset/table/tbody/tr[1]/td[2]').click()
        time.sleep(1)
        popup = self.selenium.find_element_by_id('itemDetailsModal')
        self.assertTrue(popup.is_displayed())


class SkipNavUITestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SkipNavUITestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(SkipNavUITestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def test_skip_nav(self):
        """
        1. Go to search page (default query)
        2. Check that skip-nav exists and has height == 0
        3. Press tab, check that skip nav height more than 0
        4. Click on first link, check that height == 0 (skip to nav invisible)
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            ac = ActionChains(driver)
            driver.get(self.live_server_url)
            links = driver.find_element_by_id('accessibility-links')
            self.assertEqual(links.size['height'], 0)
            # press tab (selenium.webdriver.common.keys.TAB)
            for i in range(3):
                ac.key_down(Keys.TAB)
            ac.perform()
            self.assertNotEqual(links.size['height'], 0)
            time.sleep(1)
            driver.find_element_by_xpath(
                "//ul[@id='accessibility-links']/li[1]/a").click()
            time.sleep(1)
            self.assertEqual(links.size['height'], 0)


class TabbingUITestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = WebDriver()
        self.ac = ActionChains(self.selenium)
        self.selenium.implicitly_wait(5)

    def tearDown(self):
        time.sleep(1)
        self.selenium.quit()

    def check_tabbing(self, elements):
        """
        1. Rememeber first element under focus
        2. Press 'Tab'
        3. Get current element and check that it is the same as current elements item
        4. If has - increase counter
        5. If this is first remembered element - stop, elese go to 2
        6. Check that all elements were tabbed

        :elements: xpaths to elements sorted in order they should tabbed
        """
        driver = self.selenium
        self.ac.key_up(Keys.TAB)
        self.ac.perform()
        self.ac.perform()
        start_element = driver.switch_to_active_element()
        current_element = None
        pos = 0
        while not current_element or current_element.id != start_element.id:
            next_element = driver.find_element_by_xpath(elements[pos])
            self.ac.perform()
            current_element = driver.switch_to_active_element()
            if current_element.id == next_element.id:
                pos += 1
                if pos == len(elements):
                    break
        self.assertEqual(pos, len(elements))

    def test_tabbing_on_search_page(self):
        """
        1. Go to search page (default query)
        2. Check tabbing
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            time.sleep(3)
            elements = (
                '//ul[@id="accessibility-links"]/li[3]/a', # skip to summary link
                '//ul[@class="nav"]/li[4]/a', # Accessibility page link
                '//div[@id="filters-bar"]/span[1]/span[1]', # filter by study
                '//button[@id="id_apply_filters"]', # applye filters button
                '//section[@id="results-summary"]', # results summary
                '//form[@id="id_add_files_form"]/div[1]/div[1]/button[1]', # add to cart button
                '//div[@class="items-per-page-label"]/a[1]', # items per page link
                '//div[@class="pagination-centered"]/ul/li[1]/a', #pagination
            )
            self.check_tabbing(elements)

    def test_tabbing_on_batch_search_page(self):
        """
        1. Go to search page (default query)
        2. Check tabbing
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url + reverse('batch_search_page'))
            time.sleep(3)
            elements = (
                '//ul[@id="accessibility-links"]/li[1]/a', # skip to batch form
                '//ul[@class="nav"]/li[4]/a', # Accessibility page link
                '//input[@id="id-search-field"]', # search box
                '//textarea[@id="id_text"]', # textarea
                '//input[@id="id_upload"]', # file select
                '//button[@type="submit"]', # submit button
                '//button[@type="reset"]', # reset button
            )
            self.check_tabbing(elements)

    def test_tabbing_on_cart_page(self):
        """
        1. Go to search page (default query)
        2. Add ferst file to cart
        3. Check tabbing on cart page
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            time.sleep(3)
            # add files to cart and go to cart page
            driver.find_element_by_xpath(
                    "//div[@class='bDiv']/fieldset/table/tbody/tr[1]/td[1]/div/input"
                    ).click()
            driver.find_element_by_css_selector('.add-to-cart-btn').click()
            time.sleep(3)
            elements = (
                '//ul[@id="accessibility-links"]/li[3]/a', # skip to main results
                '//ul[@class="nav"]/li[3]/a', # Help page link
                '//div[@class="btn-toolbar"]/div[1]/button[1]', # remove from cart button
                '//span[@id="ddcl-id-columns-selector"]/span[1]', # columns ddcl
                '//input[@id="id-check-all-checkbox"]', # select all checkbox
                '//th[@id="id-col-study"]/div/a', # study link
            )
            self.check_tabbing(elements)

    def test_tabbing_on_details_page(self):
        """
        1. Go to search page (default query)
        2. Get some analysis id from table
        3. Go to details page
        3. Check tabbing on details page
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            time.sleep(3)
            # go to file details page
            details_url = driver.find_element_by_xpath(
                            '//div[@class="bDiv"]//tbody/tr[1]'
                            ).get_attribute('data-details-url')
            driver.get('%s%s' % (self.live_server_url, details_url))
            time.sleep(3)
            elements = (
                '//ul[@id="accessibility-links"]/li[2]/a', # skip to main content link
                '//ul[@class="nav"]/li[2]/a', # Cart page link
                '//a[@id="id-collapse-all-button"]', # collapse all button
                '//button[@id="id-download-metadata"]', # download xml button
                '//div[@id="XMLHolder"]', # raw xml view
            )
            self.check_tabbing(elements)


class TableNavigationUITestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = WebDriver()
        self.ac = ActionChains(self.selenium)
        self.selenium.implicitly_wait(5)

    def tearDown(self):
        time.sleep(1)
        self.selenium.quit()

    def test_data_table(self):
        """
        1. Go to search page (default query)
        2. Set socus to table first checkbox
        3. Try to use arrows to navigate in table
        4. Press alt + enter, check that popup appears
        5. Press ctrl + enter, check that additional window opened
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            time.sleep(3)
            selectors = driver.find_elements_by_xpath('//td[@class="tdSelected"]')
            self.assertEqual(len(selectors), 0)
            checkbox = driver.find_element_by_xpath(
                '//div[@class="bDiv"]/fieldset/table/tbody/tr[2]/td[1]/div/input')
            checkbox.click()
            # using arrows
            time.sleep(1)
            selectors = driver.find_elements_by_xpath('//td[@class="tdSelected"]')
            self.assertEqual(len(selectors), 1)
            self.ac.key_down(Keys.ALT)
            self.ac.key_up(Keys.ARROW_RIGHT)
            self.ac.perform()
            time.sleep(1)
            selectors = driver.find_elements_by_xpath('//td[@class="tdSelected"]')
            self.assertEqual(len(selectors), 2)
            # press alt + down and check that focus changed
            self.ac.key_down(Keys.ALT)
            self.ac.key_up(Keys.ARROW_DOWN)
            self.ac.perform()
            time.sleep(1)
            current_element = driver.switch_to_active_element()
            checkbox = driver.find_element_by_xpath(
                    '//div[@class="bDiv"]/fieldset/table/tbody/tr[3]/td[1]/div/input')
            self.assertEqual(current_element, checkbox)
            # try to press alt + enter
            self.ac = ActionChains(driver)
            cell = driver.find_element_by_xpath(
                    '//div[@class="bDiv"]/fieldset/table/tbody/tr[3]/td[2]/div')
            self.ac.key_down(Keys.ALT, cell)
            self.ac.key_up(Keys.ENTER, cell)
            self.ac.perform()
            time.sleep(3)
            # check details popup visible
            popup = driver.find_element_by_css_selector('#itemDetailsModal')
            assert popup.is_displayed()
            # close popup
            driver.find_element_by_xpath(
                    "//button[@data-dismiss='modal']").click()
            time.sleep(1)
            # try to open details page using ctrl + enter
            # CONTROL + ENTER doesn't work in selenium, no idea why

    def test_current_cell_always_visible(self):
        """
        1. Go to search page (default query)
        2. Set socus to table first checkbox
        3. Check that last column not visible
        4. Pres ALT + ARROW_RIGTH buttons few times
        5. Check that last column visible
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            time.sleep(3)
            checkbox = driver.find_element_by_xpath(
                '//div[@class="bDiv"]/fieldset/table/tbody/tr[2]/td[1]/div/input')
            cell = driver.find_element_by_xpath(
                '//div[@class="bDiv"]/fieldset/table/tbody/tr[2]/td[2]/div')
            checkbox.click()
            time.sleep(1)
            last_column = TEST_SETTINGS['TABLE_COLUMNS'][-1]
            column_attr = COLUMN_NAMES[last_column]
            th = driver.find_element_by_xpath(
                    "//th[@id='id-col-%s']" % column_attr)
            self.assertFalse(th.is_displayed())
            for i in TEST_SETTINGS['TABLE_COLUMNS']:
                self.ac.key_down(Keys.ALT)
                self.ac.key_down(Keys.ARROW_RIGHT)
                self.ac.key_up(Keys.ARROW_RIGHT)
            self.ac.perform()
            time.sleep(5)
            th = driver.find_element_by_xpath(
                    "//th[@id='id-col-%s']" % column_attr)
            self.assertTrue(th.is_displayed())


# tests for help app

HELP_TEST_SETTINGS = dict(TEST_SETTINGS)
HELP_TEST_SETTINGS['HELP_HINTS'] = {
    'filter:Study': 'Filter by research study that generated the data set',
    'common:filters-reset-button': 'Reset the filters and search text to their default state',
    'Study:TCGA': 'The Cancer Genome Atlas <a href="#" data-slug="test-help" class="js-help-link">click to view help popup</a>',
    'Study:CCLE': 'Cancer Cell Line Encyclopedia',
    'Study:TCGA Benchmark': 'TCGA Mutation Calling Benchmark 4 (artificial data)',
    'Study': 'Research study that generated the data set',
}


class HelpHintsUITestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = WebDriver()
        self.ac = ActionChains(self.selenium)
        self.selenium.implicitly_wait(5)

    def tearDown(self):
        time.sleep(1)
        self.selenium.quit()

    def get_column_number_by_name(self, name):
        counter = 0
        for col in TEST_SETTINGS['TABLE_COLUMNS']:
            if TEST_SETTINGS['COLUMN_STYLES'][col]['default_state'] == 'hidden':
                continue
            counter += 1
            if col == name:
                return counter + 1

    def check_tooltip(self, target):
        """
        Check that tooltip appears if place cursor on it and wait few seconds
        """
        assert not self.selenium.find_elements_by_css_selector('.js-tooltip')
        self.ac.move_to_element(target)
        self.ac.perform()
        time.sleep(3)
        tooltip = self.selenium.find_element_by_css_selector('.js-tooltip')
        assert tooltip.is_displayed()
        # hide tooltip
        search_field = self.selenium.find_element_by_css_selector(
                '.navbar-search .search-query')
        search_field.click()
        time.sleep(1)

    def test_help_hints_in_table(self):
        """
        Check that tooltip appears.
        1. Go to search page (default query)
        2. Check tooltip for table header (move cursor to target, wait, check tooltip displayed)
        3. Check tooltip for table cells
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)

            # table header
            study_header = driver.find_element_by_xpath(
                "//div[@class='hDivBox']/table/thead/tr/th[{0}]/div/a".format(
                                self.get_column_number_by_name('Study')))
            self.check_tooltip(study_header)
            # table cell
            study_cell = driver.find_element_by_xpath(
                "//div[@class='bDiv']/fieldset/table/tbody/tr/td[{0}]/div".format(
                                self.get_column_number_by_name('Study')))
            self.check_tooltip(study_cell)

    def test_help_hints_in_filters(self):
        """
        Check that tooltip appears.
        1. Go to search page (default query)
        2. Check tooltip for filter header
        3. Check tooltip for selected filter options
        4. Check tooltip for filter options
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)

            # filter header
            study_filter_header = driver.find_elements_by_css_selector(
                            ".sidebar .filter-label")[0]
            self.check_tooltip(study_filter_header)
            # seleted filters
            study_selected_option = driver.find_elements_by_css_selector(
                            ".sidebar .ui-dropdownchecklist-text-item")[0]
            self.check_tooltip(study_selected_option)
            # open Study DDCL
            self.selenium.find_element_by_id("ddcl-id-study").click()
            # filter options
            study_filter_option = driver.find_elements_by_css_selector(
                            ".sidebar .ui-dropdownchecklist-item")[1]
            self.check_tooltip(study_filter_option)

    def test_help_hints_in_applied_filters(self):
        """
        Check that tooltip appears.
        1. Go to search page (default query)
        2. Check tooltip for Study in applied filters
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)

            study_filter_option = driver.find_element_by_xpath(
                            '//div[@class="applied-filters"]/ul/li[1]/span[1]')
            self.check_tooltip(study_filter_option)

    def test_help_hints_common(self):
        """
        Check that tooltip appears.
        1. Go to search page (default query)
        2. Check tooltip for reset button (common)
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)

            # reset button (common tooltip)
            driver.execute_script(
                "$(window).scrollTop($('#id_reset_filters').offset().top - 100);")
            reset_button = driver.find_element_by_id("id_reset_filters")
            self.check_tooltip(reset_button)

    def test_help_hints_in_details_popup(self):
        """
        Check that tooltip appears.
        1. Go to search page (default query)
        2. Open details popup
        3. Check tooltip for details table title
        4. Check tooltip for details table item
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)

            # open details popup
            driver.find_element_by_xpath(
                    "//div[@class='bDiv']/fieldset/table/tbody/tr[1]/td[2]").click()
            time.sleep(3)
            # details table titles
            details_title = driver.find_elements_by_css_selector(
                                            "#itemDetailsModal th")[0]
            self.check_tooltip(details_title)
            # details table values
            details_value = driver.find_elements_by_css_selector(
                                            "#itemDetailsModal td")[0]
            self.check_tooltip(details_value)

    def test_help_hints_on_details_page(self):
        """
        Check that tooltip appears.
        1. Go to details page
        2. Check tooltip for details table title
        3. Check tooltip for details table item
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get('%s/details/%s/' % (
                    self.live_server_url, 'f0b7370f-8473-415b-86e7-9cb1d96c1411'))
            # details table titles
            details_title = driver.find_elements_by_css_selector(
                                            ".js-details-table th")[0]
            self.check_tooltip(details_title)
            # details table values
            details_value = driver.find_elements_by_css_selector(
                                            ".js-details-table td")[0]
            self.check_tooltip(details_value)

    def test_help_hints_in_columns_ddcl_on_search_page(self):
        """
        Check that tooltip appears.
        1. Go to search page (default query)
        2. Open columns list DDCL
        3. Check tooltip columns headers in DDCL
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)

            driver.find_element_by_id("ddcl-id-columns-selector").click()
            study_column_option = driver.find_element_by_xpath(
                    "//input[@id='ddcl-id-columns-selector-i2']/../label")
            self.check_tooltip(study_column_option)

    def test_help_hints_in_columns_ddcl_on_cart_page(self):
        """
        Check that tooltip appears.
        1. Go to search page (default query)
        2. Add first item to cart
        3. Go to cart page
        4. Open columns list DDCL
        5. Check tooltip columns headers in DDCL
        """
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)

            driver.find_element_by_xpath(
                    "//div[@class='bDiv']/fieldset/table/tbody/tr[1]/td[1]/div/input"
                    ).click()
            driver.find_element_by_css_selector('.add-to-cart-btn').click()
            time.sleep(3)
            driver.find_element_by_id("ddcl-id-columns-selector").click()
            study_column_option = driver.find_element_by_xpath(
                    "//input[@id='ddcl-id-columns-selector-i2']/../label")
            self.check_tooltip(study_column_option)

    def test_help_popups(self):
        """
        1. Add help popup content to database
        2. Go to search page (default query)
        3. Trigger tooltip for Study:TCGA which contains link to open help popup
        4. Open tooltip, click on link
        5. Check that popup shown
        6. Check that content and title is right 
        """
        slug = 'test-help'
        title = 'Test popup title'
        content = 'Test popup content'
        # add help popup content to database
        HelpText.objects.create(slug=slug, title=title, content=content)
        with self.settings(**HELP_TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            study_cell = driver.find_element_by_xpath(
                "//div[@class='bDiv']/fieldset/table/tbody/tr/td[{0}]/div".format(
                                self.get_column_number_by_name('Study')))
            self.ac.move_to_element(study_cell)
            self.ac.perform()
            time.sleep(3)
            tooltip = self.selenium.find_element_by_css_selector('.js-tooltip')
            assert tooltip.is_displayed()
            link = self.selenium.find_element_by_css_selector('.js-tooltip a')
            link.click()
            time.sleep(3)
            popup = driver.find_element_by_id('messageModal')
            assert popup.is_displayed()
            popup_title = self.selenium.find_element_by_css_selector(
                    '#common-message-label').text
            popup_content = self.selenium.find_element_by_css_selector(
                    '#messageModal .modal-body').text
            self.assertEqual(popup_title, title)
            self.assertEqual(popup_content, content)
