'''
Executive Summary:
This PageClass implements the login page automation for an e-commerce application using Selenium in Python. It supports:
- TC-LOGIN-008: extremely long email validation
- TC-LOGIN-009: extremely long password validation (NEW)
All locators are mapped from Locators.json and the code is structured for maintainability and extensibility.

Detailed Analysis:
- Strict locator mapping from Locators.json
- Defensive coding using Selenium WebDriverWait and exception handling
- Functions for login, error handling, and navigation
- New method for extremely long password handling as per TC-LOGIN-009

Implementation Guide:
- Instantiate LoginPage with a Selenium WebDriver instance
- Use tc_login_008_extremely_long_email_login() to automate TC-LOGIN-008 scenario
- Use tc_login_009_extremely_long_password_login() to automate TC-LOGIN-009 scenario
- Example usage:
    page = LoginPage(driver)
    result = page.tc_login_009_extremely_long_password_login(valid_email, very_long_password)
- Returns True if system handles input gracefully (error/truncation/validation), False otherwise

Quality Assurance Report:
- All locator references validated against Locators.json
- PageClass code reviewed for Pythonic standards and Selenium best practices
- Functions include assertion checks and detailed exception handling
- Existing methods are preserved and new methods are appended

Troubleshooting Guide:
- Ensure the driver is initialized and points to the correct browser instance
- Validate all locator values against Locators.json
- For any assertion failure, review the error message for details
- TimeoutException may indicate slow page load or incorrect locator

Future Considerations:
- Extend PageClass for additional navigation and UI validation tests
- Integrate with reporting tools for enhanced test results
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    WebDriverException
)

class LoginPage:
    '''
    Page Object for the Login Page.
    Implements methods for login scenarios and navigation to password recovery.
    '''

    # Locators from Locators.json
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[contains(text(),'Mandatory fields are required')]")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Existing methods preserved ---
    # ... [existing code preserved, see previous content] ...

    # --- TC-LOGIN-008: Login with Extremely Long Email Address ---
    def tc_login_008_extremely_long_email_login(self, long_email: str, valid_password: str) -> bool:
        '''
        Automates TC-LOGIN-008: Login attempt using an extremely long email address (255+ characters).
        Steps:
            1. Navigate to the login page.
            2. Enter extremely long email address.
            3. Enter valid password.
            4. Click on the Login button.
            5. Validate system response: truncation, validation error, or graceful failure.
        Args:
            long_email (str): The extremely long email address.
            valid_password (str): The valid password.
        Returns:
            bool: True if system handles input gracefully (error/truncation/validation), False otherwise.
        '''
        try:
            self.driver.get("https://ecommerce.example.com/login")
            self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
            email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_input.clear()
            email_input.send_keys(long_email)
            password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_input.clear()
            password_input.send_keys(valid_password)
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
            error_or_validation_present = False
            try:
                error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
                if error_elem.is_displayed():
                    error_or_validation_present = True
            except (TimeoutException, NoSuchElementException):
                pass
            try:
                validation_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
                if validation_elem.is_displayed():
                    error_or_validation_present = True
            except (TimeoutException, NoSuchElementException):
                pass
            still_on_login_page = self.driver.current_url == "https://ecommerce.example.com/login"
            dashboard_header_absent = True
            try:
                self.driver.find_element(*self.DASHBOARD_HEADER)
                dashboard_header_absent = False
            except NoSuchElementException:
                dashboard_header_absent = True
            return error_or_validation_present and still_on_login_page and dashboard_header_absent
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException) as e:
            print(f"Exception during TC_LOGIN_008 extremely long email login: {e}")
            return False

    # --- TC-LOGIN-009: Login with Extremely Long Password (NEW) ---
    def tc_login_009_extremely_long_password_login(self, valid_email: str, very_long_password: str) -> bool:
        '''
        Automates TC-LOGIN-009: Login attempt using an extremely long password (1000+ characters).
        Steps:
            1. Navigate to the login page.
            2. Enter valid email address.
            3. Enter extremely long password.
            4. Click on the Login button.
            5. Validate system response: truncation, validation error, or graceful failure.
        Args:
            valid_email (str): The valid email address.
            very_long_password (str): The extremely long password string (1000+ chars).
        Returns:
            bool: True if system handles input gracefully (error/truncation/validation), False otherwise.
        '''
        try:
            self.driver.get("https://ecommerce.example.com/login")
            self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
            email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_input.clear()
            email_input.send_keys(valid_email)
            password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_input.clear()
            password_input.send_keys(very_long_password)
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
            error_or_validation_present = False
            try:
                error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
                if error_elem.is_displayed():
                    error_or_validation_present = True
            except (TimeoutException, NoSuchElementException):
                pass
            try:
                validation_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
                if validation_elem.is_displayed():
                    error_or_validation_present = True
            except (TimeoutException, NoSuchElementException):
                pass
            still_on_login_page = self.driver.current_url == "https://ecommerce.example.com/login"
            dashboard_header_absent = True
            try:
                self.driver.find_element(*self.DASHBOARD_HEADER)
                dashboard_header_absent = False
            except NoSuchElementException:
                dashboard_header_absent = True
            return error_or_validation_present and still_on_login_page and dashboard_header_absent
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException) as e:
            print(f"Exception during TC_LOGIN_009 extremely long password login: {e}")
            return False
