'''
TC_LOGIN_003_TestPage.py
Page Object Class for TC_LOGIN_003: Invalid Email Format Login Attempt

Executive Summary:
- Implements step-by-step automation for invalid email format login attempts using Selenium Python.
- Strict locator usage: id=login-email, id=login-password, id=login-submit, div.alert-danger.
- Validates error message display and ensures user remains on login page (no session creation).

Implementation Guide:
1. Instantiate TC_LOGIN_003_TestPage with Selenium WebDriver.
2. Call run_invalid_email_login_test() to execute all steps for TC_LOGIN_003.
3. Review returned results for error validation and session checks.

QA Report:
- All locators and steps strictly mapped to test case requirements.
- Comprehensive error handling and validation included.
- Peer review recommended prior to downstream integration.

Troubleshooting Guide:
- If locators fail, verify web page structure and update accordingly.
- If error message not found, check application logic and test data.
- If session is created on invalid login, review backend authentication logic.

Future Considerations:
- Parameterize email/password for broader negative testing.
- Integrate with session monitoring APIs for advanced validation.
- Extend for multi-language error message checks.
'''

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TC_LOGIN_003_TestPage:
    '''
    Page Object for TC_LOGIN_003: Invalid Email Format Login Attempt

    Steps Implemented:
    1. Navigate to login page.
    2. Enter invalid email formats (invalidemail@com, testuser.example.com, @example.com).
    3. Enter valid password (Test@1234).
    4. Click Login button.
    5. Validate error message 'Please enter a valid email address' is displayed.
    6. Verify user remains on login page and no session is created.
    '''
    LOGIN_URL = "https://example-ecommerce.com/login"
    EMAIL_LOCATOR = (By.ID, "login-email")
    PASSWORD_LOCATOR = (By.ID, "login-password")
    SUBMIT_LOCATOR = (By.ID, "login-submit")
    ERROR_MSG_LOCATOR = (By.CSS_SELECTOR, "div.alert-danger")

    INVALID_EMAILS = ["invalidemail@com", "testuser.example.com", "@example.com"]
    VALID_PASSWORD = "Test@1234"
    EXPECTED_ERROR_TEXT = "Please enter a valid email address"

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

    def validate_error_message(self):
        '''Validate error message is displayed and correct.'''
        try:
            error_elem = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_MSG_LOCATOR)
            )
            assert self.EXPECTED_ERROR_TEXT in error_elem.text, f"Error message text mismatch: {error_elem.text}"
            return True
        except (NoSuchElementException, TimeoutException, AssertionError) as e:
            return False

    def verify_remain_on_login_page(self):
        '''Verify user remains on login page and no session is created.'''
        current_url = self.driver.current_url
        # Check URL is still login page
        on_login_page = current_url.startswith(self.LOGIN_URL)
        # Basic session check: look for session cookie (example, adapt as needed)
        session_cookie = self.driver.get_cookie("sessionid")
        session_created = session_cookie is not None
        return on_login_page and not session_created

    def run_invalid_email_login_test(self):
        '''
        Runs all invalid email login steps for TC_LOGIN_003.
        Returns:
            dict: {email: {"error_displayed": bool, "remain_on_login": bool} for each invalid email}
        '''
        self.navigate_to_login_page()
        results = {}
        for email in self.INVALID_EMAILS:
            self.enter_email(email)
            self.enter_password(self.VALID_PASSWORD)
            self.click_login()
            error_displayed = self.validate_error_message()
            remain_on_login = self.verify_remain_on_login_page()
            results[email] = {
                "error_displayed": error_displayed,
                "remain_on_login": remain_on_login
            }
        return results

# Example usage:
# from selenium import webdriver
# driver = webdriver.Chrome()
# test_page = TC_LOGIN_003_TestPage(driver)
# result = test_page.run_invalid_email_login_test()
# print(result)
