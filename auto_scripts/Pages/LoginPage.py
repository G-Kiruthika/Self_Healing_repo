# Executive Summary:
# This PageClass is updated for TC_LOGIN_007. It now implements repeated invalid login attempts and account lock validation after multiple failures.
# Detailed Analysis:
# - Navigates to login page, enters valid username and invalid password 5 times, validates error message for each failure.
# - Attempts login with valid credentials after 5 failures, validates account lock message.
# - Uses locators from Locators.json and strictly follows Python Selenium best practices.
# Implementation Guide:
# 1. Instantiate LoginPage with Selenium WebDriver.
# 2. Call run_tc_login_007(email, invalid_passwords, valid_password) for TC_LOGIN_007.
# Quality Assurance Report:
# - Robust error handling, atomic methods, comprehensive docstrings.
# - Peer review and static analysis recommended.
# Troubleshooting Guide:
# - If error messages not found, check locator accuracy.
# - If account lock not triggered, validate backend logic.
# Future Considerations:
# - Extend for additional lockout scenarios, parameterize lock duration.

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.url = 'https://ecommerce.example.com/login'
        self.email_field = (By.ID, 'login-email')
        self.password_field = (By.ID, 'login-password')
        self.login_submit = (By.ID, 'login-submit')
        self.error_message = (By.CSS_SELECTOR, 'div.alert-danger')
        self.lock_message_text = "Account has been locked due to multiple failed attempts. Please try again after 30 minutes or reset your password"
        self.wait = WebDriverWait(driver, timeout)

    def navigate(self):
        self.driver.get(self.url)
        assert self.driver.find_element(*self.email_field).is_displayed(), 'Email field not displayed'
        assert self.driver.find_element(*self.password_field).is_displayed(), 'Password field not displayed'

    def enter_email(self, email):
        email_input = self.driver.find_element(*self.email_field)
        email_input.clear()
        email_input.send_keys(email)
        assert email_input.get_attribute('value') == email, 'Email not entered correctly'

    def enter_password(self, password):
        password_input = self.driver.find_element(*self.password_field)
        password_input.clear()
        password_input.send_keys(password)
        assert password_input.get_attribute('value') == password, 'Password not entered correctly'

    def click_login(self):
        self.driver.find_element(*self.login_submit).click()

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.error_message))
            return error_elem.text
        except Exception:
            return None

    def run_tc_login_007(self, email, invalid_passwords, valid_password):
        """
        Executes TC_LOGIN_007 end-to-end:
        1. Navigate to login page
        2. Enter valid username and invalid password, repeat 5 times
        3. Validate error message for each failed login
        4. Attempt login with valid credentials after 5 failures
        5. Validate account lock message
        Returns dict with results
        """
        results = {'invalid_attempts': [], 'lock_attempt': None, 'overall_pass': False}
        self.navigate()
        self.enter_email(email)
        # Repeat invalid login attempts
        for idx, invalid_pwd in enumerate(invalid_passwords):
            self.enter_password(invalid_pwd)
            self.click_login()
            error_msg = self.get_error_message()
            results['invalid_attempts'].append({'attempt': idx+1, 'password': invalid_pwd, 'error_message': error_msg})
            assert error_msg is not None, f"Error message not found for invalid attempt {idx+1}"
        # Attempt login with valid credentials after failures
        self.enter_password(valid_password)
        self.click_login()
        lock_msg = self.get_error_message()
        results['lock_attempt'] = {'valid_password': valid_password, 'lock_message': lock_msg}
        assert lock_msg is not None, 'Account lock message not found after 6th attempt'
        assert self.lock_message_text in lock_msg, f"Expected lock message not found. Got: {lock_msg}"
        results['overall_pass'] = all([
            all(attempt['error_message'] is not None for attempt in results['invalid_attempts']),
            self.lock_message_text in lock_msg
        ])
        return results

    def run_tc_login_004(self, valid_password):
        """
        Executes TC_LOGIN_004 end-to-end:
        1. Navigate to login page
        2. Leave username field empty
        3. Enter valid password
        4. Click Login
        5. Validate error message 'Username is required' is displayed
        Returns dict with results
        """
        results = {'username_empty': False, 'password_entered': False, 'error_message': None, 'pass': False}
        self.navigate()
        # Leave username empty
        email_input = self.driver.find_element(*self.email_field)
        email_input.clear()
        results['username_empty'] = email_input.get_attribute('value') == ''
        # Enter valid password
        password_input = self.driver.find_element(*self.password_field)
        password_input.clear()
        password_input.send_keys(valid_password)
        results['password_entered'] = password_input.get_attribute('value') == valid_password
        # Click Login
        self.click_login()
        # Validate error message
        error_msg = self.get_error_message()
        results['error_message'] = error_msg
        expected_error = 'Username is required'
        results['pass'] = (results['username_empty'] and results['password_entered'] and error_msg is not None and expected_error in error_msg)
        assert results['pass'], f"TC_LOGIN_004 failed: {results}"
        return results
