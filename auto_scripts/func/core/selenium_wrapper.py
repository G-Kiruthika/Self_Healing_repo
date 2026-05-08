# auto_scripts/func/core/selenium_wrapper.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SeleniumWrapper:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    def wait_for_element(self, locator, timeout=None):
        wait_time = timeout if timeout else self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_element_located(locator))
    def wait_for_element_visible(self, locator, timeout=None):
        wait_time = timeout if timeout else self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.visibility_of_element_located(locator))
    def wait_for_element_clickable(self, locator, timeout=None):
        wait_time = timeout if timeout else self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.element_to_be_clickable(locator))
    def click_element(self, locator):
        element = self.wait_for_element_clickable(locator)
        element.click()
    def enter_text(self, locator, text):
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
    def get_text(self, locator):
        element = self.wait_for_element_visible(locator)
        return element.text
    def is_element_visible(self, locator, timeout=5):
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    def is_element_present(self, locator, timeout=5):
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
