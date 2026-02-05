"""
PageClass: LoginNegativeTestPage
Description: Selenium Page Object for negative login scenarios (non-existent user).
Test Case: TC_SCRUM96_005 (login with non-existent user)
Standards: Strict adherence to Selenium Python automation conventions.
Dependencies: Locators.json, LoginPage, LogValidationPage
Mandatory Documentation: Inline docstrings, method descriptions, and usage notes.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.LoginPage import LoginPage
from pages.LogValidationPage import LogValidationPage
import requests
import json

class LoginNegativeTestPage(LoginPage):
    """
    Page Object for handling negative login cases, specifically for non-existent users.
    Extends LoginPage to reuse login logic.
    """

    def __init__(self, driver, base_url, api_endpoint, logger=None):
        """
        :param driver: Selenium WebDriver instance
        :param base_url: Application base URL
        :param api_endpoint: Endpoint for login API to validate backend response
        :param logger: Optional logger for log validation
        """
        super().__init__(driver)
        self.base_url = base_url
        self.api_endpoint = api_endpoint
        self.logger = logger
        # Load locators
        with open('Locators.json', 'r') as f:
            self.locators = json.load(f)["LoginPage"]

    def login_with_invalid_user(self, username, password):
        """
        Attempts to login with a non-existent user via the UI.
        :param username: Username string (invalid/non-existent)
        :param password: Password string
        :return: error_message (str)
        """
        self.driver.get(self.base_url)
        username_field = self.driver.find_element(By.XPATH, self.locators["username"])
        password_field = self.driver.find_element(By.XPATH, self.locators["password"])
        login_button = self.driver.find_element(By.XPATH, self.locators["login_button"])

        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        login_button.click()

        # Wait for error message
        error_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.locators["error_message"]))
        )
        error_message = error_elem.text
        return error_message

    def validate_api_response(self, username, password):
        """
        Validates backend API response for login attempt with non-existent user.
        :param username: Username string
        :param password: Password string
        :return: API response JSON
        """
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(self.api_endpoint, json=payload)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        return response.json()

    def validate_log_for_failed_login(self, username):
        """
        Validates that the log records the failed login attempt for non-existent user.
        :param username: Username string
        :return: True if log entry found, else False
        """
        log_validator = LogValidationPage(self.logger)
        return log_validator.check_log_for_event(
            event_type="FAILED_LOGIN",
            details={"username": username}
        )

    def run_negative_login_test(self, username, password):
        """
        Executes the end-to-end negative login test:
        1. Attempts login via UI.
        2. Validates backend API response.
        3. Checks log for failed login event.
        :param username: Username string
        :param password: Password string
        :return: dict with results
        """
        ui_error = self.login_with_invalid_user(username, password)
        api_result = self.validate_api_response(username, password)
        log_found = self.validate_log_for_failed_login(username)

        return {
            "ui_error_message": ui_error,
            "api_response": api_result,
            "log_validation": log_found
        }
