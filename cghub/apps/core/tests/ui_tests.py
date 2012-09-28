from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time
import os
import re
import shutil
from wsapi.settings import CACHE_DIR
from lxml import objectify


class SidebarTests(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SidebarTests, self).setUpClass()

    def test_select_all(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        driver.find_element_by_css_selector("span.ui-dropdownchecklist-text").click()

        # by center has 7 centers, i0 - deselect all, i1-i7 - selections
        driver.find_element_by_id("ddcl-6-i0").click()
        for i in range(1, 8):
            cb = driver.find_element_by_id("ddcl-6-i%d" % i)
            self.assertFalse(cb.is_selected())

        # click again - select all
        driver.find_element_by_id("ddcl-6-i0").click()
        for i in range(1, 8):
            cb = driver.find_element_by_id("ddcl-6-i%d" % i)
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

        driver.find_element_by_css_selector("span.ui-dropdownchecklist-text").click()
        # center: BCM+OR+WUGSC+OR+BCCAGSC
        driver.find_element_by_id("ddcl-6-i0").click()
        driver.find_element_by_id("ddcl-6-i1").click()
        driver.find_element_by_id("ddcl-6-i2").click()
        driver.find_element_by_id("ddcl-6-i3").click()
        driver.find_element_by_xpath("//div[@id='ddcl-6-ddw']/div/div[9]").click()
        driver.find_element_by_xpath("//span[@id='ddcl-5']/span/span").click()
        # sample type: 02+OR+03+OR+13
        driver.find_element_by_id("ddcl-5-i0").click()
        driver.find_element_by_id("ddcl-5-i1").click()
        driver.find_element_by_id("ddcl-5-i2").click()
        driver.find_element_by_id("ddcl-5-i3").click()
        driver.find_element_by_xpath("//div[@id='ddcl-5-ddw']/div/div[21]").click()
        driver.find_element_by_xpath("//span[@id='ddcl-3']/span/span").click()
        # disease_abbr: ESCA+OR+DLBC+OR+READ
        driver.find_element_by_id("ddcl-3-i0").click()
        driver.find_element_by_id("ddcl-3-i1").click()
        driver.find_element_by_id("ddcl-3-i2").click()
        driver.find_element_by_id("ddcl-3-i3").click()
        driver.find_element_by_xpath("//div[@id='ddcl-3-ddw']/div/div[29]").click()
        driver.find_element_by_xpath("//span[@id='ddcl-2']/span/span").click()
        # analyte_code: D+OR+G+OR+H
        driver.find_element_by_id("ddcl-2-i0").click()
        driver.find_element_by_id("ddcl-2-i1").click()
        driver.find_element_by_id("ddcl-2-i2").click()
        driver.find_element_by_id("ddcl-2-i3").click()
        driver.find_element_by_xpath("//div[@id='ddcl-2-ddw']/div/div[9]/span").click()
        driver.find_element_by_xpath("//span[@id='ddcl-1']/span/span").click()
        # library_strategy: POOLCLONE+OR+WCS+OR+EST
        driver.find_element_by_id("ddcl-1-i0").click()
        driver.find_element_by_id("ddcl-1-i1").click()
        driver.find_element_by_id("ddcl-1-i2").click()
        driver.find_element_by_id("ddcl-1-i3").click()
        driver.find_element_by_xpath("//div[@id='ddcl-1-ddw']/div/div[22]/span").click()
        driver.find_element_by_id("id_apply_filters").click()

        url = driver.current_url

        # center: BCM+OR+WUGSC+OR+BCCAGSC
        self.assertTrue(
            'BCM' in url and
            'WUGSC' in url and
            'BCCAGSC' in url)
        self.assertFalse(
            'UNC-LCCC' in url)
        # sample type: 02+OR+03+OR+13
        self.assertTrue(
            re.match('.*sample_type=[^&]*02', url) and
            re.match('.*sample_type=[^&]*03', url) and
            re.match('.*sample_type=[^&]*13', url))
        self.assertFalse(
            re.match('.*sample_type=[^&]*14', url))
        # disease_abbr: ESCA+OR+DLBC+OR+READ
        self.assertTrue(
            re.match('.*disease_abbr=[^&]*ESCA', url) and
            re.match('.*disease_abbr=[^&]*DLBC', url) and
            re.match('.*disease_abbr=[^&]*READ', url))
        self.assertFalse(
            re.match('.*disease_abbr=[^&]*GBM', url))
        # analyte_code: D+OR+G+OR+H
        self.assertTrue(
            re.match('.*analyte_code=[^&]*D', url) and
            re.match('.*analyte_code=[^&]*G', url) and
            re.match('.*analyte_code=[^&]*H', url))
        self.assertFalse(
            re.match('.*analyte_code=[^&]*T', url))
        # library_strategy: POOLCLONE+OR+WCS+OR+EST
        self.assertTrue(
            re.match('.*library_strategy=[^&]*POOLCLONE', url) and
            re.match('.*library_strategy=[^&]*WCS', url) and
            re.match('.*library_strategy=[^&]*EST', url))
        self.assertFalse(
            re.match('.*library_strategy=[^&]*WXS', url))

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SidebarTests, self).tearDownClass()


class SearchTests(LiveServerTestCase):
    cache_files = [
        '427dcd2c78d4be27efe3d0cde008b1f9.xml'
    ]
    query = "6d5*"

    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
        super(SearchTests, self).setUpClass()
        TEST_DATA_DIR = 'cghub/test_data/'
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        for f in self.cache_files:
            shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(CACHE_DIR, f)
            )
        self.default_results = objectify.fromstring(
            open(os.path.join(CACHE_DIR, self.cache_files[0])).read())
        self.default_results_count = len(
            self.default_results.findall('Result'))

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(SearchTests, self).tearDownClass()
        for f in self.cache_files:
            os.remove(os.path.join(CACHE_DIR, f))

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
            "//*[@id='id_add_files_form']/div[3]/div[5]/table/tbody/tr"))
        self.selenium.find_element_by_link_text("50").click()
        assert 50 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[3]/div[5]/table/tbody/tr"))

    def test_pagination(self):
        self.selenium.get(self.live_server_url)
        element = self.selenium.find_element_by_name("q")
        element.send_keys("6d7*")
        element.submit()
        assert 10 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[3]/div[5]/table/tbody/tr"))
        element = self.selenium.find_element_by_name("q")
        element.clear()
        element.send_keys("6d*")
        element.submit()
        assert "Found" in self.selenium.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]").text
        assert 10 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[3]/div[5]/table/tbody/tr"))
        self.selenium.find_element_by_link_text("2").click()
        assert 10 == len(self.selenium.find_elements_by_xpath(
            "//*[@id='id_add_files_form']/div[3]/div[5]/table/tbody/tr"))

    def test_filtering_shown(self):
        self.selenium.get(self.live_server_url)
        # unselect all
        self.selenium.execute_script("$('.sidebar span')[0].click()")
        self.selenium.execute_script("$('#ddcl-6-i0').attr('checked', false)")
        self.selenium.execute_script("$('#ddcl-6-i0').click()")

        # select Baylor and Harvard
        self.selenium.execute_script("$('#ddcl-6-i1').click()")
        self.selenium.execute_script("$('#ddcl-6-i6').click()")

        self.search()

        # check if filters is shown
        filter = (self.selenium.find_element_by_css_selector(
            "#ddcl-6 > span:first-child > span:first-child"))
        self.assertEqual(filter.text, u'Baylor\nHarvard')

    def test_links(self):
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
            for page_num in range(2, page_count+1):
                self.selenium.find_element_by_link_text(str(page_num)).click()
                a = self.selenium.find_element_by_link_text(str(page_num))
                self.__link_is_active(a)

            # 'Next' link must be disabled if we are on the last page
            next = self.selenium.find_element_by_link_text('Next')
            self.__link_is_disabled(next)

            # if now click on 'Prev', page_num-1 will be loaded
            self.selenium.find_element_by_link_text('Prev').click()
            current = self.selenium.find_element_by_link_text(str(page_num-1))
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
                   'Last modified', 'Disease', 'Sample Type',
                   'Experiment Type', 'Run Type', 'Center']

        self.selenium.get(self.live_server_url)
        for i, column in enumerate(columns):
            # aftre first click element element is asc sorted
            self.selenium.find_element_by_partial_link_text(column).click()

            # getting first element in column
            selector = ".bDiv > table td:nth-child({})".format(i + 2)
            first = self.selenium.find_element_by_css_selector(selector).text

            # resort
            self.selenium.find_element_by_partial_link_text(column).click()
            second = self.selenium.find_element_by_css_selector(selector).text
            self.assertLessEqual(first, second)

