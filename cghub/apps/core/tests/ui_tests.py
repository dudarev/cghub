import time
import re
import os, shutil

from selenium.webdriver.firefox.webdriver import WebDriver

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
        element.send_keys("6d71*")
        element.submit()
        time.sleep(10)
        assert ("/search/?q=6d71%A" in self.selenium.current_url or
            "/search/?q=6d71*" in self.selenium.current_url)

    def test_search_result(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys("6d71*")
        element.submit()
        time.sleep(5)
        assert "6d71*" in self.selenium.find_element_by_css_selector(
            ".page-header + div").text

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
        self.selenium.find_element_by_link_text("25").click()
        print len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[4]/table/tbody/tr"))
        assert 10 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[4]/table/tbody/tr"))
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys("6d1*")
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
        self.search("6d*")

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
