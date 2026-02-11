'''
TC_LOGIN_003_TestPage.py
Page Object Class for TC_LOGIN_003: Invalid Email Format Login Attempt AND Invalid Password Scenario

Executive Summary:
- Implements step-by-step automation for invalid email format login attempts AND invalid password login attempts using Selenium Python.
- Strict locator usage: id=login-email, id=login-password, id=login-submit, div.alert-danger.
- Validates error message display and ensures user remains on login page (no session creation).
- Now covers both invalid email and invalid password scenarios as per test case requirements.

Implementation Guide:
1. Instantiate TC_LOGIN_003_TestPage with Selenium WebDriver.
2. Call run_invalid_email_login_test() for invalid email format scenario.
3. Call run_invalid_password_login_test() for invalid password scenario (TC_LOGIN_003).
4. Review returned results for error validation and session checks.

QA Report:
- All locators and steps strictly mapped to test case requirements and Locators.json.
- Comprehensive error handling and validation included.
- Peer review recommended prior to downstream integration.
- Both negative login scenarios covered for robust regression.

Troubleshooting Guide:
- If locators fail, verify web page structure and update accordingly.
- If error message not found, check application logic and test data.
- If session is created on invalid login, review backend authentication logic.

Future Considerations:
- Parameterize email/password for broader negative testing.
- Integrate with session monitoring APIs for advanced validation.
- Extend for multi-language error message checks.
- Consider splitting scenarios into separate PageClasses if test coverage increases.
'''

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TC_LOGIN_003_TestPage:
    '''
    Page Object for TC_LOGIN_003: Invalid Email Format Login Attempt AND Invalid Password Scenario

    Steps Implemented:
    1. Navigate to login page.
    2. Enter invalid email formats (invalidemail@com, testuser.example.com, @example.com).
    3. Enter valid password (Test@1234).
    4. Click Login button.
    5. Validate error message 'Please enter a valid email address' is displayed.
    6. Verify user remains on login page and no session is created.

    Added Steps for TC_LOGIN_003:
    1. Navigate to login page.
    2. Enter valid username (validuser@example.com).
    3. Enter invalid password (WrongPass456!).
    4. Click Login button.
    5. Validate error message 'Invalid username or password' is displayed.
    6. Verify user remains on login page and no session is created.
    '''
    LOGIN_URL = "https://example-ecommerce.com/login"
    EMAIL_LOCATOR = (By.ID, "login-email")
    PASSWORD_LOCATOR = (By.ID, "login-password")
    SUBMIT_LOCATOR = (By.ID, "login-submit")
    ERROR_MSG_LOCATOR = (By.CSS_SELECTOR, "div.alert-danger")

    INVALID_EMAILS = ["invalidemail@com", "testuser.example.com", "@example.com"]
    VALID_PASSWORD = "Test@1234"
    EXPECTED_EMAIL_ERROR_TEXT = "Please enter a valid email address"

    VALID_USERNAME = "validuser@example.com"
    INVALID_PASSWORD = "WrongPass456!"
    EXPECTED_LOGIN_ERROR_TEXT = "Invalid username or password"

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

    def validate_error_message(self, expected_text):
        '''Validate error message is displayed and correct.'''
        try:
            error_elem = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_MSG_LOCATOR)
            )
            assert expected_text in error_elem.text, f"Error message text mismatch: {error_elem.text}"
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
        Runs all invalid email login steps for TC_LOGIN_003 (email format scenario).
        Returns:
            dict: {email: {"error_displayed": bool, "remain_on_login": bool} for each invalid email}
        '''
        self.navigate_to_login_page()
        results = {}
        for email in self.INVALID_EMAILS:
            self.enter_email(email)
            self.enter_password(self.VALID_PASSWORD)
            self.click_login()
            error_displayed = self.validate_error_message(self.EXPECTED_EMAIL_ERROR_TEXT)
            remain_on_login = self.verify_remain_on_login_page()
            results[email] = {
                "error_displayed": error_displayed,
                "remain_on_login": remain_on_login
            }
        return results

    def run_invalid_password_login_test(self):
        '''
        Runs steps for TC_LOGIN_003 (invalid password scenario).
        Steps:
            1. Navigate to login page.
            2. Enter valid username.
            3. Enter invalid password.
            4. Click Login button.
            5. Validate error message 'Invalid username or password' is displayed.
            6. Verify user remains on login page and no session is created.
        Returns:
            dict: {"error_displayed": bool, "remain_on_login": bool}
        '''
        self.navigate_to_login_page()
        self.enter_email(self.VALID_USERNAME)
        self.enter_password(self.INVALID_PASSWORD)
        self.click_login()
        error_displayed = self.validate_error_message(self.EXPECTED_LOGIN_ERROR_TEXT)
        remain_on_login = self.verify_remain_on_login_page()
        return {
            "error_displayed": error_displayed,
            "remain_on_login": remain_on_login
        }

# Example usage:
# from selenium import webdriver
# driver = webdriver.Chrome()
# test_page = TC_LOGIN_003_TestPage(driver)
# email_results = test_page.run_invalid_email_login_test()
# password_result = test_page.run_invalid_password_login_test()
# print(email_results)
# print(password_result)
