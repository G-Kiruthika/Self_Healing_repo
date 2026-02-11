'''
TC_LOGIN_009_TestPage.py
Page Object Class for TC_LOGIN_009: Login with Email Containing Special Characters

Executive Summary:
- Implements end-to-end automation for login with email containing special characters using Selenium Python.
- Strict locator usage: id=login-email, id=login-password, id=login-submit, div.alert-danger, h1.dashboard-header.
- Validates acceptance of special character email, successful login, and error handling.

Implementation Guide:
1. Instantiate TC_LOGIN_009_TestPage with Selenium WebDriver.
2. Call run_special_character_email_login_test() to execute all steps for TC_LOGIN_009.
3. Review returned results for login success/error validation.

QA Report:
- All locators and steps strictly mapped to test case requirements.
- Comprehensive error handling and validation included.
- Peer review recommended prior to downstream integration.
- Code reviewed for atomicity, maintainability, and adherence to project standards.

Troubleshooting Guide:
- If locators fail, verify web page structure and update accordingly.
- If login fails with valid credentials, check backend authentication logic.
- If error message not found, check application logic and test data.

Future Considerations:
- Parameterize email/password for broader special character testing.
- Integrate with session monitoring APIs for advanced validation.
- Extend for multi-language error message checks and accessibility validation.
'''

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TC_LOGIN_009_TestPage:
    '''
    Page Object for TC_LOGIN_009: Login with Email Containing Special Characters

    Steps Implemented:
    1. Navigate to login page.
    2. Enter email with special characters (test.user+tag@example.com).
    3. Enter valid password (Test@1234).
    4. Click Login button.
    5. Validate successful login (dashboard header) or error message.
    '''
    LOGIN_URL = "https://example-ecommerce.com/login"
    EMAIL_LOCATOR = (By.ID, "login-email")
    PASSWORD_LOCATOR = (By.ID, "login-password")
    SUBMIT_LOCATOR = (By.ID, "login-submit")
    ERROR_MSG_LOCATOR = (By.CSS_SELECTOR, "div.alert-danger")
    DASHBOARD_HEADER_LOCATOR = (By.CSS_SELECTOR, "h1.dashboard-header")

    SPECIAL_CHAR_EMAIL = "test.user+tag@example.com"
    VALID_PASSWORD = "Test@1234"

    def __init__(self, driver):
        '''
        Args:
            driver: Selenium WebDriver instance
        '''
        self.driver = driver

    def navigate_to_login_page(self):
        '''Navigate to the login page.'''
        self.driver.get(self.LOGIN_URL)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.EMAIL_LOCATOR)
        )

    def enter_email(self, email):
        '''Enter email in the email field.'''
        email_field = self.driver.find_element(*self.EMAIL_LOCATOR)
        email_field.clear()
        email_field.send_keys(email)

    def enter_password(self, password):
        '''Enter password in the password field.'''
        password_field = self.driver.find_element(*self.PASSWORD_LOCATOR)
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        '''Click the login button.'''
        submit_btn = self.driver.find_element(*self.SUBMIT_LOCATOR)
        submit_btn.click()

    def validate_dashboard_header(self):
        '''Validate dashboard header is displayed, indicating successful login.'''
        try:
            dashboard_elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.DASHBOARD_HEADER_LOCATOR)
            )
            return True, dashboard_elem.text
        except (NoSuchElementException, TimeoutException):
            return False, None

    def validate_error_message(self):
        '''Validate error message is displayed and return its text.'''
        try:
            error_elem = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_MSG_LOCATOR)
            )
            return True, error_elem.text
        except (NoSuchElementException, TimeoutException):
            return False, None

    def run_special_character_email_login_test(self):
        '''
        Runs all steps for TC_LOGIN_009: Login with email containing special characters.
        Returns:
            dict: {
                "login_success": bool,
                "dashboard_header": str or None,
                "error_displayed": bool,
                "error_message": str or None
            }
        '''
        self.navigate_to_login_page()
        self.enter_email(self.SPECIAL_CHAR_EMAIL)
        self.enter_password(self.VALID_PASSWORD)
        self.click_login()

        login_success, dashboard_header = self.validate_dashboard_header()
        error_displayed, error_message = self.validate_error_message()

        return {
            "login_success": login_success,
            "dashboard_header": dashboard_header,
            "error_displayed": error_displayed,
            "error_message": error_message
        }

# Example usage:
# from selenium import webdriver
# driver = webdriver.Chrome()
# test_page = TC_LOGIN_009_TestPage(driver)
# result = test_page.run_special_character_email_login_test()
# print(result)
