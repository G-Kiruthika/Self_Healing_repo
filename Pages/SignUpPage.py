"""
SignUpPage Page Object

This class models the Sign Up page for automation using Selenium WebDriver.
It uses locators defined in Locators.json and provides methods for interacting with the sign up functionality.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
import json
import os
class SignUpPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Load locators from Locators.json
        loc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Locators.json')
        with open(loc_path, 'r') as f:
            self.locators = json.load(f)[self.__class__.__name__]
    def enter_username(self, username: str):
        elem = self.driver.find_element(By.ID, self.locators['username_input']['value'])
        elem.clear()
        elem.send_keys(username)
    def enter_email(self, email: str):
        elem = self.driver.find_element(By.ID, self.locators['email_input']['value'])
        elem.clear()
        elem.send_keys(email)
    def enter_password(self, password: str):
        elem = self.driver.find_element(By.ID, self.locators['password_input']['value'])
        elem.clear()
        elem.send_keys(password)
    def click_signup(self):
        self.driver.find_element(By.ID, self.locators['signup_button']['value']).click()
    def is_duplicate_email_error_displayed(self) -> bool:
        try:
            return self.driver.find_element(By.XPATH, self.locators['duplicate_email_error']['value']).is_displayed()
        except NoSuchElementException:
            return False