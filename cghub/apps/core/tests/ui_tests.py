import time
import re
import os, shutil
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains

from django.test import LiveServerTestCase
from django.conf import settings

from wsapi.api import request as api_request


def wsapi_cache_copy(cache_files):
    """
    copy cache_files from TEST_DATA_DIR to CACHE_DIR
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
    remove cache_files from CACHE_DIR
    """
    for f in cache_files:
        os.remove(os.path.join(settings.WSAPI_CACHE_DIR, f))


def back_to_bytes(*args):
    """
    Converts File Size back to bytes for comparing purposes
    """
    files = [str(ar) for ar in args]
    result = []
    for file_name in files:
        if file_name.endswith('GB'):
            result.append(float(file_name.split(' ')[0]) * 1073741824.)
        elif file_name.endswith('MB'):
            result.append(float(file_name.split(' ')[0]) * 1048576.)
        elif file_name.endswith('KB'):
            result.append(float(file_name.split(' ')[0]) * 1024.)
        else:
            result.append(float(file_name.split(' ')[0]))
    return result[0], result[1]

def get_filter_id(driver, filter_name):
    """
    Helper function for getting sidebar filter id.
    Makes filter tests easier to maintain.
    """
    el = driver.find_element_by_css_selector("select[data-section='{0}'] + span".format(filter_name))
    el_id = el.get_attribute('id').split('-')[-1]
    return el_id

class SidebarTestCase(LiveServerTestCase):
    cache_files = ('543044213d0b4057751b559589049cd2.xml',)

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SidebarTestCase, self).setUpClass()
        wsapi_cache_copy(self.cache_files)

    def test_select_all(self):
        driver = self.selenium
        driver.get(self.live_server_url)

        center_id = get_filter_id(driver, 'center_name')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(center_id)).click()

        # by center has 8 centers, i0 - deselect all, i1-i7 - selections
        driver.find_element_by_id("ddcl-{0}-i0".format(center_id)).click()
        for i in range(1, 8):
            cb = driver.find_element_by_id("ddcl-{0}-i{1}".format(center_id, i))
            self.assertFalse(cb.is_selected())

        # click again - select all
        driver.find_element_by_id("ddcl-{0}-i0".format(center_id)).click()
        for i in range(1, 8):
            cb = driver.find_element_by_id("ddcl-{0}-i{1}".format(center_id, i))
            self.assertTrue(cb.is_selected())


    def test_select_date(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        driver.find_element_by_css_selector("span.ui-dropdownchecklist-text").click()

        # Time modified
        last_modified_id = get_filter_id(driver, 'last_modified')
        driver.find_element_by_xpath(
            "//span[@id='ddcl-{0}']/span/span".format(last_modified_id)).click()
        # click the first selection
        i_click = 0

        # check that others are not selected
        driver.find_element_by_id("ddcl-{0}-i{1}".format(last_modified_id, i_click)).click()
        for i in range(0, 5):
            if not i == i_click:
                rb = driver.find_element_by_id("ddcl-{0}-i{1}".format(last_modified_id, i))
                self.assertFalse(rb.is_selected())

        # click the second selection
        i_click = 1

        # check that others are not selected
        driver.find_element_by_id("ddcl-{0}-i{1}".format(last_modified_id, i_click)).click()
        for i in range(0, 5):
            if not i == i_click:
                rb = driver.find_element_by_id("ddcl-{0}-i{1}".format(last_modified_id, i))
                self.assertFalse(rb.is_selected())

        # Upload date
        upload_date_id = get_filter_id(driver, 'upload_date')
        driver.find_element_by_xpath(
            "//span[@id='ddcl-{0}']/span/span".format(upload_date_id)).click()
        # click the first selection
        z_click = 0

        # check that others are not selected
        driver.find_element_by_id("ddcl-{0}-i{1}".format(upload_date_id, z_click)).click()
        for i in range(0, 5):
            if not i == z_click:
                rb = driver.find_element_by_id("ddcl-{0}-i{1}".format(upload_date_id, i))
                self.assertFalse(rb.is_selected())

        # click the second selection
        z_click = 1

        # check that others are not selected
        driver.find_element_by_id("ddcl-{0}-i{1}".format(upload_date_id, z_click)).click()
        for i in range(0, 5):
            if not i == z_click:
                rb = driver.find_element_by_id("ddcl-{0}-i{1}".format(upload_date_id, i))
                self.assertFalse(rb.is_selected())

    def test_selection(self):
        driver = self.selenium
        driver.get(self.live_server_url)

        # study: phs000178
        study_id = get_filter_id(driver, 'study')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(study_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(study_id)).click()
        driver.find_element_by_id("ddcl-{0}-i1".format(study_id)).click()
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
        # analyte_code: D+OR+H+OR+R
        analyte_code_id = get_filter_id(driver, 'analyte_code')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(analyte_code_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(analyte_code_id)).click()
        driver.find_element_by_id("ddcl-{0}-i1".format(analyte_code_id)).click()
        driver.find_element_by_id("ddcl-{0}-i2".format(analyte_code_id)).click()
        driver.find_element_by_id("ddcl-{0}-i3".format(analyte_code_id)).click()
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:last-child > span".format(analyte_code_id)).click()
        # library_strategy: Bisulfite-Seq+OR+OTHER+OR+RNA-Seq
        library_strategy_id = get_filter_id(driver, 'library_strategy')
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:first-child > span".format(library_strategy_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(library_strategy_id)).click()
        driver.find_element_by_id("ddcl-{0}-i1".format(library_strategy_id)).click()
        driver.find_element_by_id("ddcl-{0}-i2".format(library_strategy_id)).click()
        driver.find_element_by_id("ddcl-{0}-i3".format(library_strategy_id)).click()
        self.selenium.find_element_by_css_selector("#ddcl-{0} > span:last-child > span".format(library_strategy_id)).click()
        # refassem_short_name: NCBI36*+OR+HG18*
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

        driver.find_element_by_id("id_apply_filters").click()

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
        # state: bad_data+OR+live+OR+validating_sample
        self.assertTrue(
            re.match('.*state=[^&]*bad_data', url) and
            re.match('.*state=[^&]*validating_sample', url) and
            re.match('.*state=[^&]*live', url))
        self.assertFalse(
            re.match('.*state=[^&]*submitted', url))

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SidebarTestCase, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)


class CustomDatepickersTestCase(LiveServerTestCase):

    cache_files = (
        '71411da734e90beda34360fa47d88b99_ids.cache',
        '01f2124514e0ee69cbe1723a7d25129f_ids.cache')

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(CustomDatepickersTestCase, self).setUpClass()
        wsapi_cache_copy(self.cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(CustomDatepickersTestCase, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

    def set_datepicker_date(self, start, end, year=None, month=None):
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

    def check_custom_date(self, filter_name, dp_values,
            reverse=False, future=False):
        """
        Helper function for checking whether or not new custom date filter
        is displayed in date filter input.
        """
        driver = self.selenium
        filter_id = get_filter_id(driver, filter_name)

        dp_values = dict(dp_values)
        if reverse:
            tmp = dp_values['start']
            dp_values['start'] = dp_values['end']
            dp_values['end'] = tmp
        elif future:
            dp_values['start'] = datetime.now().date().day - 1
            dp_values['end'] = datetime.now().date().day
            dp_values['month'] = datetime.now().date().month
        else:
            dp_values['month'] += 1
        for key in dp_values:
            if len(str(dp_values[key])) == 1:
                 dp_values[key] = '0' + str(dp_values[key])

        # Check custom date is displayed in filter input
        filter_input = driver.find_element_by_css_selector("#ddcl-{0}".format(filter_id))
        filter_text = filter_input.find_element_by_css_selector('.ui-dropdownchecklist-text').text
        text = "{0}/{1}/{2} - {0}/{1}/{3}".format(
            dp_values['year'], dp_values['month'],
            dp_values['start'], dp_values['end'])
        assert text in filter_text.strip()

    def test_custom_datepickers_future_date(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        dp_values = {
            'start': 31, 'end': 31, 'month': 11,
            'year': datetime.now().date().year}
        last_modified_id = get_filter_id(driver, 'last_modified')
        upload_date_id = get_filter_id(driver, 'upload_date')

        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(upload_date_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(upload_date_id)).click()
        driver.find_element_by_css_selector("button.btn-cancel.btn").click()

        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(upload_date_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(upload_date_id)).click()
        self.set_datepicker_date(dp_values['start'], dp_values['end'], dp_values['month'])
        driver.find_element_by_css_selector("button.btn-submit.btn").click()

        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(last_modified_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(last_modified_id)).click()
        driver.find_element_by_css_selector("button.btn-cancel.btn").click()

        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(last_modified_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(last_modified_id)).click()
        self.set_datepicker_date(dp_values['start'], dp_values['end'], dp_values['month'])
        driver.find_element_by_css_selector("button.btn-submit.btn").click()
        self.check_custom_date('upload_date', dp_values, future=True)
        self.check_custom_date('last_modified', dp_values, future=True)

    def test_custom_datepickers_wrong_date(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        dp_values = {
            'start': 2, 'end': 1,
            'year': datetime.now().date().year,
            'month': datetime.now().date().month}

        last_modified_id = get_filter_id(driver, 'last_modified')
        upload_date_id = get_filter_id(driver, 'upload_date')

        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(upload_date_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(upload_date_id)).click()
        driver.find_element_by_css_selector("button.btn-cancel.btn").click()

        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(upload_date_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(upload_date_id)).click()
        self.set_datepicker_date(dp_values['start'], dp_values['end'])
        driver.find_element_by_css_selector("button.btn-submit.btn").click()

        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(last_modified_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(last_modified_id)).click()
        driver.find_element_by_css_selector("button.btn-cancel.btn").click()

        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(last_modified_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(last_modified_id)).click()
        self.set_datepicker_date(dp_values['start'], dp_values['end'])
        driver.find_element_by_css_selector("button.btn-submit.btn").click()
        self.check_custom_date('upload_date', dp_values, reverse=True)
        self.check_custom_date('last_modified', dp_values, reverse=True)

    def test_custom_datepickers_right_date(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        dp_values = {
            'start': 1, 'end': 2,
            'year': 2012, 'month': 0}

        last_modified_id = get_filter_id(driver, 'last_modified')
        upload_date_id = get_filter_id(driver, 'upload_date')

        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(upload_date_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(upload_date_id)).click()
        self.set_datepicker_date(dp_values['start'], dp_values['end'], dp_values['year'], dp_values['month'])
        driver.find_element_by_css_selector("button.btn-submit.btn").click()

        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(last_modified_id)).click()
        driver.find_element_by_css_selector('#ddcl-{0}-ddw .js-pick-period'.format(last_modified_id)).click()
        self.set_datepicker_date(dp_values['start'], dp_values['end'], dp_values['year'], dp_values['month'])
        driver.find_element_by_css_selector("button.btn-submit.btn").click()
        self.check_custom_date('upload_date', dp_values)
        self.check_custom_date('last_modified', dp_values)
        driver.find_element_by_id("id_apply_filters").click()

        applied_filters = driver.find_element_by_css_selector('.applied-filters')
        assert 'Uploaded' in applied_filters.text
        assert 'Modified' in applied_filters.text


class HelpHintsTestCase(LiveServerTestCase):

    cache_files = ('71411da734e90beda34360fa47d88b99_ids.cache',)

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(HelpHintsTestCase, self).setUpClass()
        wsapi_cache_copy(self.cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(HelpHintsTestCase, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

    def check_help_popups(self, driver):
        ac = ActionChains(driver)
        uuids = driver.find_elements_by_xpath("//div[@class='hDivBox']/table/thead/tr/th")
        uuid = 0
        for uuid_id in range(2, len(uuids) + 1):
            if uuid_id != 2:  # TODO remove this check when all help hints are set up
                continue
            uuid = driver.find_element_by_xpath(
                "//div[@class='hDivBox']/table/thead/tr/th[{0}]/div/a".format(uuid_id))
            ac.move_to_element(uuid)
            ac.perform()
            time.sleep(3)
            tooltip = driver.find_element_by_css_selector('.js-tooltip')
            assert tooltip.is_displayed()

    def test_help_popups(self):
        """
        If this test fails try not to move your mouse while test runs
        """
        driver = self.selenium
        driver.get(self.live_server_url)
        self.check_help_popups(driver)
        driver.find_element_by_css_selector('.data-table-checkbox').click()
        driver.find_element_by_css_selector('.add-to-cart-btn').click()
        self.check_help_popups(driver)


class DetailsTestCase(LiveServerTestCase):

    cache_files = (
        '3d1d2ac5-a525-480f-90dd-b373de8e75dc_with_attributes',
        '3d1d2ac5-a525-480f-90dd-b373de8e75dc_without_attributes',
        '6eddf5ada46b4245d235ef99cba05c67.xml',
        '8d5b272f6c3beb7ef181bdaa15624e83.xml',
        '68ab23f6-254c-4330-8aa9-91c63d445f60_with_attributes',
        '68ab23f6-254c-4330-8aa9-91c63d445f60_without_attributes',
        '7789f892-91e0-4f24-a5f1-165e0111e8be_with_attributes',
        '7789f892-91e0-4f24-a5f1-165e0111e8be_without_attributes',
        '71411da734e90beda34360fa47d88b99_ids.cache',
        '331176dd5166828c0be5f1760007062d.xml')

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
        wsapi_cache_copy(self.cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(DetailsTestCase, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

    def check_popup_shows(self, driver):
        for i in range(1, 4):
            ac = ActionChains(driver)

            # Test that clicking row of the table shows details pop-up
            popup = driver.find_element_by_css_selector('#itemDetailsModal')
            assert not popup.is_displayed()
            td = driver.find_element_by_xpath(
                "//div[@class='bDiv']/table/tbody/tr[{0}]/td[{1}]".format(i, i + 1))
            td.click()
            uuid = driver.find_element_by_xpath(
                "//div[@class='bDiv']/table/tbody/tr[{0}]/td[2]".format(i)).text
            time.sleep(2)
            popup = driver.find_element_by_css_selector('#itemDetailsModal')
            assert popup.is_displayed()
            assert uuid in driver.find_element_by_css_selector('#details-label').text
            driver.find_element_by_xpath("//button[@data-dismiss='modal']").click()

            # Test that clicking on space around checkbox doesn't show pop-up
            driver.find_element_by_xpath(
                "//div[@class='bDiv']/table/tbody/tr[{0}]/td[1]".format(i)
                ).click()
            driver.find_element_by_xpath(
                "//div[@class='bDiv']/table/tbody/tr[{0}]/td[1]/div".format(i)
                ).click()
            popup = driver.find_element_by_css_selector('#itemDetailsModal')
            assert not popup.is_displayed()

            # Test that clicking context menu 'Details' shows details pop-up
            context_menu = driver.find_element_by_css_selector('#table-context-menu')
            assert not context_menu.is_displayed()
            ac.context_click(td)
            ac.perform()
            context_menu = driver.find_element_by_css_selector('#table-context-menu')
            assert context_menu.is_displayed()
            driver.find_element_by_css_selector(".js-details-popup").click()
            time.sleep(2)

            # Uncomment when context menu 'Details' will be fixed and will show pop-up
            # popup = driver.find_element_by_css_selector('#itemDetailsModal')
            # assert popup.is_displayed()
            # assert uuid in driver.find_element_by_css_selector('#details-label').text
            # driver.find_element_by_xpath("//button[@data-dismiss='modal']").click()
            driver.find_element_by_xpath(
                "//div[@class='bDiv']/table/tbody/tr[{0}]/td[1]/div/input".format(i)
                ).click()

    def test_details_popups(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        self.check_popup_shows(driver)
        driver.find_element_by_css_selector('.add-to-cart-btn').click()
        time.sleep(3)
        self.check_popup_shows(driver)

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

        # Test 'Collapse all' and 'Expand all' buttons
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
            "$('.base-container').scrollTop($('#id-download-metadata').position().top);")
        driver.find_element_by_id('id-download-metadata').click()
        time.sleep(5)
        try:
            os.remove(settings.WSAPI_CACHE_DIR + 'metadata.xml')
        except OSError:
            assert False, "File metadata.xml wasn't downloaded"


class SearchTestCase(LiveServerTestCase):

    cache_files = (
        '5c0d0328d8b134326b65f7664b4ca24e.xml', '76c362d1a1f7cf2bddbe62293303ad7e.xml',
        'bb4d172f8ae244b8674e1d07466d3f55.xml', '707395879d3c23366c5ec1642e69f7ad.xml',
        '91b007cb6807683c2e2ecfba09c24f7d.xml', 'ec658922e853a8c3741330af01bc405b.xml',
        'aa06888ac2f625d8d3f84a5e30a34f39.xml', '790aa376817fac025b17aa878fb86e9b.xml',
        'cfbc5305b10bdb1bae5b420f0a371af6.xml', '03dd7235eeb75bd19521e49b0da96604.xml',
        '8095ea0809a0074e8c415845115062b3.xml', '0de87d39f79698685cbbe78b8dae8f54.xml',
        '13dd8ffefeee9a4bcca7b5f29ed6911f.xml', '4c9983171c2b3b793d74d55ca49b980d.xml',
        '09e82ff3db65f0bf8cb36acb8e3a4d9b.xml', '4160e2c5199163358e7e918eaf1b7986.xml',
        '6c34d043ca88ec8032f97eac592e33d9.xml', 'b5b52e9da30c9869530490533891e709.xml')
    query = "6d5*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SearchTestCase, self).setUpClass()
        wsapi_cache_copy(self.cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SearchTestCase, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

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
        time.sleep(10)
        assert "/search/?q=6d71test" in self.selenium.current_url

    def test_search_result(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys("6d71*")
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
        time.sleep(5)
        self.selenium.find_element_by_link_text("25").click()
        assert 25 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[4]/table/tbody/tr"))
        self.selenium.find_element_by_link_text("50").click()
        assert 50 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[4]/table/tbody/tr"))

    def test_pagination(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys("6d*")
        element.submit()
        time.sleep(5)
        assert "Found" in self.selenium.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]").text
        assert 10 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[4]/table/tbody/tr"))
        self.selenium.find_element_by_link_text("2").click()
        assert 10 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[4]/table/tbody/tr"))

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

        # check if filters is shown
        filter = (self.selenium.find_element_by_css_selector(
            "#ddcl-{0} > span:first-child > span".format(center_id)))
        self.assertEqual(filter.text, u'Baylor\nHarvard')
        
        filter2 = (self.selenium.find_element_by_css_selector(
            "#ddcl-{0} > span:first-child > span".format(assembly_id)))
        self.assertEqual(filter2.text, u'NCBI36/HG18')

    def test_pagination_links(self):
        self.selenium.get(self.live_server_url)
        self.search("6d7*")

        found = (self.selenium.find_element_by_css_selector(
            ".base-content > div:nth-child(2)"))
        try:
            page_count = (int(found.text.split()[1]) / 10) + 1
        except:
            page_count = None

        if page_count:
            # at begining 'Prev' and '1' link must be disabled
            prev = self.selenium.find_element_by_link_text('Prev')
            self.__link_is_disabled(prev)
            first = self.selenium.find_element_by_link_text('1')
            self.__link_is_active(first)

            # check page by page
            for page_num in range(2, page_count + 1):
                self.selenium.find_element_by_link_text(str(page_num)).click()
                a = self.selenium.find_element_by_link_text(str(page_num))
                self.__link_is_active(a)

            # 'Next' link must be disabled if we are on the last page
            next = self.selenium.find_element_by_link_text('Next')
            self.__link_is_disabled(next)

            # if now click on 'Prev', page_num-1 will be loaded
            self.selenium.find_element_by_link_text('Prev').click()
            current = self.selenium.find_element_by_link_text(str(page_num - 1))
            self.__link_is_active(current)

            # if now click on 'Next', page_num will be loaded
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
                    'UUID', 'Study', 'Disease', 'Disease Name',
                    'Library Type', 'Assembly', 'Center',
                    'Center Name', 'Experiment Type', 'Upload time',
                    'Last modified', 'Sample Type', 'Sample Type Name', 
                    'State', 'Barcode', 'Sample Accession', 'Files Size'
        ]

        self.selenium.get(self.live_server_url)
        for i, column in enumerate(columns):
            if i in (3, 7, 11):
                continue
            # scroll table
            self.selenium.execute_script("$('.flexigrid div')"
                        ".scrollLeft($('.sort-link:contains(%s)')"
                        ".parents('th').position().left);" % column);
            # after first click element element is asc sorted
            self.selenium.find_element_by_partial_link_text(column).click()

            # getting first element in column
            selector = ".bDiv > table td:nth-child({})".format(i + 2)
            first = self.selenium.find_element_by_css_selector(selector).text

            # scroll table
            self.selenium.execute_script("$('.flexigrid div')"
                        ".scrollLeft($('.sort-link:contains(%s)')"
                        ".parents('th').position().left);" % column);
            # resort
            self.selenium.find_element_by_partial_link_text(column).click()
            second = self.selenium.find_element_by_css_selector(selector).text
            # TODO: for now ignoring the case when one of them is 'None'
            # consider doing it differently
            if not (first == 'None' or second == 'None' or
                    first == ' ' or second == ' '):
                if column == 'Files Size':
                    # GB == GB, MB == MB, etc.
                    first, second = back_to_bytes(first, second)
                    self.assertLessEqual(first, second)
                else:
                    self.assertLessEqual(first, second)


class ColumnSelectTestCase(LiveServerTestCase):
    cache_files = (
                '376f9b98cb2e63cb7dddfbbd5647bcf7.xml',
                'cb712a7b93a6411001cbc34cfb883594.xml',
                'ecbf7eaaf5b476df08b2997afd675701.xml')
    query = "6d53*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(ColumnSelectTestCase, self).setUpClass()
        wsapi_cache_copy(self.cache_files)
        lxml = api_request(file_name=settings.WSAPI_CACHE_DIR + self.cache_files[0])._lxml_results
        self.items_count = lxml.Hits

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(ColumnSelectTestCase, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

    def select_columns(self, driver, location):
        time.sleep(3)
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
                driver.execute_script("$('.flexigrid div')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % j)
                assert not driver.find_element_by_xpath("//th[@axis='col%d']" % (j + 1)).is_displayed()
            for j in r[(i + 1):]:
                driver.execute_script("$('.flexigrid div')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % j)
                assert driver.find_element_by_xpath("//th[@axis='col%d']" % (j + 1)).is_displayed()
        # Select (all) option
        driver.find_element_by_xpath("//label[@for='ddcl-1-i0']").click()
        r2 = range(column_count)
        for x in r2:
            driver.execute_script("$('.flexigrid div')"
                        ".scrollLeft($('.flexigrid table thead tr th[axis=col%d]')"
                        ".position().left)" % x)
            assert driver.find_element_by_xpath("//th[@axis='col%d']" % (x + 1)).is_displayed()
            # I hide each column after test checks if it exists because this
            # part can't check last two columns when tests are run not in fullscreen.
            driver.find_element_by_xpath("//label[@for='ddcl-1-i%d']" % (x + 1)).click()        
        driver.find_element_by_xpath("//label[@for='ddcl-1-i0']").click()
        select.click()

    def test_column_select(self):
        driver = self.selenium
        driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

        self.select_columns(driver, 'search')
        driver.find_element_by_css_selector('input.js-select-all').click()
        driver.find_element_by_css_selector('button.add-to-cart-btn').click()
        time.sleep(3)
        self.select_columns(driver, 'cart')


class ColumnsFillTableWidthTestCase(LiveServerTestCase):
    cache_files = (
                '376f9b98cb2e63cb7dddfbbd5647bcf7.xml',
                'cb712a7b93a6411001cbc34cfb883594.xml',
                'ecbf7eaaf5b476df08b2997afd675701.xml')
    query = "6d53*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(ColumnsFillTableWidthTestCase, self).setUpClass()
        wsapi_cache_copy(self.cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(ColumnsFillTableWidthTestCase, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

    def select_columns(self, driver, location):
        time.sleep(3)
        # Find select on search or cart page
        if location == 'search':
            select = driver.find_element_by_xpath("//form[@id='id_add_files_form']/span/span\
                /span[@class='ui-dropdownchecklist-text']")
        elif location == 'cart':
            select = driver.find_element_by_css_selector("#ddcl-1 > span:first-child > span")
        select.click()

        full_table = driver.find_element_by_class_name('hDiv')
        full_width = full_table.value_of_css_property('width')[:-2]
        full_width = int(full_width.split('.')[0])

        # Unselect all elements
        driver.find_element_by_xpath("//label[@for='ddcl-1-i0']").click()

        # Add columns by 1 each step and check their width equals 
        # full tabel width.
        first_col = driver.find_element_by_xpath("//th[@axis='col0']")
        all_columns_width = first_col.size.get('width', 0)
        for i in range(1, 6):
            driver.find_element_by_xpath("//label[@for='ddcl-1-i%d']" % i).click()
        for x in range(1, 6):
            col = driver.find_element_by_xpath("//th[@axis='col%d']" % x)
            if col.is_displayed():
                all_columns_width += col.size.get('width', 0)

        # Taking in count some random borders < 3px total.
        self.assertTrue((full_width - all_columns_width) < 3)

        # Remove first 2 columns
        all_columns_width = first_col.size.get('width', 0)
        for i in range(1, 3):
            driver.find_element_by_xpath("//label[@for='ddcl-1-i%d']" % i).click()
        for x in range(1, 6):
            col = driver.find_element_by_xpath("//th[@axis='col%d']" % x)
            if col.is_displayed():
                all_columns_width += col.size.get('width', 0)

        # Taking in count some random borders < 3px total.
        self.assertTrue((full_width - all_columns_width) < 3)

        driver.find_element_by_xpath("//label[@for='ddcl-1-i0']").click()

    def test_column_fill_table_space(self):
        driver = self.selenium
        driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

        self.select_columns(driver, 'search')
        driver.find_element_by_css_selector('input.js-select-all').click()
        driver.find_element_by_css_selector('button.add-to-cart-btn').click()
        time.sleep(3)
        self.select_columns(driver, 'cart')


class ResetFiltersButtonTestCase(LiveServerTestCase):
    cache_files = ('f0824accdea06f55a22de5be6e2db752.xml', )

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(ResetFiltersButtonTestCase, self).setUpClass()
        wsapi_cache_copy(self.cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(ResetFiltersButtonTestCase, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

    def test_reset_filters_button(self):
        driver = self.selenium
        driver.get(self.live_server_url)

        # Apply filters on Center Name.
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

        # Apply filters on Sample Type.
        sample_type_id = get_filter_id(driver, 'sample_type')
        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(sample_type_id)).click()
        driver.find_element_by_id("ddcl-{0}-i0".format(sample_type_id)).click()
        driver.find_element_by_xpath("//label[@for='ddcl-{0}-i1']".format(sample_type_id)).click()
        driver.find_element_by_xpath("//label[@for='ddcl-{0}-i2']".format(sample_type_id)).click()
        driver.find_element_by_xpath("//span[@id='ddcl-{0}']/span/span".format(sample_type_id)).click()
        driver.find_element_by_id("id_apply_filters").click()

        # Make sure filters are applied.
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
        time.sleep(2)

        driver.execute_script(
            "$('.flexigrid div')"
            ".scrollLeft($('.flexigrid table thead tr th[axis=col13]')"
            ".position().left)")

        # Sort by Sample Type Name to make sure column includes not only
        # Blood Derived Normal
        driver.find_element_by_xpath("//th[@axis='col13']").click()
        tmp_text = driver.find_element_by_xpath(
            "//div[@class='bDiv']//table//tbody//tr[1]//td[14]/div").text
        if tmp_text == driver.find_element_by_xpath("//label[@for='ddcl-{0}-i1']".format(sample_type_id)).text:
            driver.find_element_by_xpath("//th[@axis='col13']").click()

        filter1 = driver.find_element_by_xpath("//label[@for='ddcl-{0}-i4']".format(center_id))
        filter2 = driver.find_element_by_xpath("//label[@for='ddcl-{0}-i1']".format(sample_type_id))
        for i in range(3):
            text1 = driver.find_element_by_xpath(
                "//div[@class='bDiv']//table//tbody//tr[%d]//td[9]/div" % (i + 1)).text
            text2 = driver.find_element_by_xpath(
                "//div[@class='bDiv']//table//tbody//tr[%d]//td[14]/div" % (i + 1)).text
            self.assertNotEqual(filter1.text, text1)
            self.assertNotEqual(filter2.text, text2)

        applied_filters3 = driver.find_element_by_xpath("//div[@class='applied-filters']//ul//li[1]")
        self.assertTrue(filter1.text not in applied_filters3.text)
        try:
            applied_filters4 = driver.find_element_by_xpath("//div[@class='applied-filters']//ul//li[3]")
        except:
            pass
        else:
            self.assertTrue(filter2.text not in applied_filters4.text)
