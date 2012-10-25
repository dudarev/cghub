from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time
import re
import os, shutil
from wsapi.settings import CACHE_DIR
from wsapi.api import request as api_request


class SidebarTests(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SidebarTests, self).setUpClass()

    def test_select_all(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        self.selenium.find_element_by_css_selector("#ddcl-8 > span:first-child > span").click()

        # by center has 8 centers, i0 - deselect all, i1-i7 - selections
        driver.find_element_by_id("ddcl-8-i0").click()
        for i in range(1, 8):
            cb = driver.find_element_by_id("ddcl-8-i%d" % i)
            self.assertFalse(cb.is_selected())

        # click again - select all
        driver.find_element_by_id("ddcl-8-i0").click()
        for i in range(1, 8):
            cb = driver.find_element_by_id("ddcl-8-i%d" % i)
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

        self.selenium.find_element_by_css_selector("#ddcl-9 > span:first-child > span").click()
        # study: phs000178
        driver.find_element_by_id("ddcl-9-i0").click()
        driver.find_element_by_id("ddcl-9-i1").click()
        self.selenium.find_element_by_css_selector("#ddcl-9 > span:last-child > span").click()
        self.selenium.find_element_by_css_selector("#ddcl-8 > span:first-child > span").click()
        # center: BCM+OR+BCCAGSC+OR+BI
        driver.find_element_by_id("ddcl-8-i0").click()
        driver.find_element_by_id("ddcl-8-i1").click()
        driver.find_element_by_id("ddcl-8-i2").click()
        driver.find_element_by_id("ddcl-8-i3").click()
        self.selenium.find_element_by_css_selector("#ddcl-8 > span:last-child > span").click()
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
        self.selenium.find_element_by_css_selector("#ddcl-7 > span:first-child > span").click()
        # analyte_code: D+OR+H+OR+R
        driver.find_element_by_id("ddcl-7-i0").click()
        driver.find_element_by_id("ddcl-7-i1").click()
        driver.find_element_by_id("ddcl-7-i2").click()
        driver.find_element_by_id("ddcl-7-i3").click()
        self.selenium.find_element_by_css_selector("#ddcl-7 > span:last-child > span").click()
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
        driver.find_element_by_id("ddcl-2-i1").click()
        driver.find_element_by_id("ddcl-2-i2").click()
        driver.find_element_by_id("ddcl-2-i3").click()
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


class SearchTests(LiveServerTestCase):
    query = "6d5*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SearchTests, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SearchTests, self).tearDownClass()

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
        self.selenium.execute_script("$('#ddcl-8').click()")
        self.selenium.execute_script("$('#ddcl-8-i0').attr('checked', false)")
        self.selenium.execute_script("$('#ddcl-8-i0').click()")

        # select Baylor and Harvard
        self.selenium.execute_script("$('#ddcl-8-i1').click()")
        self.selenium.execute_script("$('#ddcl-8-i4').click()")

        self.search()

        # check if filters is shown
        filter = (self.selenium.find_element_by_css_selector(
            "#ddcl-8 > span:first-child > span"))
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
        columns = ['Barcode', 'UUID', 'Accession', 'Files Size',
                   'Last modified', 'Disease', 'Disease (full)',
                   'Sample Type', 'Sample Type (full)',
                   'Experiment Type', 'Run Type', 'Center',
                   'Center (full)', 'State']

        self.selenium.get(self.live_server_url)
        for i, column in enumerate(columns):
            if i in (5, 7, 11):
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
    cache_file = '376f9b98cb2e63cb7dddfbbd5647bcf7.xml'
    query = "6d53*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(ColumnSelectTestCase, self).setUpClass()
        TEST_DATA_DIR = 'cghub/test_data/'
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        shutil.copy(
            os.path.join(TEST_DATA_DIR, self.cache_file),
            os.path.join(CACHE_DIR, self.cache_file)
        )
        lxml = api_request(file_name=CACHE_DIR + self.cache_file)._lxml_results
        self.items_count = lxml.Hits

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(ColumnSelectTestCase, self).tearDownClass()
        os.remove(os.path.join(CACHE_DIR, self.cache_file))

    def select_columns(self, driver, location):
        column_count = len(driver.find_elements_by_xpath("//div[@class='hDivBox']/table/thead/tr/th")) - 1
        # Find select on search or cart page
        if location == 'search':
            select = driver.find_element_by_xpath("//form[@id='id_add_files_form']/span/span\
                /span[@class='ui-dropdownchecklist-text']")
        elif location == 'cart':
            select = driver.find_element_by_xpath("//form/span/span/span[@class='ui-dropdownchecklist-text']")
        select.click()
        # Unselecting one by one
        r = range(column_count)
        for i in r:
            driver.find_element_by_id('ddcl-1-i%d' % (i + 1)).click()
            for j in r[:(i + 1)]:
                assert not driver.find_element_by_xpath("//th[@axis='col%d']" % (j + 1)).is_displayed()
            for j in r[(i + 1):]:
                assert driver.find_element_by_xpath("//th[@axis='col%d']" % (j + 1)).is_displayed()
        # Select (all) option
        driver.find_element_by_id('ddcl-1-i0').click()
        for i in range(column_count):
            assert driver.find_element_by_xpath("//th[@axis='col%d']" % (i + 1)).is_displayed()

        select.click()

    def test_column_select(self):
        driver = self.selenium
        driver.get('%s/search/?q=%s' % (self.live_server_url, self.query))

        self.select_columns(driver, 'search')
        driver.find_element_by_css_selector('button.select_all_items').click()
        driver.find_element_by_css_selector('button.add-to-cart-btn').click()
        self.select_columns(driver, 'cart')
