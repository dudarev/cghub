import time
import os
from urllib import unquote
from datetime import datetime, date, timedelta

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains

from django.test import LiveServerTestCase
from django.conf import settings

from cghub.settings.utils import root
from cghub.apps.core.filters_storage import ALL_FILTERS
from cghub.apps.core.attributes import DATE_ATTRIBUTES, COLUMN_NAMES


TEST_CACHE_DIR = root('test_cache')

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
    DETAILS_FIELDS = (
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
    COLUMN_STYLES = {
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
        'Disease': {
            'width': 65, 'align': 'left', 'default_state': 'visible',
        },
        'Experiment Type': {
            'width': 95, 'align': 'left', 'default_state': 'hidden',
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
    DEFAULT_FILTERS = {
        'study': ('phs000178','*Other_Sequencing_Multiisolate'),
        'state': ('live',),
        'upload_date': '[NOW-7DAY+TO+NOW]',
    },
    # use existing cache
    WSAPI_CACHE_DIR=TEST_CACHE_DIR,
    CART_CACHE_DIR=TEST_CACHE_DIR
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


def get_filter_id(driver, filter_name):
    """
    Helper function for getting sidebar filter id.
    Makes filter tests easier to maintain.
    """
    el = driver.find_element_by_css_selector("select[data-section='{0}'] + span".format(filter_name))
    el_id = el.get_attribute('id').split('-')[-1]
    return el_id


def scroll_page_to_filter(driver, filter_id):
    """
    Scroll page to element (makes it visible fo user).
    """
    driver.execute_script(
            "$(window).scrollTop($('#ddcl-{0}').offset().top - 100);".format(filter_id))


class SidebarTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        # FIXME(nanvel): maybe possible decrease it or use in other tests
        # http://selenium-python.readthedocs.org/en/latest/api.html#selenium.webdriver.remote.webdriver.implicitly_wait
        self.selenium.implicitly_wait(5)
        super(SidebarTestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(SidebarTestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def test_select_all(self):
        """
        1. Open 'By Center' filter (Selected all items by default)
        2. Click on '(all)'
        3. Check that all checkboxes unchecked
        4. Click on '(all)'
        5. Check that all checkboxes checked
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)

            center_id = get_filter_id(driver, 'center_name')
            self.selenium.find_element_by_id("ddcl-{0}".format(center_id)).click()

            # get centers count
            centers_count = len(ALL_FILTERS['center_name']['filters'])
            # by center has <centers_count> centers, i0 - deselect all, i1-i<centers_count> - selections
            # click on 'All' to deselect all and check that no one selected
            driver.find_element_by_id("ddcl-{0}-i0".format(center_id)).click()
            for i in range(1, centers_count + 1):
                cb = driver.find_element_by_id("ddcl-{0}-i{1}".format(center_id, i))
                self.assertFalse(cb.is_selected())

            # click again - select all
            # check that all centers selected
            driver.find_element_by_id("ddcl-{0}-i0".format(center_id)).click()
            for i in range(1, centers_count + 1):
                cb = driver.find_element_by_id("ddcl-{0}-i{1}".format(center_id, i))
                self.assertTrue(cb.is_selected())

    def test_select_date(self):
        """
        1. Open 'By Time Modified' filter
        2. Select 'Any date' option
        3. Check that other options unchecked
        4. Click on 'Today' option
        5. Check that other unchecked
        6. Open 'By Upload Time' filter
        7. Go To 2
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            driver.find_element_by_css_selector("span.ui-dropdownchecklist-text").click()

            # Open 'By Time Modified' filter
            last_modified_id = get_filter_id(driver, 'last_modified')
            driver.find_element_by_xpath(
                "//span[@id='ddcl-{0}']/span/span".format(last_modified_id)).click()

            # click the first selection
            i_click = 0
            driver.find_element_by_id("ddcl-{0}-i{1}".format(last_modified_id, i_click)).click()
            # check that other options are unselected
            for i in range(0, 5):
                if not i == i_click:
                    rb = driver.find_element_by_id("ddcl-{0}-i{1}".format(last_modified_id, i))
                    self.assertFalse(rb.is_selected())

            # click on first option
            i_click = 1
            driver.find_element_by_id("ddcl-{0}-i{1}".format(last_modified_id, i_click)).click()
            # check that other options unselected
            for i in range(0, 5):
                if not i == i_click:
                    rb = driver.find_element_by_id("ddcl-{0}-i{1}".format(last_modified_id, i))
                    self.assertFalse(rb.is_selected())

            # open 'By Upload Time' filter
            upload_date_id = get_filter_id(driver, 'upload_date')
            driver.find_element_by_xpath(
                "//span[@id='ddcl-{0}']/span/span".format(upload_date_id)).click()
        
            # select first option
            z_click = 0
            driver.find_element_by_id("ddcl-{0}-i{1}".format(upload_date_id, z_click)).click()
            # check that other options are unselected
            for i in range(0, 5):
                if not i == z_click:
                    rb = driver.find_element_by_id("ddcl-{0}-i{1}".format(upload_date_id, i))
                    self.assertFalse(rb.is_selected())

            # select second option
            z_click = 1
            driver.find_element_by_id("ddcl-{0}-i{1}".format(upload_date_id, z_click)).click()
            # check that other options are unselected
            for i in range(0, 5):
                if not i == z_click:
                    rb = driver.find_element_by_id("ddcl-{0}-i{1}".format(upload_date_id, i))
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
                filter_id = get_filter_id(driver, f)
                scroll_page_to_filter(driver, filter_id)
                self.selenium.find_element_by_css_selector(
                        "#ddcl-{0} > span:first-child > span".format(filter_id)).click()
                # if some items selected by default, select all
                if f in TEST_SETTINGS['DEFAULT_FILTERS']:
                    driver.find_element_by_id("ddcl-{0}-i0".format(filter_id)).click()
                # unselect all
                driver.find_element_by_id("ddcl-{0}-i0".format(filter_id)).click()
                # select necessary options
                for i in selected_options_ids[f]:
                    driver.find_element_by_id("ddcl-{0}-i{1}".format(filter_id, i)).click()
                # and close filter DDCL
                self.selenium.find_element_by_css_selector(
                        "#ddcl-{0} > span:last-child > span".format(filter_id)).click()

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


class CustomPeriodTestCase(LiveServerTestCase):

    year = date.today().year
    TEST_DATES = (
        {
            'start': date(year, 2, 10),
            'end': date(year, 2, 15),
            'res_start': date(year, 2, 10),
            'res_end': date(year, 2, 15)},
        { # another month
            'start': date(year, 1, 10),
            'end': date(year, 3, 15),
            'res_start': date(year, 1, 10),
            'res_end': date(year, 3, 15)},
        { # today
            'start': date(year, 2, 10),
            'end': date(year, 2, 10),
            'res_start': date(year, 2, 9),
            'res_end': date(year, 2, 10)},
        { # future
            'start': date(year, 2, 10),
            'end': date.today() + timedelta(days=10),
            'res_start': date(year, 2, 10),
            'res_end': date.today()},
        { # swapped
            'start': date(year, 2, 15),
            'end': date(year, 2, 10),
            'res_start': date(year, 2, 10),
            'res_end': date(year, 2, 15)},
    )

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(CustomPeriodTestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(CustomPeriodTestCase, self).tearDownClass()

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
        filter_id = get_filter_id(driver, filter_name)

        # Check custom date is displayed in filter input
        filter_input = driver.find_element_by_id("ddcl-{0}".format(filter_id))
        filter_text = filter_input.find_element_by_css_selector(
                                    '.ui-dropdownchecklist-text').text
        text = "{0} - {1}".format(
                        datetime.strftime(start, '%Y/%m/%d'),
                        datetime.strftime(end, '%Y/%m/%d'))
        assert text in filter_text.strip()

    def test_custom_upload_date(self):
        """
        1. Open 'By Upload Time' filter
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
            # scroll to 'By Upload Time' filter
            filter_id = get_filter_id(driver, 'upload_date')
            scroll_page_to_filter(driver, filter_id)

            # check popup displayed and cancel button works
            self.assertFalse(driver.find_elements_by_css_selector('.dp-container'))
            driver.find_element_by_id("ddcl-{0}".format(filter_id)).click()
            driver.find_element_by_css_selector(
                        '#ddcl-{0}-ddw .js-pick-period'.format(filter_id)).click()
            # check that popup is visible
            self.assertTrue(driver.find_element_by_css_selector('.dp-container').is_displayed())
            # click 'Cancel'
            driver.find_element_by_css_selector('button.btn-cancel.btn').click()
            self.assertFalse(driver.find_elements_by_css_selector('.dp-container'))

            # check different periods submit
            for dates in self.TEST_DATES:
                # select period
                driver.find_element_by_id("ddcl-{0}".format(filter_id)).click()
                driver.find_element_by_css_selector(
                        '#ddcl-{0}-ddw .js-pick-period'.format(filter_id)).click()
                self.set_datepicker_date(dates['start'], dates['end'])
                # click 'Submin' in custom period popup
                driver.find_element_by_css_selector("button.btn-submit.btn").click()
                # check that displayed right period
                self.check_custom_date('upload_date', dates['res_start'], dates['res_end'])

    def test_custom_last_modified(self):
        """
        1. Open 'By Time Modified' filter
        2. Click on 'Custom period' button
        3. Select period
        4. Clcik 'Submit'
        5. Check that displayed right period as filter value
        """
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            # scroll to 'By Time Modified' filter
            filter_id = get_filter_id(driver, 'last_modified')
            scroll_page_to_filter(driver, filter_id)

            dates = self.TEST_DATES[0]
            # select period
            driver.find_element_by_id("ddcl-{0}".format(filter_id)).click()
            driver.find_element_by_css_selector(
                        '#ddcl-{0}-ddw .js-pick-period'.format(filter_id)).click()
            self.set_datepicker_date(dates['start'], dates['end'])
            # click 'Submin' in custom period popup
            driver.find_element_by_css_selector("button.btn-submit.btn").click()
            # check that displayed right period
            self.check_custom_date('last_modified', dates['res_start'], dates['res_end'])


class DetailsTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", TEST_CACHE_DIR)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml")
        self.selenium = webdriver.Firefox(firefox_profile=fp)
        self.selenium.implicitly_wait(5)
        super(DetailsTestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(DetailsTestCase, self).tearDownClass()

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
                    "//div[@class='bDiv']/table/tbody/tr[1]/td[2]")
        td.click()
        # analysis_id consist in first column
        uuid = driver.find_element_by_xpath(
                    "//div[@class='bDiv']/table/tbody/tr[1]").get_attribute('data-analysis_id')
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
                    "//div[@class='bDiv']/table/tbody/tr[1]/td[1]/div/input"
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
            td = driver.find_element_by_xpath("//div[@class='bDiv']/table/tbody/tr[1]/td[2]")
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
                os.remove(os.path.join(TEST_CACHE_DIR, 'metadata.xml'))
            except OSError:
                pass
            td = driver.find_element_by_xpath("//div[@class='bDiv']/table/tbody/tr[1]/td[2]")
            analysis_id = driver.find_element_by_xpath(
                    "//div[@class='bDiv']/table/tbody/tr[1]").get_attribute('data-analysis_id')
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
                os.remove(os.path.join(TEST_CACHE_DIR, 'metadata.xml'))
            except OSError:
                assert False, "File metadata.xml wasn't downloaded"


class SearchTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SearchTestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(SearchTestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def test_no_results(self):
        """
        Enter bad query, submit, check that not results was found.
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
                    "/html/body/div[2]/div[2]/div[2]").text
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
                    "//*[@id='id_add_files_form']/div[5]/div[1]/div[1]/div[1]/div[4]/table/tbody/tr"))
            self.selenium.find_element_by_link_text("25").click()
            assert 25 == len(self.selenium.find_elements_by_xpath(
                    "//*[@id='id_add_files_form']/div[5]/div[1]/div[1]/div[1]/div[4]/table/tbody/tr"))
            self.selenium.find_element_by_link_text("50").click()
            assert 50 == len(self.selenium.find_elements_by_xpath(
                    "//*[@id='id_add_files_form']/div[5]/div[1]/div[1]/div[1]/div[4]/table/tbody/tr"))

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
                    "//*[@id='id_add_files_form']/div[5]/div[1]/div[1]/div[1]/div[4]/table/tbody/tr"))
            assert 'offset' not in self.selenium.current_url

            # initially 'Prev' and '1' links should be disabled
            prev = self.selenium.find_element_by_link_text('Prev')
            assert not link_state(prev)
            first = self.selenium.find_element_by_link_text('1')
            assert not link_state(first)

            # got to second page
            self.selenium.find_element_by_link_text("2").click()
            assert 10 == len(self.selenium.find_elements_by_xpath(
                    "//*[@id='id_add_files_form']/div[5]/div[1]/div[1]/div[1]/div[4]/table/tbody/tr"))
            # check that url contains offset and limit
            assert 'offset=10&limit=10' in self.selenium.current_url

            found = self.selenium.find_element_by_xpath(
                                    "/html/body/div[2]/div[2]/div[2]")
            pages_count = (int(found.text.split()[1]) / 10) + 1

            # check other pages
            for page in (2, pages_count,):
                self.selenium.find_element_by_link_text(str(page)).click()
                a = self.selenium.find_element_by_link_text(str(page))
                assert not link_state(a)

            # check 'Prev'
            self.selenium.find_element_by_link_text('Prev').click()
            current = self.selenium.find_element_by_link_text(str(pages_count - 1))
            assert not link_state(current)


    def test_sorting_order(self):
        """
        Test that sorting works properly.
        1. Go to search page (default query)
        2. Walk throw table columns
        3. Click on column header to select descending ordering
        4. Get top value in clumn
        5. Click on column header once more to select ascending ordering
        6. Get top value in column and compare in with previous
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
                self.selenium.execute_script("$('.viewport')"
                        ".scrollLeft($('th[axis=col{0}]')"
                        ".position().left);".format(i + 1));
                # after first click element element is asc sorted
                self.selenium.find_element_by_partial_link_text(column).click()

                # getting top element in the column
                selector = ".bDiv > table td:nth-child({})".format(i + 2)
                first = self.selenium.find_element_by_css_selector(selector).text

                # scroll table
                self.selenium.execute_script("$('.viewport')"
                        ".scrollLeft($('th[axis=col{0}]')"
                        ".position().left);".format(i + 1));
                # resort
                self.selenium.find_element_by_partial_link_text(column).click()
                second = self.selenium.find_element_by_css_selector(selector).text
                if not (first == 'None' or second == 'None' or
                        first == ' ' or second == ' '):
                    if column == 'Files Size':
                        # GB == GB, MB == MB, etc.
                        first = back_to_bytes(first)
                        second = back_to_bytes(second)
                        self.assertLessEqual(first, second)
                    else:
                        self.assertLessEqual(first, second)


class ColumnSelectTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(ColumnSelectTestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(ColumnSelectTestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def check_select_columns(self, location):
        """
        Check that displayed columns selection works.
        1. Uncheck all columns one by one
        2. After every click, check that all previous columns are hidden and all next are visible
        3. Also check that last column takes all free space
        4. Click on '(all)'
        5. Check that all columns visible

        :param location: 'search' or 'cart'
        """
        # TODO(nanvel): Add test for default columns

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
                        "#ddcl-1 > span:first-child > span")
        select.click()
        # uncheck one by one
        r = range(column_count)
        for i in r:
            driver.find_element_by_xpath("//label[@for='ddcl-1-i%d']" % (i + 1)).click()
            # check that all previous columns are hidden
            for j in r[:(i + 1)]:
                driver.execute_script("$('.viewport')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % j)
                assert not driver.find_element_by_xpath("//th[@axis='col%d']" % (j + 1)).is_displayed()
            # check that all next columns are visible
            for j in r[(i + 1):]:
                driver.execute_script("$('.viewport')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % j)
                assert driver.find_element_by_xpath("//th[@axis='col%d']" % (j + 1)).is_displayed()
            # check that last column takes all free space
            if i < column_count - 1:
                full_width = driver.find_element_by_class_name('hDiv').value_of_css_property('width')[:-2]
                full_width = int(full_width.split('.')[0])
                all_columns_width = driver.find_element_by_xpath("//th[@axis='col0']").size.get('width', 0)
                for x in range(1, column_count + 1):
                    col = driver.find_element_by_xpath("//th[@axis='col%d']" % x)
                    if col.is_displayed():
                        all_columns_width += col.size.get('width', 0)
                self.assertTrue(full_width - all_columns_width < 3)
        # select (all) option
        driver.find_element_by_xpath("//label[@for='ddcl-1-i0']").click()
        r2 = range(column_count)
        for x in r2:
            driver.execute_script("$('.viewport')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % x)
            assert driver.find_element_by_xpath("//th[@axis='col%d']" % (x + 1)).is_displayed()       
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
            driver.find_element_by_css_selector('input.js-select-all').click()
            driver.find_element_by_css_selector('button.add-to-cart-btn').click()
            time.sleep(5)
            self.check_select_columns('cart')


class ResetFilteTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(ResetFiltersButtonTestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        time.sleep(1)
        self.selenium.quit()
        super(ResetFiltersButtonTestCase, self).tearDownClass()

    def tearDown(self):
        self.selenium.delete_all_cookies()

    # TODO(nanvel): check saving last query here

    def get_selected_filters(self):
        """
        Return selected filters as text.
        '(all)' skipped
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
            filter_id = get_filter_id(driver, filter_name)
            driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(filter_id)).click()
            driver.find_element_by_id("ddcl-{0}-i0".format(filter_id)).click()
            driver.find_element_by_xpath("//label[@for='ddcl-{0}-i1']".format(filter_id)).click()
            driver.find_element_by_xpath("//label[@for='ddcl-{0}-i2']".format(filter_id)).click()
            driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(filter_id)).click()

            # apply filters
            driver.find_element_by_id("id_apply_filters").click()
            self.assertNotEqual(default_filters, self.get_selected_filters())

            # try to reset filters
            driver.find_element_by_id("id_reset_filters").click()
            self.assertEqual(default_filters, self.get_selected_filters())
