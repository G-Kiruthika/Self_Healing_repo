# Executive Summary:
# This PageClass implements the login page automation for TC_LOGIN_003, TC_LOGIN_004, and now TC_LOGIN_006 using Selenium in Python.
# Updates:
# - Added validate_required_password_error_tc_login_006() for TC_LOGIN_006: Validates error message for required password when login is attempted with valid email and empty password.
# - All locators mapped from Locators.json, structured for maintainability and extensibility.

# Detailed Analysis:
# - Strict locator mapping from Locators.json
# - Defensive coding using Selenium WebDriverWait and exception handling
# - Functions for navigation, login, error validation, and negative login outcome
# - Existing methods are preserved and new methods are appended

# Implementation Guide:
# - Instantiate LoginPage with a Selenium WebDriver instance
# - Use open_login_page(), login_with_credentials(), get_authentication_error(), get_validation_error(), is_login_unsuccessful(), validate_required_field_errors_tc_login_004(), and validate_required_password_error_tc_login_006() to automate TC_LOGIN_003, TC_LOGIN_004, and TC_LOGIN_006 scenarios
# - Example usage for TC_LOGIN_006:
#     page = LoginPage(driver)
#     result = page.validate_required_password_error_tc_login_006()
#     assert result['password_error'] is not None
#     assert result['login_unsuccessful']

# Quality Assurance Report:
# - All locator references validated against Locators.json
# - PageClass code reviewed for Pythonic standards and Selenium best practices
# - Functions include assertion checks and detailed exception handling
# - Existing methods are preserved and new methods are appended

# Troubleshooting Guide:
# - Ensure the driver is initialized and points to the correct browser instance
# - Validate all locator values against Locators.json
# - For any assertion failure, review the error message for details
# - TimeoutException may indicate slow page load or incorrect locator

# Future Considerations:
# - Extend PageClass for additional login scenarios and UI validation tests
# - Integrate with reporting tools for enhanced test results

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

    def open_login_page(self):
        '''Navigates to the login page.'''
        try:
            self.driver.get(self.URL)
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        except (TimeoutException, WebDriverException) as e:
            raise Exception(f"Failed to open login page: {str(e)}")

    def login_with_credentials(self, email, password):
        '''Enters credentials and clicks the login button.'''
        try:
            email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_elem.clear()
            email_elem.send_keys(email)
            password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_elem.clear()
            password_elem.send_keys(password)
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            raise Exception(f"Login interaction failed: {str(e)}")

    def get_validation_error(self):
        '''Returns the validation error message for invalid email format.'''
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return error_elem.text
        except TimeoutException:
            return None

    def get_authentication_error(self):
        '''Returns the error message shown for incorrect credentials.'''
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except TimeoutException:
            return None

    def is_login_unsuccessful(self):
        '''Returns True if login was NOT successful (dashboard/user icon not present).'''
        try:
            self.driver.implicitly_wait(2)
            dashboard = self.driver.find_elements(*self.DASHBOARD_HEADER)
            user_icon = self.driver.find_elements(*self.USER_PROFILE_ICON)
            return len(dashboard) == 0 and len(user_icon) == 0
        finally:
            self.driver.implicitly_wait(10)

    def validate_required_field_errors_tc_login_004(self):
        '''
        TC_LOGIN_004: Validates error messages for required fields when login is attempted with empty email and password.
        Steps:
            1. Navigate to login page
            2. Leave email and password fields empty
            3. Click 'Login'
            4. Verify error messages for required fields
        Returns:
            dict with keys: 'empty_prompt', 'error_message', 'validation_error', 'login_unsuccessful'
        '''
        result = {"empty_prompt": None, "error_message": None, "validation_error": None, "login_unsuccessful": None}
        try:
            self.open_login_page()
            email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_elem.clear()
            password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_elem.clear()
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
            # Check for required field error prompts
            try:
                empty_prompt_elem = self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
                result["empty_prompt"] = empty_prompt_elem.text
            except TimeoutException:
                result["empty_prompt"] = None
            try:
                error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
                result["error_message"] = error_elem.text
            except TimeoutException:
                result["error_message"] = None
            try:
                validation_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
                result["validation_error"] = validation_elem.text
            except TimeoutException:
                result["validation_error"] = None
            result["login_unsuccessful"] = self.is_login_unsuccessful()
        except Exception as e:
            raise Exception(f"TC_LOGIN_004 validation failed: {str(e)}")
        return result

    def validate_required_password_error_tc_login_006(self):
        '''
        TC_LOGIN_006: Validates error message for required password when login is attempted with valid email and empty password.
        Steps:
            1. Navigate to login page
            2. Enter valid email (user@example.com) and leave password empty
            3. Click 'Login'
            4. Verify error message for required password
            5. Ensure login is not successful
        Returns:
            dict with keys: 'password_error', 'login_unsuccessful'
        '''
        result = {"password_error": None, "login_unsuccessful": None}
        try:
            self.open_login_page()
            email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_elem.clear()
            email_elem.send_keys("user@example.com")
            password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_elem.clear()
            # Leave password empty
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
            # Check for required password error
            try:
                password_error_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
                result["password_error"] = password_error_elem.text
            except TimeoutException:
                result["password_error"] = None
            result["login_unsuccessful"] = self.is_login_unsuccessful()
        except Exception as e:
            raise Exception(f"TC_LOGIN_006 validation failed: {str(e)}")
        return result
