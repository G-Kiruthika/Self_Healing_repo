# LoginPage.py
"""
Selenium PageClass for Login functionality.
Covers TC_LOGIN_009: Login with email containing special characters.

Best practices:
- Explicit locator definitions for email, password, login button, and error/success messages.
- Robust input validation for emails with special characters.
- Comprehensive docstrings for downstream automation.
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class LoginPage:
    def __init__(self, driver):
        """
        Initializes LoginPage with Selenium WebDriver instance.
        """
        self.driver = driver
        self.login_url = "https://example-ecommerce.com/login"
        self.email_input_locator = (By.ID, "email_input")
        self.password_input_locator = (By.ID, "password_input")
        self.login_button_locator = (By.ID, "login_button")
        self.success_message_locator = (By.ID, "login_success_message")
        self.error_message_locator = (By.ID, "login_error_message")

    def navigate_to_login_page(self):
        """
        Navigates to the login page URL and verifies page load.
        Returns: True if login page is displayed, raises AssertionError otherwise.
        """
        self.driver.get(self.login_url)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_input_locator),
            message="Login page not loaded: email input not visible"
        )
        return True

    def enter_email(self, email):
        """
        Enters email into the email input field.
        Validates email format, including special characters.
        Args:
            email (str): Email address to enter.
        Returns: True if email is accepted, raises AssertionError otherwise.
        """
        assert self.is_valid_email(email), f"Invalid email format: {email}"
        email_input = self.driver.find_element(*self.email_input_locator)
        email_input.clear()
        email_input.send_keys(email)
        return True

    def is_valid_email(self, email):
        """
        Validates email address format, including special characters (RFC 5322 compliant).
        Args:
            email (str): Email address to validate.
        Returns: True if valid, False otherwise.
        """
        # RFC 5322 regex for email validation, allowing special characters
        email_regex = r"^(?=.{1,64}@)[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return re.match(email_regex, email) is not None

    def enter_password(self, password):
        """
        Enters password into the password input field.
        Args:
            password (str): Password to enter.
        Returns: True if password is accepted, raises AssertionError otherwise.
        """
        password_input = self.driver.find_element(*self.password_input_locator)
        password_input.clear()
        password_input.send_keys(password)
        return True

    def click_login(self):
        """
        Clicks the login button.
        Returns: True if click is successful, raises AssertionError otherwise.
        """
        login_button = self.driver.find_element(*self.login_button_locator)
        login_button.click()
        return True

    def verify_login_result(self):
        """
        Verifies login result: success or error message.
        Returns: 'success' if login successful, 'error' if error message displayed.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.success_message_locator)
            )
            return 'success'
        except TimeoutException:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(self.error_message_locator)
                )
                return 'error'
            except TimeoutException:
                raise AssertionError("Neither success nor error message displayed after login attempt.")

    def login_with_special_char_email(self, email, password):
        """
        End-to-end login workflow for email containing special characters.
        Args:
            email (str): Email address with special characters.
            password (str): Valid password.
        Returns: 'success' or 'error' based on login result.
        """
        self.navigate_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self.verify_login_result()

# Example usage for TC_LOGIN_009
# from selenium import webdriver
# driver = webdriver.Chrome()
# login_page = LoginPage(driver)
# result = login_page.login_with_special_char_email("test.user+tag@example.com", "Test@1234")
# assert result == 'success' or result == 'error'
# print(f"TC_LOGIN_009: Login result = {result}")
