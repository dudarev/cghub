import time
import re
import os, shutil
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains

from django.test import LiveServerTestCase
from django.conf import settings
from django.utils import timezone

from wsapi.api import request as api_request


"""
preffered queries (allow using the same cache files):
"6d711*" - returns one result
"6d1*" - for many results

"bad-analysis-id" - bad id
"""


TEST_SETTINGS = dict(
    TABLE_COLUMNS=('Analysis Id', 'State'),
    COLUMN_STYLES={
            'Analysis Id': {
                    'width': 220, 'align': 'left', 'default_state': 'visible'},
            'State': {
                    'width': 70, 'align': 'left', 'default_state': 'visible'}}
)

"""
FIXME(nanvel): maybe simply specify new CACHE_DIR with already existed cache files
"""
def wsapi_cache_copy(cache_files):
    """
    Copy cache_files from TEST_DATA_DIR to WSAPI_CACHE_DIR
    In case of cart_cache, it should be generated every time,
    but it will use wsapi cache.
    """
    TEST_DATA_DIR = 'cghub/test_data/'
    if not os.path.exists(settings.WSAPI_CACHE_DIR):
        os.makedirs(settings.WSAPI_CACHE_DIR)
    for f in cache_files:
        shutil.copy(
            os.path.join(TEST_DATA_DIR, f),
            os.path.join(settings.WSAPI_CACHE_DIR, f)
        )


def wsapi_cache_remove(cache_files):
    """
    Remove cache_files from WSAPI_CACHE_DIR
    """
    for f in cache_files:
        path = os.path.join(settings.WSAPI_CACHE_DIR, f)
        if os.path.exists(path):
            os.remove(path)


def cart_cache_remove(cache_files):
    """
    Remove cache_files from CART_CACHE_DIR
    """
    for f in cache_files:
        path = os.path.join(settings.CART_CACHE_DIR, f)
        if os.path.isdir(path):
            shutil.rmtree(path)


def back_to_bytes(*args):
    """
    Converts File Size back to bytes for comparing purposes
    """
    files = [str(ar) for ar in args]
    result = []
    for file_name in files:
        float_result = float(file_name.split(' ')[0].replace(',', '.'))
        if file_name.endswith('GB'):
            result.append(float_result * 1073741824.)
        elif file_name.endswith('MB'):
            result.append(float_result * 1048576.)
        elif file_name.endswith('KB'):
            result.append(float_result * 1024.)
        else:
            result.append()
    # FIXME(nanvel): why tuple returns
    return result[0], result[1]


def get_filter_id(driver, filter_name):
    """
    Helper function for getting sidebar filter id.
    Makes filter tests easier to maintain.
    """
    el = driver.find_element_by_css_selector("select[data-section='{0}'] + span".format(filter_name))
    el_id = el.get_attribute('id').split('-')[-1]
    # FIXME(nanvel): check this
    driver.execute_script(
            "$(window).scrollTop($('#ddcl-{0}').offset().top - 100);".format(el_id))
    return el_id


class SidebarTestCase(LiveServerTestCase):
    wsapi_cache_files = (
                'f87f34ec002eff67850c644d09bf6f80.ids',
                '71411da734e90beda34360fa47d88b99.ids',
                )

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        # FIXME(nanvel): maybe possible decrease it or use in other tests
        # http://selenium-python.readthedocs.org/en/latest/api.html#selenium.webdriver.remote.webdriver.implicitly_wait
        self.selenium.implicitly_wait(5)
        super(SidebarTestCase, self).setUpClass()
        wsapi_cache_copy(self.wsapi_cache_files)

    def test_select_all(self):
        """
        1. Open 'By Center' filter (Selected all items by default)
        2. Click on '(all)'
        3. Check that all checkboxes unchecked
        4. Click on '(all)'
        5. Check that all checkboxes checked
        """
        # FIXME(nanvel): check that uploaded small amount of data
        driver = self.selenium
        driver.get(self.live_server_url)

        center_id = get_filter_id(driver, 'center_name')
        self.selenium.find_element_by_id("ddcl-{0}".format(center_id)).click()

        # by center has 8 centers, i0 - deselect all, i1-i7 - selections
        # click on 'All' to deselect all and check that no one selected
        driver.find_element_by_id("ddcl-{0}-i0".format(center_id)).click()
        for i in range(1, 8):
            cb = driver.find_element_by_id("ddcl-{0}-i{1}".format(center_id, i))
            self.assertFalse(cb.is_selected())

        # click again - select all
        # check that all centers selected
        driver.find_element_by_id("ddcl-{0}-i0".format(center_id)).click()
        for i in range(1, 8):
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
        # FIXME(nanvel): check that uploaded small amount of data (maybe using custom settings for tests will fix this)
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
        Select filters, click on submit, check query
        1. Open 'By Study' filter, unselect all
        2. Select first item (phs000178)
        3. Open 'By Center' filter, unselect all
        4. Select first 3 items (BCM, BCCAGSC, BI)
        5. Open 'By Sample Type' filter, unselect all
        6. Select first 3 options (10, 12, 20)
        7. Open 'By Disease' filter, unselect all
        8. Select first 3 items (LAML, BLCA, LGG)
        9. Open 'By Experiment Type' filter, unselect all
        10. Select first 3 items (D, H, R)
        11. Open 'By Library Type' filter, unselect all
        12. Select first 3 options (Bisulfite-Seq, OTHER, RNA-Seq)
        13. Open 'By Assembly' filter, unselect all
        14. Select fist option (NCBI36*+OR+HG18*)
        15. Open 'By State' filter (live by default)
        16. Select all, unselect all, select 1,2,5 options (bad_data, live, validating_sample)
        17. Click on 'Apply filters'
        18. Check that only selected filters options exists in url
        
        """
        # FIXME: add filter by platform
        driver = self.selenium
        driver.get(self.live_server_url)

        # study: phs000178
        # FIXME(nanvel): for now not all options selected by default, should work right after using custom settings for tests
        study_id = get_filter_id(driver, 'study')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(study_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(study_id)).click()
        driver.find_element_by_id("ddcl-{0}-i1".format(study_id)).click()
        # and close filter DDCL
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:last-child > span".format(study_id)).click()

        # center: BCM+OR+BCCAGSC+OR+BI
        center_id = get_filter_id(driver, 'center_name')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(center_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(center_id)).click()
        driver.find_element_by_id("ddcl-{0}-i1".format(center_id)).click()
        driver.find_element_by_id("ddcl-{0}-i2".format(center_id)).click()
        driver.find_element_by_id("ddcl-{0}-i3".format(center_id)).click()
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:last-child > span".format(center_id)).click()

        # sample type: 10+OR+12+OR+20
        sample_type_id = get_filter_id(driver, 'sample_type')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(sample_type_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(sample_type_id)).click()
        driver.find_element_by_id("ddcl-{0}-i1".format(sample_type_id)).click()
        driver.find_element_by_id("ddcl-{0}-i2".format(sample_type_id)).click()
        driver.find_element_by_id("ddcl-{0}-i3".format(sample_type_id)).click()
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:last-child > span".format(sample_type_id)).click()

        # disease_abbr: LAML+OR+BLCA+OR+LGG'
        disease_abbr_id = get_filter_id(driver, 'disease_abbr')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(disease_abbr_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(disease_abbr_id)).click()
        driver.find_element_by_id("ddcl-{0}-i1".format(disease_abbr_id)).click()
        driver.find_element_by_id("ddcl-{0}-i2".format(disease_abbr_id)).click()
        driver.find_element_by_id("ddcl-{0}-i3".format(disease_abbr_id)).click()
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:last-child > span".format(disease_abbr_id)).click()

        # analyte_code (By Experiment Type): D+OR+H+OR+R
        analyte_code_id = get_filter_id(driver, 'analyte_code')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(analyte_code_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(analyte_code_id)).click()
        driver.find_element_by_id("ddcl-{0}-i1".format(analyte_code_id)).click()
        driver.find_element_by_id("ddcl-{0}-i2".format(analyte_code_id)).click()
        driver.find_element_by_id("ddcl-{0}-i3".format(analyte_code_id)).click()
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:last-child > span".format(analyte_code_id)).click()

        # library_strategy (Library Type): Bisulfite-Seq+OR+OTHER+OR+RNA-Seq
        library_strategy_id = get_filter_id(driver, 'library_strategy')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(library_strategy_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(library_strategy_id)).click()
        driver.find_element_by_id("ddcl-{0}-i1".format(library_strategy_id)).click()
        driver.find_element_by_id("ddcl-{0}-i2".format(library_strategy_id)).click()
        driver.find_element_by_id("ddcl-{0}-i3".format(library_strategy_id)).click()
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:last-child > span".format(library_strategy_id)).click()

        # refassem_short_name (By Assembly): NCBI36*+OR+HG18*
        refassem_short_name_id = get_filter_id(driver, 'refassem_short_name')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(refassem_short_name_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(refassem_short_name_id)).click()
        driver.find_element_by_id("ddcl-{0}-i1".format(refassem_short_name_id)).click()
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:last-child > span".format(refassem_short_name_id)).click()

        # state: bad_data+OR+live+OR+validating_sample
        state_id = get_filter_id(driver, 'state')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(state_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(state_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(state_id)).click()
        driver.find_element_by_id("ddcl-{0}-i1".format(state_id)).click()
        driver.find_element_by_id("ddcl-{0}-i2".format(state_id)).click()
        driver.find_element_by_id("ddcl-{0}-i5".format(state_id)).click()
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:last-child > span".format(state_id)).click()

        # submit form
        driver.find_element_by_id("id_apply_filters").click()

        # check that all selected filters options exists in url
        url = driver.current_url
        # study: phs000178
        self.assertTrue('phs000178' in url)
        self.assertFalse('TCGA_MUT_BENCHMARK_4' in url)
        # center: BCM+OR+BCCAGSC+OR+BI
        self.assertTrue(
            'BCM' in url and
            'BCCAGSC' in url and
            'BI' in url)
        self.assertFalse(
            'UNC-LCCC' in url)
        # sample type: 10+OR+12+OR+20
        self.assertTrue(
            re.match('.*sample_type=[^&]*10', url) and
            re.match('.*sample_type=[^&]*12', url) and
            re.match('.*sample_type=[^&]*20', url))
        self.assertFalse(
            re.match('.*sample_type=[^&]*14', url))
        # disease_abbr: LAML+OR+BLCA+OR+LGG
        self.assertTrue(
            re.match('.*disease_abbr=[^&]*LAML', url) and
            re.match('.*disease_abbr=[^&]*BLCA', url) and
            re.match('.*disease_abbr=[^&]*LGG', url))
        self.assertFalse(
            re.match('.*disease_abbr=[^&]*GBM', url))
        # analyte_code: D+OR+H+OR+R
        self.assertTrue(
            re.match('.*analyte_code=[^&]*D', url) and
            re.match('.*analyte_code=[^&]*H', url) and
            re.match('.*analyte_code=[^&]*R', url))
        self.assertFalse(
            re.match('.*analyte_code=[^&]*T', url))
        # library_strategy: Bisulfite-Seq+OR+OTHER+OR+RNA-Seq
        self.assertTrue(
            re.match('.*library_strategy=[^&]*Bisulfite-Seq', url) and
            re.match('.*library_strategy=[^&]*OTHER', url) and
            re.match('.*library_strategy=[^&]*RNA-Seq', url))
        self.assertFalse(
            re.match('.*library_strategy=[^&]*WXS', url))
        # refassem_short_name: NCBI36*+OR+HG18*
        self.assertTrue(
            re.match('.*refassem_short_name=[^&]*NCBI36*', url) and
            re.match('.*refassem_short_name=[^&]*HG18*', url))
        self.assertFalse(
            re.match('.*refassem_short_name=[^&]*GRCh37*', url))
        # state: live+OR+submitted+OR+bad_data
        self.assertTrue(
            re.match('.*state=[^&]*bad_data', url) and
            re.match('.*state=[^&]*submitted', url) and
            re.match('.*state=[^&]*live', url))
        self.assertFalse(
            re.match('.*state=[^&]*uploading', url))
        # FIXME(nanvel): add filter by platform (after custom settings for tests will be implemented)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SidebarTestCase, self).tearDownClass()
        wsapi_cache_remove(self.wsapi_cache_files)


# FIXME(nanvel): rename this testcase ?
class CustomDatepickersTestCase(LiveServerTestCase):

    wsapi_cache_files = (
        '71411da734e90beda34360fa47d88b99.ids',
        '0036c3926adab0f1ec1af6a76ae0a3d0.ids'
        )

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(CustomDatepickersTestCase, self).setUpClass()
        wsapi_cache_copy(self.wsapi_cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(CustomDatepickersTestCase, self).tearDownClass()
        wsapi_cache_remove(self.wsapi_cache_files)

    def set_datepicker_date(self, start, end, year=None, month=None):
        """
        Select start and end dates in custom period popup
        """
        driver = self.selenium
        dp_start = driver.find_element_by_id('dp-start')
        dp_end = driver.find_element_by_id('dp-end')
        if year:
            dp_start.find_element_by_css_selector('.ui-datepicker-year').click()
            dp_start.find_element_by_css_selector("option[value='{0}']".format(year)).click()
            dp_end.find_element_by_css_selector('.ui-datepicker-year').click()
            dp_end.find_element_by_css_selector("option[value='{0}']".format(year)).click()
        if month or month == 0:
            dp_start.find_element_by_css_selector('.ui-datepicker-month').click()
            dp_start.find_element_by_css_selector("option[value='{0}']".format(month)).click()
            dp_end.find_element_by_css_selector('.ui-datepicker-month').click()
            dp_end.find_element_by_css_selector("option[value='{0}']".format(month)).click()
        dp_start.find_element_by_link_text("{}".format(start)).click()
        dp_end.find_element_by_link_text("{}".format(end)).click()

    def check_custom_date(
            self, filter_name, dp_values, reverse=False, future=False):
        """
        Check that right date displayed in specified date filter.

        :param filter_name: 'last_modified' or 'upload_date'
        :param dp_values: for example {'start': 31, 'end': 31, 'month': 11, 'year': 2013}
        :param reverse: if True - swap start and end values
        :param future: set dates from yesterday to now
        """
        # FIXME(nanvel): is future really usefull ?
        # FIXME(nanvel): fails when today is last day of mnth
        driver = self.selenium
        filter_id = get_filter_id(driver, filter_name)

        dp_values = dict(dp_values)
        if reverse:
            tmp = dp_values['start']
            dp_values['start'] = dp_values['end']
            dp_values['end'] = tmp
        elif future:
            dp_values['start'] = timezone.now().date().day - 1
            dp_values['end'] = timezone.now().date().day
            dp_values['month'] = timezone.now().date().month
        else:
            dp_values['month'] += 1
        # add forward zero for dates and months with values from 1 to 9
        for key in dp_values:
            if len(str(dp_values[key])) == 1:
                 dp_values[key] = '0' + str(dp_values[key])

        # Check custom date is displayed in filter input
        filter_input = driver.find_element_by_id("ddcl-{0}".format(filter_id))
        filter_text = filter_input.find_element_by_css_selector(
                                    '.ui-dropdownchecklist-text').text
        # FIXME(nanvel): month and year can be different
        text = "{0}/{1}/{2} - {0}/{1}/{3}".format(
            dp_values['year'], dp_values['month'],
            dp_values['start'], dp_values['end'])
        assert text in filter_text.strip()

    # FIXME(nanvel): merge this 3 tests in one
    # And create 2 tests: one for upload_date (full) and one for last_modified (superficially)

    def test_custom_datepickers_future_date(self):
        """
        1. Go to main page
        2. Open 'By Upload Time filter'
        3. Click 'Pick period', check that custom period form visible
        4. Click 'Cancel' in the form, check that form invisible
        5. Click 'Pick Period', select date
        6. Click 'Submit' in the custom period form
        7. Check that in 'By Upload Date' filter displayed right date
        8. Open 'By Time Modified' filter
        9. Click 'Pick Period', select date
        10. Click 'Submit' in the custom period form
        11. Check that in 'By Time Modified' filter displayed right date
        """
        driver = self.selenium
        driver.get(self.live_server_url)
        # we shouldn't use dates near the end or beginning of month
        dp_values = {
            'start': 15, 'end': 15, 'month': 11,
            'year': timezone.now().date().year}
        last_modified_id = get_filter_id(driver, 'last_modified')
        upload_date_id = get_filter_id(driver, 'upload_date')
        # FIXME(nanvel): We shoudnt use analyte_code here only to move screen
        analyte_code_id = get_filter_id(driver, 'analyte_code')

        driver.execute_script(
            "$('body').scrollTop($('#ddcl-{0}').position().top);".format(
                analyte_code_id))

        # -- open custom perio popup and than cloase it
        # open 'By Upload Time' filter
        driver.find_element_by_id("ddcl-{0}".format(upload_date_id)).click()
        # click 'Pick period'
        driver.find_element_by_css_selector(
                '#ddcl-{0}-ddw .js-pick-period'.format(upload_date_id)).click()
        # FIXME(nanvel): check that custom period form visible
        # click 'Cancel'
        driver.find_element_by_css_selector("button.btn-cancel.btn").click()
        # FIXME(nanvel): check that custom period popup closed

        # open 'By Upload Time' filter
        driver.find_element_by_id("ddcl-{0}".format(upload_date_id)).click()
        # click 'Pick period'
        driver.find_element_by_css_selector(
                '#ddcl-{0}-ddw .js-pick-period'.format(upload_date_id)).click()
        # set dates
        self.set_datepicker_date(
                dp_values['start'], dp_values['end'], dp_values['month'])
        # click 'Submin' in custom period popup
        driver.find_element_by_css_selector("button.btn-submit.btn").click()
        # check selected date
        self.check_custom_date('upload_date', dp_values, future=True)

        # the same for last_modified (By Time Modified)
        # FIXME(nanvel): we can test last_modified superficially
        driver.find_element_by_id("ddcl-{0}".format(last_modified_id)).click()
        driver.find_element_by_css_selector(
                '#ddcl-{0}-ddw .js-pick-period'.format(last_modified_id)).click()
        self.set_datepicker_date(
                dp_values['start'], dp_values['end'], dp_values['month'])
        driver.find_element_by_css_selector("button.btn-submit.btn").click()
        # check selected date
        # FIXME(nanvel): should be used different days for last_modified and upload_time,
        # to catch cases when one custom period form cange both filters values
        self.check_custom_date('last_modified', dp_values, future=True)

    def test_custom_datepickers_wrong_date(self):
        # FIXME(nanvel): should be merged in one function
        driver = self.selenium
        driver.get(self.live_server_url)
        dp_values = {
            'start': 2, 'end': 1,
            'year': timezone.now().date().year,
            'month': timezone.now().date().month}

        last_modified_id = get_filter_id(driver, 'last_modified')
        upload_date_id = get_filter_id(driver, 'upload_date')
        analyte_code_id = get_filter_id(driver, 'analyte_code')

        driver.execute_script(
            "$('body').scrollTop($('#ddcl-{0}').position().top);".format(
                analyte_code_id))

        driver.find_element_by_id("ddcl-{0}".format(upload_date_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(upload_date_id)).click()
        driver.find_element_by_css_selector("button.btn-cancel.btn").click()

        driver.find_element_by_id("ddcl-{0}".format(upload_date_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(upload_date_id)).click()
        self.set_datepicker_date(dp_values['start'], dp_values['end'])
        driver.find_element_by_css_selector("button.btn-submit.btn").click()

        driver.find_element_by_id("ddcl-{0}".format(last_modified_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(last_modified_id)).click()
        driver.find_element_by_css_selector("button.btn-cancel.btn").click()

        driver.find_element_by_id("ddcl-{0}".format(last_modified_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(last_modified_id)).click()
        self.set_datepicker_date(dp_values['start'], dp_values['end'])
        driver.find_element_by_css_selector("button.btn-submit.btn").click()
        self.check_custom_date('upload_date', dp_values, reverse=True)
        self.check_custom_date('last_modified', dp_values, reverse=True)

    def test_custom_datepickers_right_date(self):
        # FIXME(nanvel): should be merged in one function
        driver = self.selenium
        driver.get(self.live_server_url)
        dp_values = {
            'start': 1, 'end': 2,
            'year': 2012, 'month': 0}

        last_modified_id = get_filter_id(driver, 'last_modified')
        upload_date_id = get_filter_id(driver, 'upload_date')
        analyte_code_id = get_filter_id(driver, 'analyte_code')

        driver.execute_script(
            "$('body').scrollTop($('#ddcl-{0}').position().top);".format(
                analyte_code_id))

        driver.find_element_by_id("ddcl-{0}".format(upload_date_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(upload_date_id)).click()
        self.set_datepicker_date(dp_values['start'], dp_values['end'], dp_values['year'], dp_values['month'])
        driver.find_element_by_css_selector("button.btn-submit.btn").click()

        driver.find_element_by_id("ddcl-{0}".format(last_modified_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(last_modified_id)).click()
        self.set_datepicker_date(dp_values['start'], dp_values['end'], dp_values['year'], dp_values['month'])
        driver.find_element_by_css_selector("button.btn-submit.btn").click()
        self.check_custom_date('upload_date', dp_values)
        self.check_custom_date('last_modified', dp_values)

        driver.execute_script(
            "$('body').scrollTop($('#id_apply_filters').position().top);")
        driver.find_element_by_id("id_apply_filters").click()

        applied_filters = driver.find_element_by_css_selector('.applied-filters')
        assert 'Uploaded' in applied_filters.text
        assert 'Modified' in applied_filters.text


class HelpHintsTestCase(LiveServerTestCase):

    wsapi_cache_files = ('71411da734e90beda34360fa47d88b99.ids',)

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(HelpHintsTestCase, self).setUpClass()
        wsapi_cache_copy(self.wsapi_cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(HelpHintsTestCase, self).tearDownClass()
        wsapi_cache_remove(self.wsapi_cache_files)

    def test_help_hints(self):
        driver = self.selenium
        with self.settings(HELP_HINTS = { 'Study': 'Help for Study'}):
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


class DetailsTestCase(LiveServerTestCase):

    wsapi_cache_files = (
        '71411da734e90beda34360fa47d88b99.ids',
        '9aa43640de03f3d47f87c21ef1a35ee5.xml',
        )
    cart_cache_files = (
        '0b8eae89-0af1-45b7-9b97-ea1fdeaf3890',
    )

    @classmethod
    def setUpClass(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", settings.WSAPI_CACHE_DIR)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml")
        self.selenium = webdriver.Firefox(firefox_profile=fp)
        self.selenium.implicitly_wait(5)
        super(DetailsTestCase, self).setUpClass()
        wsapi_cache_copy(self.wsapi_cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(DetailsTestCase, self).tearDownClass()
        wsapi_cache_remove(self.wsapi_cache_files)
        cart_cache_remove(self.cart_cache_files)

    def check_popup_shows(self, driver):
        ac = ActionChains(driver)
        # test clicking on row leads to details popup opening
        popup = driver.find_element_by_css_selector('#itemDetailsModal')
        assert not popup.is_displayed()
        td = driver.find_element_by_xpath(
            "//div[@class='bDiv']/table/tbody/tr[{0}]/td[{1}]".format(1, 2))
        td.click()
        uuid = driver.find_element_by_xpath(
            "//div[@class='bDiv']/table/tbody/tr[{0}]/td[2]".format(1)).text
        time.sleep(4)
        popup = driver.find_element_by_css_selector('#itemDetailsModal')
        assert popup.is_displayed()
        assert uuid in driver.find_element_by_css_selector('#details-label').text
        driver.find_element_by_xpath("//button[@data-dismiss='modal']").click()
        time.sleep(1)
        # test clicking on 'Details' option from context menu leads to details popup opening
        context_menu = driver.find_element_by_css_selector('#table-context-menu')
        assert not context_menu.is_displayed()
        popup = driver.find_element_by_css_selector('#itemDetailsModal')
        time.sleep(1)
        assert not popup.is_displayed()
        ac.context_click(td)
        ac.perform()
        context_menu = driver.find_element_by_css_selector('#table-context-menu')
        assert context_menu.is_displayed()
        driver.find_element_by_css_selector('.js-details-popup').click()
        popup = driver.find_element_by_css_selector('#itemDetailsModal')
        assert popup.is_displayed()
        driver.find_element_by_css_selector(".modal-footer .btn").click()

    # FIXME: broke after changes in filters_storage_full
    '''
    def test_details_popups(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        self.check_popup_shows(driver)
        driver.find_element_by_xpath(
                "//div[@class='bDiv']/table/tbody/tr[{0}]/td[1]/div/input".format(1)
                ).click()
        driver.find_element_by_css_selector('.add-to-cart-btn').click()
        time.sleep(4)
        self.check_popup_shows(driver)
    '''

    def test_xml_display(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        td = driver.find_element_by_xpath("//div[@class='bDiv']/table/tbody/tr[1]/td[2]")
        td.click()
        time.sleep(3)
        driver.execute_script(
            "$('.modal-body').scrollTop($('.raw-xml-link').position().top);")
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
        with self.settings(**TEST_SETTINGS):
            driver = self.selenium
            driver.get(self.live_server_url)
            try:
                os.remove(settings.WSAPI_CACHE_DIR + 'metadata.xml')
            except OSError:
                pass
            td = driver.find_element_by_xpath("//div[@class='bDiv']/table/tbody/tr[1]/td[2]")
            td_text = driver.find_element_by_xpath(
                "//div[@class='bDiv']/table/tbody/tr[1]/td[2]").text
            ac = ActionChains(driver)
            ac.context_click(td)
            ac.perform()
            driver.find_element_by_css_selector('.js-details-page').click()
            time.sleep(5)
            driver.switch_to_window(driver.window_handles[-1])
            page_header = driver.find_element_by_class_name('page-header').text
            assert (td_text in driver.current_url and 'details' in driver.current_url)
            assert (td_text in page_header and 'details' in page_header)
            driver.execute_script(
                "$(window).scrollTop($('#id-download-metadata').offset().top - 100);")
            # try to load analysis xml
            driver.find_element_by_id('id-download-metadata').click()
            time.sleep(3)
            try:
                os.remove(settings.WSAPI_CACHE_DIR + 'metadata.xml')
            except OSError:
                assert False, "File metadata.xml wasn't downloaded"


class SearchTestCase(LiveServerTestCase):

    wsapi_cache_files = (
        '71411da734e90beda34360fa47d88b99.ids', '7483974d8235868e5d4d2079d5051332.xml',
        '714f182ce3b2196b3b064880493e242d.xml', 'c0db6ab7b80ded4f9211570170011d80.xml',
        '754c3dc8c582013011f0028a6f78e0d4.xml', 'e0004ef23a2e10e42ac402db10ac0535.xml',
        'faf6e2f16239b6b844226ab83bb98756.xml',
        '7bf8d051308235f7b2aff34391303113.xml', 'ca3707b0c52ca54d2d264d9f8b122c28.xml',
        'd83fe04980a423f672ed63c39d4a86dd.xml',
        '39983600179929edc5cba726704dfbb8.xml', 'dcc000923be4973a3a201f65bc9d86fb.xml',
        'f1db42e28cca7a220508b4e9778f66fc.xml',
        '3f7b84aaa3c17cdade74e151d5d67d48.xml', '630a979741b05f755ed83591703c38aa.xml',
        '707ffa5e53cbc239ee358240839177c2.xml',
        '0ccd7cf2c00f026998262840d940d485.ids', '682ca432dc8f4a85bc70d89d10ef64b1.ids', 
        'af5eb9d62e2bafda2eb3bad59afa5b2d.ids', '12b0c26f18006e39b45d135ff626148f.ids',
        '695f8c090ce677d51b3184e721e90198.ids', 'b02bb4f82cb336d7d7ad0f512c17a879.ids',
        '194a167248e69ab52f7984f251423eb3.ids', '6a5d605d38e701a14bf16c094333bab2.ids',
        'b50de5c4b4c0fd0cd0c2b4c91409a45a.ids', '28e1cf619d26bdab58fcab5e7a2b9e6c.ids',
        '6f55a35e4a0aa854110317a459f46a63.ids', 'bf8267e82f09bc70cebd0179ae04222b.ids',
        '2b2cddbe3555451285e826c410598f8d.ids', '7169b446f2c2a0f3824ff54748f2279c.ids',
        'c410977da1ca1a9d10f79e5c106a87e7.ids', '2b59cdba32158d41e96292263e080c9a.ids',
        '71a961a423dea25d42e06ab2c015334d.ids', 'e9284a03bf4b46354cc645abd7eba129.ids',
        '3fe0137f1c7df05124508e503ff18c27.ids', '8211bfd303398c83fd6266268772a0f6.ids',
        'ef7e8c3d4403a0d52a09d49d7c5b903b.ids', '422c90827750a69a42d4035b9aae6899.ids',
        '87b817c0c86c91c11246b9f241ce40c9.ids', 'efbff930fa0a2423d282c4e71700ca74.ids',
        '63b0dd56b1ceaa4d191e5033fbcecbc5.ids', 'a3204a04d92154d37de73b1be4959c5e.ids',
        'f5aa9c674cf08d95920510a239babbcb.ids'
    )

    query = "6d5*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SearchTestCase, self).setUpClass()
        wsapi_cache_copy(self.wsapi_cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SearchTestCase, self).tearDownClass()
        wsapi_cache_remove(self.wsapi_cache_files)

    def tearDown(self):
        self.selenium.delete_all_cookies()

    def search(self, text="6d1*"):
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys(text)
        element.submit()

    def test_no_results(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys("some text")
        element.submit()
        time.sleep(2)
        result = self.selenium.find_element_by_xpath(
            "//div[contains(@class,'base-container')]/div/h4")
        assert result.text == "No results found."

    def test_url(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys("6d71test")
        element.submit()
        time.sleep(2)
        assert "/search/?q=6d71test" in self.selenium.current_url

    def test_search_result(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys("6d711*")
        element.submit()
        time.sleep(5)
        assert "Found" in self.selenium.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]").text

    def test_count_pages(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys("6d1*")
        element.submit()
        time.sleep(3)
        self.selenium.find_element_by_link_text("25").click()
        assert 25 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[1]/div[1]/div[1]/div[4]/table/tbody/tr"))
        self.selenium.find_element_by_link_text("50").click()
        assert 50 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[1]/div[1]/div[1]/div[4]/table/tbody/tr"))

    def test_pagination(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys("6d1*")
        element.submit()
        time.sleep(5)
        assert "Found" in self.selenium.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]").text
        assert 10 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[1]/div[1]/div[1]/div[4]/table/tbody/tr"))
        self.selenium.find_element_by_link_text("2").click()
        assert 10 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[1]/div[1]/div[1]/div[4]/table/tbody/tr"))

    # FIXME: broke after changes in filters_storage_full
    '''
    def test_filtering_shown(self):
        self.selenium.get(self.live_server_url)

        # unselect all in Center
        center_id = get_filter_id(self.selenium, 'center_name')
        self.selenium.execute_script("$('#ddcl-{0}').click()".format(center_id))
        self.selenium.execute_script("$('#ddcl-{0}-i0').click()".format(center_id))
        self.selenium.execute_script("$('#ddcl-{0}-i0').click()".format(center_id))
        # select Baylor and Harvard
        self.selenium.execute_script("$('#ddcl-{0}-i1').click()".format(center_id))
        self.selenium.execute_script("$('#ddcl-{0}-i4').click()".format(center_id))

        # unselect all in Assembly
        assembly_id = get_filter_id(self.selenium, 'refassem_short_name')
        self.selenium.execute_script("$('#ddcl-{0}').click()".format(assembly_id))
        self.selenium.execute_script("$('#ddcl-{0}-i0').click()".format(assembly_id))
        self.selenium.execute_script("$('#ddcl-{0}-i0').click()".format(assembly_id))
        # select NCBI36/HG18
        self.selenium.execute_script("$('#ddcl-{0}-i1').click()".format(assembly_id))

        self.search()

        # check filters is shown
        filter = (self.selenium.find_element_by_css_selector(
            "#ddcl-{0} > span:first-child > span".format(center_id)))
        self.assertEqual(filter.text, u'Baylor\nHarvard')
        
        filter2 = (self.selenium.find_element_by_css_selector(
            "#ddcl-{0} > span:first-child > span".format(assembly_id)))
        self.assertEqual(filter2.text, u'NCBI36/HG18')
    '''

    def test_pagination_links(self):
        self.selenium.get(self.live_server_url)
        self.search("6d1*")

        found = (self.selenium.find_element_by_css_selector(
            ".base-content > div:nth-child(2)"))
        try:
            page_count = (int(found.text.split()[1]) / 10) + 1
        except:
            page_count = None

        if page_count:
            # initially 'Prev' and '1' links should be disabled
            prev = self.selenium.find_element_by_link_text('Prev')
            self.__link_is_disabled(prev)
            first = self.selenium.find_element_by_link_text('1')
            self.__link_is_active(first)

            # check other pages
            for page_num in (2, 3, page_count):
                self.selenium.find_element_by_link_text(str(page_num)).click()
                a = self.selenium.find_element_by_link_text(str(page_num))
                self.__link_is_active(a)

            # 'Next' link should be disabled in case when last page selected
            next = self.selenium.find_element_by_link_text('Next')
            self.__link_is_disabled(next)

            # check 'Prev'
            self.selenium.find_element_by_link_text('Prev').click()
            current = self.selenium.find_element_by_link_text(str(page_num - 1))
            self.__link_is_active(current)

            # check 'Next'
            self.selenium.find_element_by_link_text('Next').click()
            current = self.selenium.find_element_by_link_text(str(page_num))
            self.__link_is_active(current)

    def __parent_has_class(self, child, class_name):
        parent = child.find_element_by_xpath("..")
        self.assertEqual(u'{}'.format(class_name),
                         parent.get_attribute('class'))

    def __link_is_disabled(self, link):
        self.__parent_has_class(link, 'disabled')

    def __link_is_active(self, link):
        self.__parent_has_class(link, 'active')

    def test_sorting_order(self):
        columns = [
                    'Analysis Id', 'Study', 'Disease', 'Disease Name',
                    'Library Type', 'Assembly', 'Center',
                    'Center Name', 'Experiment Type', 'Uploaded',
                    'Modified', 'Sample Type', 'Sample Type Name', 
                    'State', 'Barcode', 'Sample Accession', 'Files Size'
        ]
        self.selenium.get(self.live_server_url)
        for i, column in enumerate(columns):
            if i in (3, 7, 11):
                continue
            # scroll table
            self.selenium.execute_script("$('.viewport')"
                        ".scrollLeft($('th[axis=col{0}]')"
                        ".position().left);".format(i + 1));
            # after first click element element is asc sorted
            self.selenium.find_element_by_partial_link_text(column).click()

            # getting first element in column
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
                    first, second = back_to_bytes(first, second)
                    self.assertLessEqual(first, second)
                else:
                    self.assertLessEqual(first, second)


class ColumnSelectTestCase(LiveServerTestCase):
    wsapi_cache_files = (
                '862628620de0b3600cbaa8c11d92a4a2.xml',
                'c819df02cad704f9d074e73d322cb319.xml',
                '862e15fcf25b3882bb5c58e3a96026da.xml',
                )
    cart_cache_files = (
                'c7e49b79-2f7d-1584-e040-ad451e410b1c',
    )
    query = "6d711*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(ColumnSelectTestCase, self).setUpClass()
        wsapi_cache_copy(self.wsapi_cache_files)
        lxml = api_request(file_name=settings.WSAPI_CACHE_DIR + self.wsapi_cache_files[0])._lxml_results
        self.items_count = lxml.Hits

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(ColumnSelectTestCase, self).tearDownClass()
        wsapi_cache_remove(self.wsapi_cache_files)
        cart_cache_remove(self.cart_cache_files)

    def select_columns(self, driver, location):
        time.sleep(2)
        column_count = len(driver.find_elements_by_xpath("//div[@class='hDivBox']/table/thead/tr/th")) - 1
        # Find select on search or cart page
        if location == 'search':
            select = driver.find_element_by_xpath("//form[@id='id_add_files_form']/span/span\
                /span[@class='ui-dropdownchecklist-text']")
        elif location == 'cart':
            select = driver.find_element_by_css_selector("#ddcl-1 > span:first-child > span")
        select.click()
        # Unselecting one by one
        r = range(column_count)
        for i in r:
            driver.find_element_by_xpath("//label[@for='ddcl-1-i%d']" % (i + 1)).click()
            for j in r[:(i + 1)]:
                driver.execute_script("$('.viewport')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % j)
                assert not driver.find_element_by_xpath("//th[@axis='col%d']" % (j + 1)).is_displayed()
            for j in r[(i + 1):]:
                driver.execute_script("$('.viewport')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % j)
                assert driver.find_element_by_xpath("//th[@axis='col%d']" % (j + 1)).is_displayed()
            # Check that last column takes all free space
            if i < column_count - 1:
                full_width = driver.find_element_by_class_name('hDiv').value_of_css_property('width')[:-2]
                full_width = int(full_width.split('.')[0])
                all_columns_width = driver.find_element_by_xpath("//th[@axis='col0']").size.get('width', 0)
                for x in range(1, column_count + 1):
                    col = driver.find_element_by_xpath("//th[@axis='col%d']" % x)
                    if col.is_displayed():
                        all_columns_width += col.size.get('width', 0)
                self.assertTrue(full_width - all_columns_width < 3)
        # Select (all) option
        driver.find_element_by_xpath("//label[@for='ddcl-1-i0']").click()
        r2 = range(column_count)
        for x in r2:
            driver.execute_script("$('.viewport')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % x)
            assert driver.find_element_by_xpath("//th[@axis='col%d']" % (x + 1)).is_displayed()
            driver.find_element_by_xpath("//label[@for='ddcl-1-i%d']" % (x + 1)).click()        
        driver.find_element_by_xpath("//label[@for='ddcl-1-i0']").click()
        select.click()

    # FIXME: broke after changes in filters_storage_full
    '''
    def test_column_select(self):
        driver = self.selenium
        driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

        self.select_columns(driver, 'search')
        driver.find_element_by_css_selector('input.js-select-all').click()
        driver.find_element_by_css_selector('button.add-to-cart-btn').click()
        time.sleep(2)
        self.select_columns(driver, 'cart')
    '''


class ResetFiltersButtonTestCase(LiveServerTestCase):
    wsapi_cache_files = (
                '71411da734e90beda34360fa47d88b99.ids',
                'ab111b55fd90876ca6d64f2e79d8a338.ids',
                'f5aa9c674cf08d95920510a239babbcb.ids')

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(ResetFiltersButtonTestCase, self).setUpClass()
        wsapi_cache_copy(self.wsapi_cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(ResetFiltersButtonTestCase, self).tearDownClass()
        wsapi_cache_remove(self.wsapi_cache_files)

    # FIXME: broke after changes in filters_storage_full
    '''
    def test_reset_filters_button(self):
        driver = self.selenium
        driver.get(self.live_server_url)

        # Apply filters on Center Name
        center_id = get_filter_id(driver, 'center_name')
        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(center_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(center_id)).click()
        driver.find_element_by_xpath("//label[@for='ddcl-{0}-i4']".format(center_id)).click()
        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(center_id)).click()

        # Set time filters to 'Any date'
        last_modified_id = get_filter_id(driver, 'last_modified')
        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(last_modified_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(last_modified_id)).click()
        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(last_modified_id)).click()
        upload_date_id = get_filter_id(driver, 'upload_date')
        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(upload_date_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(upload_date_id)).click()
        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(upload_date_id)).click()

        # Apply filters on Sample Type
        sample_type_id = get_filter_id(driver, 'sample_type')
        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(sample_type_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(sample_type_id)).click()
        driver.find_element_by_xpath("//label[@for='ddcl-{0}-i1']".format(sample_type_id)).click()
        driver.find_element_by_xpath("//label[@for='ddcl-{0}-i2']".format(sample_type_id)).click()
        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(sample_type_id)).click()
        driver.find_element_by_id("id_apply_filters").click()

        # Make sure that filters are applied
        applied_filters1 = driver.find_element_by_xpath("//div[@class='applied-filters']//ul//li[1]")
        applied_filters2 = driver.find_element_by_xpath("//div[@class='applied-filters']//ul//li[2]")
        filter1 = driver.find_element_by_xpath("//label[@for='ddcl-{0}-i4']".format(center_id))
        filter2 = driver.find_element_by_xpath("//label[@for='ddcl-{0}-i1']".format(sample_type_id))
        filter3 = driver.find_element_by_xpath("//label[@for='ddcl-{0}-i2']".format(sample_type_id))
        self.assertTrue(filter1.text in applied_filters1.text)
        self.assertTrue(filter2.text in applied_filters2.text)
        self.assertTrue(filter3.text in applied_filters2.text)

        for i in range(3):
            text1 = driver.find_element_by_xpath(
                "//div[@class='bDiv']//table//tbody//tr[%d]//td[9]/div" % (i + 1)).text
            text2 = driver.find_element_by_xpath(
                "//div[@class='bDiv']//table//tbody//tr[%d]//td[14]/div" % (i + 1)).text
            self.assertEqual(filter1.text, text1)
            self.assertEqual(filter2.text, text2)

        # Reset filters
        driver.find_element_by_id("id_reset_filters").click()
        time.sleep(5)

        driver.execute_script(
            "$('.viewport')"
            ".scrollLeft($('thead tr th[axis=col13]')"
            ".position().left)")

        driver.find_element_by_xpath("//div[@class='hDivBox']/table/thead/tr/th[14]").click()
        tmp_text = driver.find_element_by_xpath(
            "//div[@class='bDiv']//table//tbody//tr[1]//td[14]/div").text
        if tmp_text == driver.find_element_by_xpath("//label[@for='ddcl-{0}-i1']".format(sample_type_id)).text:
            driver.execute_script(
                "$('.viewport')"
                ".scrollLeft($('thead tr th[axis=col13]')"
                ".position().left)")
            driver.find_element_by_xpath("//div[@class='hDivBox']/table/thead/tr/th[14]").click()
        time.sleep(2)
        filter2 = driver.find_element_by_xpath("//label[@for='ddcl-{0}-i1']".format(sample_type_id))
        for i in range(3):
            text2 = driver.find_element_by_xpath(
                "//div[@class='bDiv']//table//tbody//tr[%d]//td[14]/div" % (i + 1)).text
            self.assertNotEqual(filter2.text, text2)

        applied_filters3 = driver.find_element_by_xpath("//div[@class='applied-filters']//ul//li[1]")
        try:
            applied_filters4 = driver.find_element_by_xpath("//div[@class='applied-filters']//ul//li[3]")
        except:
            pass
        else:
            self.assertTrue(filter2.text not in applied_filters4.text)
    '''
