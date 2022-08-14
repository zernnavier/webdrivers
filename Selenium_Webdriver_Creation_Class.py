import time
from importlib import import_module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


EDGE_EXTENSION_PATH = "edge://extensions/"
EXPLICIT_WAIT = 10


class HOME:
    URL = "https://microsoftedge.microsoft.com/addons/Microsoft-Edge-Extensions-Home"
    SEARCH_STR = "SaveFrom.net helper"
    _SEARCH_INPUT = "//input[@type='text' and @value]"
    _GET_BUTTON = "//*[@title='SaveFrom.net helper']/ancestor::*[starts-with(@id, 'SearchList')]//*[text()='Get']"


def main():
    driver = Create_WebDriver("edge").get_driver()
    driver.get(HOME.URL)
    search_box = driver.find_element(By.XPATH, HOME._SEARCH_INPUT)
    search_box.send_keys(HOME.SEARCH_STR)
    search_box.send_keys(Keys.ENTER)
    WebDriverWait(driver, EXPLICIT_WAIT).until(EC.element_to_be_clickable((By.XPATH, HOME._GET_BUTTON))).click()
    WebDriverWait(driver, EXPLICIT_WAIT).until(EC.alert_is_present())
    alert = Alert(driver)
    alert.accept()
    time.sleep(15)
    

class Create_WebDriver:
    webdrivers = {
        "Chrome": 'chromedriver',
        "Edge": 'msedgedriver',
        "Firefox": "geckodriver"
    }
    corporations = {
        "Chrome": 'Google',
        "Edge": 'Microsoft',
        "Firefox": "Mozilla"
    }

    def __init__(self, name: str):
        self.name = name.strip().title()

    def get_web_driver_name(self):
        return Create_WebDriver.webdrivers[self.name]

    def get_service_obj(self):
        browser_module = import_module(f"{webdriver.__package__}.{self.name.lower()}")
        return browser_module.service.Service()

    def get_options_obj(self):
        browser_module = import_module(f"{webdriver.__package__}.{self.name.lower()}")
        return browser_module.options.Options()

    def get_driver(self):
        return getattr(webdriver, self.name)(options=self.get_options_obj(), service=self.get_service_obj())




if __name__ == "__main__":
    main()
