import configparser
import os
import queue

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
# Read the config file
config_path = os.path.join(os.path.dirname(__file__), '../data/', 'config.ini')

config = configparser.ConfigParser()
config.read(config_path)

# Access the API keys
YOUTUBE_API_KEY = config["DEFAULT"]["YOUTUBE_API_KEY"]


sitekey = "6LfwuyUTAAAAAOAmoS0fdqijC2PbbdH4kjq62Y1b"
CAPTCHA_KEY = config["DEFAULT"]["CAPTCHA_KEY"]

first_keywords_queue = queue.Queue()
all_keywords_queue = queue.Queue()


def add_to_queue(keywords):
    for _ in keywords:
        first_keywords_queue.put(_)


class ScrapePAA():

    def __init__(self, proxy=None):

        service = Service(executable_path=GeckoDriverManager().install())
        if proxy:
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True

            firefox_capabilities['proxy'] = {
                "proxyType": "MANUAL",
                "httpProxy": proxy,
                "sslProxy": proxy
            }

        if os.name == 'posix':  # Detect Linux
            install_dir = "/snap/firefox/current/usr/lib/firefox"
            driver_loc = os.path.join(install_dir, "geckodriver")
            binary_loc = os.path.join(install_dir, "firefox")
            opts = webdriver.FirefoxOptions()
            opts.binary_location = binary_loc
            capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
            if proxy:
                proxy = webdriver.Proxy()
                proxy.proxyType = webdriver.ProxyType.MANUAL
                proxy.http_proxy = 'http://localhost:8080'
                proxy.ssl_proxy = 'http://localhost:8080'
                capabilities['proxy'] = proxy
            self.driver = webdriver.Firefox(capabilities=capabilities, executable_path=driver_loc, options=opts)
        else:
            if proxy:
                profile = webdriver.FirefoxProfile()
                profile.set_preference('network.proxy.type', 1)
                profile.set_preference('network.proxy.http', 'localhost')
                profile.set_preference('network.proxy.http_port', 8080)
                self.driver = webdriver.Firefox(firefox_profile=profile, service=service)
            else:
                self.driver = webdriver.Firefox(service=service)

    def load_more_people_also_ask(self, question):
        # Find the "People Also Ask" box and click it
        paa_box = self.driver.find_element(By.XPATH, f"//div[text()='{question}']")
        paa_box.click()

    def open_page(self, url):
        self.driver.get(url)

    def click_cookies_close(self):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, "button:has-text(\"Reject all\")")
            element.click()
            print("Closed cookie banner")
        except:
            pass

    def search_query_browser(self, keyword, first_search=False):
        wait = WebDriverWait(self.driver, 6)

        if first_search:

            try:
                element = self.driver.find_element(By.XPATH, "//div[text()='Reject all']")
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                # create an ActionChains object
                actions = ActionChains(self.driver)

                # move to the element and click it
                actions.move_to_element(element).click().perform()
            except:
                pass

        # find the search box element and enter the search query
        search_box = self.driver.find_element(By.NAME, 'q')
        search_box.send_keys(keyword)

        search_box.send_keys(Keys.RETURN)

        wait.until(EC.title_contains("Search"))

    def scrape_people_also_ask(self):
        all_questions = []

        wait = WebDriverWait(self.driver, 6)

        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "wQiwMc")))
        paa_boxes = self.driver.find_elements(By.CLASS_NAME, "wQiwMc")
        while len(paa_boxes) < 5:
            for paa_box in paa_boxes:
                action = ActionChains(self.driver)
                action.send_keys(Keys.DOWN)
                action.send_keys(Keys.DOWN)
                action.send_keys(Keys.DOWN)

                action.send_keys(Keys.DOWN)
                paa_box.click()

            paa_boxes = self.driver.find_elements(By.CLASS_NAME, "wQiwMc")

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        paa_boxes = soup.find_all(class_="wQiwMc")

        for count, box in enumerate(paa_boxes):
            div_element = box.find('div', attrs={'jsname': 'lN6iy'})
            question = div_element.span.text
            answer = soup.find_all(class_="hgKElc")[count].text

            qa_pair = {
                'question': question,
                'answer': answer
            }

            all_questions.append(qa_pair)

        print(all_questions)
        return all_questions



    def scrape_link_results(self):
        link_list = []

        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        search = soup.find_all('div', class_="yuRUbf")

        for h in search:
            link_list.append(h.a.get('href'))

        return link_list
