from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time
import os
import shutil
from wsapi.settings import CACHE_DIR
from lxml import objectify


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

