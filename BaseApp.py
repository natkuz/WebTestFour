from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import yaml
import requests
from zeep import Client, Settings

with open('testdata.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = data.get('address')

    def find_element(self, locator, time=10):
        try:
            element = WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                             message=f"Can't find element by locator {locator}")
        except:
            logging.exception("Find element exception")
            element = None
        return element

    def get_element_property(self, locator, property):
        element = self.find_element(locator)
        if element:
            return element.value_of_css_property(property)
        else:
            logging.error(f"Property {property} not found in element with locator {locator}")
            return None

    def go_to_site(self):
        try:
            start_browsing = self.driver.get(self.base_url)
        except:
            logging.exception("Exception while open site")
            start_browsing = None
        return start_browsing

    def switch_to_alert(self):
        try:
            alert = self.driver.switch_to.alert
            return alert.text
        except:
            logging.exception("Exception with alert")
            return None


class BaseRestApi:
    def __init__(self):
        self.base_api_url = "https://en.wikipedia.org/w/api.php"
        self.s = requests.Session()

    def get_sites(self, lat, long, radius, limit=100):
        params = {
            "format": "json",
            "list": "geosearch",
            "gs_coord": f"{lat}|{long}",
            "gs_limit": f"{limit}",
            "gs_radius": f"{radius}",
            "action": "query"
        }
        try:
            url = self.base_api_url
            r = self.s.get(url=url, params=params)
            pages = r.json()['query']['geosearch']
            sites = [i['title'] for i in pages]
            return sites
        except:
            logging.exception("Exception with get site")
            return None


class BaseSoapApi:
    def __init__(self):
        self.settings = Settings(strict=False)
        self.client = Client(wsdl=data.get('wsdl'), settings=self.settings)

    def check_text(self, word: str) -> list:
        try:
            res = self.client.service.checkText(word)[0]['s']
            return res
        except:
            logging.exception("Exception with check text")
            return None
