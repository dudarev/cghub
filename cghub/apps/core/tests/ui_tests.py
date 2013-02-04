from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time
import re
import os, shutil
from wsapi.settings import CACHE_DIR
from wsapi.api import request as api_request


def wsapi_cache_copy(cache_files):
    """
    copy cache_files from TEST_DATA_DIR to CACHE_DIR
    """
    TEST_DATA_DIR = 'cghub/test_data/'
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    for f in cache_files:
        shutil.copy(
            os.path.join(TEST_DATA_DIR, f),
            os.path.join(CACHE_DIR, f)
        )


def wsapi_cache_remove(cache_files):
    """
    remove cache_files from CACHE_DIR
    """
    for f in cache_files:
        os.remove(os.path.join(CACHE_DIR, f))


class SidebarTests(LiveServerTestCase):
    cache_files = (
                    '7fef5a3e22282d1330d8478c3cb6dcae.xml',
                    'e663e2849a7da1a84256e4527d4102ac.xml')

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SidebarTests, self).setUpClass()
        wsapi_cache_copy(self.cache_files)

    def test_select_all(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        self.selenium.find_element_by_css_selector("#ddcl-9 > span:first-child > span").click()

        # by center has 8 centers, i0 - deselect all, i1-i7 - selections
        driver.find_element_by_id("ddcl-9-i0").click()
        for i in range(1, 8):
            cb = driver.find_element_by_id("ddcl-9-i%d" % i)
            self.assertFalse(cb.is_selected())

        # click again - select all
        driver.find_element_by_id("ddcl-9-i0").click()
        for i in range(1, 8):
            cb = driver.find_element_by_id("ddcl-9-i%d" % i)
            self.assertTrue(cb.is_selected())

    def test_select_date(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        driver.find_element_by_css_selector("span.ui-dropdownchecklist-text").click()

        # dates are ddcl-4
        driver.find_element_by_xpath(
            "//span[@id='ddcl-4']/span/span").click()

        # click the first selection
        i_click = 0

        # check that others are not selected
        driver.find_element_by_id("ddcl-4-i%d" % i_click).click()
        for i in range(0, 5):
            if not i == i_click:
                rb = driver.find_element_by_id("ddcl-4-i%i" % i)
                self.assertFalse(rb.is_selected())

        # click the second selection
        i_click = 1

        # check that others are not selected
        driver.find_element_by_id("ddcl-4-i%d" % i_click).click()
        for i in range(0, 5):
            if not i == i_click:
                rb = driver.find_element_by_id("ddcl-4-i%i" % i)
                self.assertFalse(rb.is_selected())

    def test_selection(self):
        driver = self.selenium
        driver.get(self.live_server_url)

        self.selenium.find_element_by_css_selector("#ddcl-10 > span:first-child > span").click()
        # study: phs000178
        driver.find_element_by_id("ddcl-10-i0").click()
        driver.find_element_by_id("ddcl-10-i2").click()
        self.selenium.find_element_by_css_selector("#ddcl-10 > span:last-child > span").click()
        self.selenium.find_element_by_css_selector("#ddcl-9 > span:first-child > span").click()
        # center: BCM+OR+BCCAGSC+OR+BI
        driver.find_element_by_id("ddcl-9-i0").click()
        driver.find_element_by_id("ddcl-9-i1").click()
        driver.find_element_by_id("ddcl-9-i2").click()
        driver.find_element_by_id("ddcl-9-i3").click()
        self.selenium.find_element_by_css_selector("#ddcl-9 > span:last-child > span").click()
        self.selenium.find_element_by_css_selector("#ddcl-5 > span:first-child > span").click()
        # sample type: 10+OR+12+OR+20
        driver.find_element_by_id("ddcl-5-i0").click()
        driver.find_element_by_id("ddcl-5-i1").click()
        driver.find_element_by_id("ddcl-5-i2").click()
        driver.find_element_by_id("ddcl-5-i3").click()
        self.selenium.find_element_by_css_selector("#ddcl-5 > span:last-child > span").click()
        self.selenium.find_element_by_css_selector("#ddcl-3 > span:first-child > span").click()
        # disease_abbr: LAML+OR+BLCA+OR+LGG
        driver.find_element_by_id("ddcl-3-i0").click()
        driver.find_element_by_id("ddcl-3-i1").click()
        driver.find_element_by_id("ddcl-3-i2").click()
        driver.find_element_by_id("ddcl-3-i3").click()
        self.selenium.find_element_by_css_selector("#ddcl-3 > span:last-child > span").click()
        self.selenium.find_element_by_css_selector("#ddcl-8 > span:first-child > span").click()
        # analyte_code: D+OR+H+OR+R
        driver.find_element_by_id("ddcl-8-i0").click()
        driver.find_element_by_id("ddcl-8-i1").click()
        driver.find_element_by_id("ddcl-8-i2").click()
        driver.find_element_by_id("ddcl-8-i3").click()
        self.selenium.find_element_by_css_selector("#ddcl-8 > span:last-child > span").click()
        self.selenium.find_element_by_css_selector("#ddcl-4 > span:first-child > span").click()
        # library_strategy: Bisulfite-Seq+OR+OTHER+OR+RNA-Seq
        driver.find_element_by_id("ddcl-4-i0").click()
        driver.find_element_by_id("ddcl-4-i1").click()
        driver.find_element_by_id("ddcl-4-i2").click()
        driver.find_element_by_id("ddcl-4-i3").click()
        self.selenium.find_element_by_css_selector("#ddcl-4 > span:last-child > span").click()
        self.selenium.find_element_by_css_selector("#ddcl-2 > span:first-child > span").click()
        # state: bad_data+OR+validating_sample+OR+live+OR+supressed
        driver.find_element_by_id("ddcl-2-i0").click()
        driver.find_element_by_id("ddcl-2-i0").click()
        driver.find_element_by_id("ddcl-2-i1").click()
        driver.find_element_by_id("ddcl-2-i2").click()
        driver.find_element_by_id("ddcl-2-i7").click()
        self.selenium.find_element_by_css_selector("#ddcl-2 > span:last-child > span").click()
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
        # state: bad_data+OR+validating_sample+OR+live+OR+supressed
        self.assertTrue(
            re.match('.*state=[^&]*bad_data', url) and
            re.match('.*state=[^&]*validating_sample', url) and
            re.match('.*state=[^&]*live', url))
        self.assertFalse(
            re.match('.*state=[^&]*submitted', url))

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SidebarTests, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)


class SearchTests(LiveServerTestCase):
    cache_files = (
                '02bb9676ca1a88fececbb4909ccca4fc.xml', '5fa63cb5e9696f2f6edb9cafd16a377f.xml',
                '714f182ce3b2196b3b064880493e242d.xml', 'c0db6ab7b80ded4f9211570170011d80.xml',
                '1337b453bc52e564fdf5853222aee83d.xml', '647ecc223f2f713367bed01d695fbcca.xml',
                '718a11e6622c452544644029fcc90664.xml', 'e663e2849a7da1a84256e4527d4102ac.xml',
                '3e45de4a60a55cb60772e035417aabb1.xml', '69f24e8461162cca74992a655cd902cc.xml',
                '7483974d8235868e5d4d2079d5051332.xml', 'eb43d51ba32b3d5b63288be3d53d409b.xml',
                '4fef00a90792853839aa515df0d4208a.xml', '6ac8323ed6e770f1453201f34809779b.xml',
                'a2ea32b5bcb173f3e434979ba599c3ad.xml', 'fe7edde187f36c943a97e63775909caf.xml')
    query = "6d5*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SearchTests, self).setUpClass()
        wsapi_cache_copy(self.cache_files)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SearchTests, self).tearDownClass()
        wsapi_cache_remove(self.cache_files)

    def search(self, text="6d*"):
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys(text)
        element.submit()

    def test_no_results(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.send_keys("some text")
        element.submit()
        result = self.selenium.find_element_by_xpath(
            "//div[contains(@class,'base-container')]/div/h4")
        assert result.text == "No results found."

    def test_url(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.send_keys("6d7*")
        element.submit()
        time.sleep(10)
        assert "/search/?q=6d7%2A" in self.selenium.current_url

    def test_search_result(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.send_keys("6d7*")
        element.submit()
        assert "Found" in self.selenium.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]").text

    def test_count_pages(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.send_keys("6d*")
        element.submit()
        self.selenium.find_element_by_link_text("25").click()
        assert 25 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[4]/table/tbody/tr"))
        self.selenium.find_element_by_link_text("50").click()
        assert 50 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[4]/table/tbody/tr"))

    def test_pagination(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.send_keys("6d7*")
        element.submit()
        assert 10 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[4]/table/tbody/tr"))
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys("6d*")
        element.submit()
        assert "Found" in self.selenium.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]").text
        assert 10 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[4]/table/tbody/tr"))
        self.selenium.find_element_by_link_text("2").click()
        assert 10 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[6]/div[4]/table/tbody/tr"))

    def test_filtering_shown(self):
        self.selenium.get(self.live_server_url)
        # unselect all
        self.selenium.execute_script("$('#ddcl-9').click()")
        self.selenium.execute_script("$('#ddcl-9-i0').click()")
        self.selenium.execute_script("$('#ddcl-9-i0').click()")

        # select Baylor and Harvard
        self.selenium.execute_script("$('#ddcl-9-i1').click()")
        self.selenium.execute_script("$('#ddcl-9-i4').click()")

        self.search()

        # check if filters is shown
        filter = (self.selenium.find_element_by_css_selector(
            "#ddcl-9 > span:first-child > span"))
        self.assertEqual(filter.text, u'Baylor\nHarvard')

    def test_pagination_links(self):
        self.selenium.get(self.live_server_url)
        self.search("6fd*")

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
                    'Run Type', 'Reference genome', 'Center',
                    'Center Name', 'Experiment Type', 'Upload time',
                    'Last modified', 'Sample Type', 'Sample Type Name', 
                    'State', 'Barcode', 'Sample Accession', 'Files Size'
        ]

        self.selenium.get(self.live_server_url)
        for i, column in enumerate(columns):
            if i in (3, 7, 12):
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
                    self.assertLessEqual(int(first), int(second))
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
        lxml = api_request(file_name=CACHE_DIR + self.cache_files[0])._lxml_results
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
        self.select_columns(driver, 'cart')
