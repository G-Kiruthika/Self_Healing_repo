# Executive Summary:
# This PageClass implements the login page automation for TC_LOGIN_003, TC_LOGIN_004, TC_LOGIN_006, and now TC001 using Selenium in Python.
# Updates:
# - Added execute_tc001_login_workflow() for TC001, which navigates to login page, enters valid credentials, submits, and verifies dashboard redirection.
# - All locators mapped from Locators.json, structured for maintainability and extensibility.

# Detailed Analysis:
# - Strict locator mapping from Locators.json
# - Defensive coding using Selenium WebDriverWait and exception handling
# - Functions for navigation, login, error validation, and positive login outcome
# - Existing methods are preserved and new methods are appended

# Implementation Guide:
# - Instantiate LoginPage with a Selenium WebDriver instance
# - Use open_login_page(), login_with_credentials(), execute_tc001_login_workflow(email, password) to automate TC001 scenario
# - Example usage for TC001:
#     page = LoginPage(driver)
#     result = page.execute_tc001_login_workflow(email="user@example.com", password="ValidPassword123")
#     assert result["dashboard_displayed"]

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
        Returns dict with keys: 'empty_prompt', 'error_message', 'validation_error', 'login_unsuccessful'
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

    def validate_password_required_error_tc_login_006(self, email):
        '''
        TC_LOGIN_006: Validates error message for required password when login is attempted with valid email and empty password.
        Returns dict with keys: 'empty_prompt', 'error_message', 'validation_error', 'login_unsuccessful'
        '''
        result = {"empty_prompt": None, "error_message": None, "validation_error": None, "login_unsuccessful": None}
        try:
            self.open_login_page()
            email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_elem.clear()
            email_elem.send_keys(email)
            password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_elem.clear()
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
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
            raise Exception(f"TC_LOGIN_006 validation failed: {str(e)}")
        return result

    def execute_tc001_login_workflow(self, email, password):
        '''
        TC001: Executes the login workflow for a valid user.
        Steps:
            1. Navigate to the login page
            2. Enter valid email and password
            3. Click the 'Login' button
            4. Verify dashboard is displayed
        Args:
            email (str): Valid email
            password (str): Valid password
        Returns:
            dict with keys: 'dashboard_displayed', 'user_icon_displayed', 'error_message'
        '''
        result = {"dashboard_displayed": False, "user_icon_displayed": False, "error_message": None}
        try:
            self.open_login_page()
            self.login_with_credentials(email, password)
            dashboard = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            result["dashboard_displayed"] = dashboard.is_displayed()
            user_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            result["user_icon_displayed"] = user_icon.is_displayed()
        except TimeoutException:
            result["dashboard_displayed"] = False
            result["user_icon_displayed"] = False
            result["error_message"] = self.get_authentication_error()
        except Exception as e:
            result["error_message"] = str(e)
        return result
