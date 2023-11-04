import time
import yaml
from BaseApp import BasePage
from selenium.webdriver.common.by import By
import logging


class TestSearchLocators:

    ids = dict()
    with open('locators.yaml', encoding='utf-8') as f:
        locators = yaml.safe_load(f)
    for locator in locators["xpath"].keys():
        ids[locator] = (By.XPATH, locators["xpath"][locator])
    for locator in locators["css"].keys():
        ids[locator] = (By.CSS_SELECTOR, locators["css"][locator])


class OperationHelper(BasePage):

    def enter_text_into_field(self, locator, word, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        logging.debug(f"Send {word} to element {element_name}")
        field = self.find_element(locator)
        if not field:
            logging.error(f"Element {locator} not found")
            return False
        try:
            field.clear()
            field.send_keys(word)
        except:
            logging.exception(f"Exception while operation with {locator}")
            return False
        return True

    def enter_login(self, word):
        self.enter_text_into_field(TestSearchLocators.ids["LOCATOR_LOGIN_FIELD"], word,
                                   description="login form")

    def enter_pass(self, word):
        self.enter_text_into_field(TestSearchLocators.ids["LOCATOR_PASS_FIELD"], word,
                                   description="password form")

    def enter_contact_name(self, word):
        self.enter_text_into_field(TestSearchLocators.ids["LOCATOR_ENTER_CONTACT_NAME"], word,
                                   description="name form")

    def enter_contact_email(self, word):
        self.enter_text_into_field(TestSearchLocators.ids["LOCATOR_ENTER_CONTACT_EMAIL"], word,
                                   description="email form")

    def enter_contact_content(self, word):
        self.enter_text_into_field(TestSearchLocators.ids["LOCATOR_ENTER_CONTACT_CONTENT"], word,
                                   description="description")

    def click_button(self, locator, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        button = self.find_element(locator)
        if not button:
            return False
        try:
            button.click()
        except:
            logging.exception("Exception with click")
            return False
        logging.debug(f"Clicked {element_name} button")
        return True

    def click_login_button(self):
        self.click_button(TestSearchLocators.ids["LOCATOR_LOGIN_BTN"], description="login")

    def click_contact_button(self):
        self.click_button(TestSearchLocators.ids["LOCATOR_CONTACT_BTN"], description="Click contact button")

    def click_submit_contact_button(self):
        self.click_button(TestSearchLocators.ids["LOCATOR_SUBMIT_CONTACT_BTN"],
                          description="Click submit contact button")

    def get_text_from_element(self, locator, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        field = self.find_element(locator, time=3)
        if not field:
            return None
        try:
            text = field.text
        except:
            logging.exception(f"Exception while get text from {element_name}")
            return None
        logging.debug(f"We find text {text} in field {element_name}")
        return text

    def get_error_text(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_ERROR_FIELD"])

    def get_enter_text(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_ENTER_FIELD"])

    def get_contact_text(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_CONTACT_TEXT"])

    def get_alert_text(self):
        logging.info("Get alert text")
        text = self.switch_to_alert()
        logging.info(text)
        return text
