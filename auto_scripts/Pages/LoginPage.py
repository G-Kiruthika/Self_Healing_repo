# Executive Summary:
# This PageClass is updated for TC_LOGIN_004. It implements validation for empty username field and proper error message handling.
# Detailed Analysis:
# - Navigates to login page, leaves username empty, enters valid password, clicks login, and validates error message.
# - Uses locators from Locators.json and strictly follows Python Selenium best practices.
# Implementation Guide:
# 1. Instantiate LoginPage with Selenium WebDriver.
# 2. Call run_tc_login_004(valid_password) for TC_LOGIN_004.
# Quality Assurance Report:
# - Robust error handling, atomic methods, comprehensive docstrings.
# - Peer review and static analysis recommended.
# Troubleshooting Guide:
# - If error messages not found, check locator accuracy.
# - If validation fails, check backend logic.
# Future Considerations:
# - Extend for additional negative login scenarios, parameterize error messages.

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
        self.validation_error = (By.CSS_SELECTOR, '.invalid-feedback')
        self.empty_field_prompt = (By.XPATH, "//*[text()='Mandatory fields are required']")
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

    def get_validation_error(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.validation_error))
            return error_elem.text
        except Exception:
            return None

    def get_empty_field_prompt(self):
        try:
            prompt_elem = self.wait.until(EC.visibility_of_element_located(self.empty_field_prompt))
            return prompt_elem.text
        except Exception:
            return None

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
        validation_error = self.get_validation_error()
        empty_field_prompt = self.get_empty_field_prompt()
        results['error_message'] = error_msg or validation_error or empty_field_prompt
        expected_error = 'Username is required'
        results['pass'] = (results['username_empty'] and results['password_entered'] and results['error_message'] is not None and expected_error in results['error_message'])
        assert results['pass'], f"TC_LOGIN_004 failed: {results}"
        return results
