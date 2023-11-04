import time

import pytest
from testpage import OperationHelper
import logging
import yaml

with open('testdata.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


def test_step_one(browser):
    logging.info("Test_one starting")
    test_page = OperationHelper(browser)
    test_page.go_to_site()
    test_page.enter_login("test")
    test_page.enter_pass("test")
    test_page.click_login_button()
    assert test_page.get_error_text() == "401", "test_step_one FAILED"


def test_step_two(browser):
    logging.info("Test_two starting")
    test_page = OperationHelper(browser)
    test_page.go_to_site()
    test_page.enter_login(data.get('login'))
    test_page.enter_pass(data.get('password'))
    test_page.click_login_button()
    assert test_page.get_enter_text() == "Home", "test_step_two FAILED"


def test_step_three(browser):
    logging.info("Test_three starting")
    test_page = OperationHelper(browser)
    test_page.click_contact_button()
    time.sleep(3)
    assert test_page.get_contact_text() == "Contact us!", "step_three FAILED"


def test_step_four(browser):
    logging.info("Test_four starting")
    test_page = OperationHelper(browser)
    test_page.enter_contact_name(data.get('contact_name'))
    test_page.enter_contact_email(data.get('contact_email'))
    test_page.enter_contact_content(data.get('contact_content'))
    test_page.click_submit_contact_button()
    time.sleep(3)
    assert "successfully" in test_page.get_alert_text(), "step_four FAILED"


if __name__ == '__main__':
    pytest.main(['-vv'])
