# LoginPage.py
# Automated PageClass for TC_LOGIN_001: End-to-end login workflow
# Covers navigation, input, login action, and post-login validation

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://example-ecommerce.com/login'
        self.email_field = (By.ID, 'login-email')
        self.password_field = (By.ID, 'login-password')
        self.remember_me_checkbox = (By.ID, 'remember-me')
        self.login_submit = (By.ID, 'login-submit')
        self.forgot_password_link = (By.CSS_SELECTOR, 'a.forgot-password-link')
        self.error_message = (By.CSS_SELECTOR, 'div.alert-danger')
        self.validation_error = (By.CSS_SELECTOR, '.invalid-feedback')
        self.empty_field_prompt = (By.XPATH, "//*[text()='Mandatory fields are required']")
        self.dashboard_header = (By.CSS_SELECTOR, 'h1.dashboard-title')
        self.user_profile_icon = (By.CSS_SELECTOR, '.user-profile-name')

    def navigate(self):
        """
        Step 1: Navigate to the login page
        """
        self.driver.get(self.url)
        assert self.driver.find_element(*self.email_field).is_displayed(), 'Email field not displayed'
        assert self.driver.find_element(*self.password_field).is_displayed(), 'Password field not displayed'

    def enter_email(self, email):
        """
        Step 2: Enter valid username
        """
        email_input = self.driver.find_element(*self.email_field)
        email_input.clear()
        email_input.send_keys(email)
        assert email_input.get_attribute('value') == email, 'Email not entered correctly'

    def enter_password(self, password):
        """
        Step 3: Enter password
        """
        password_input = self.driver.find_element(*self.password_field)
        password_input.clear()
        password_input.send_keys(password)
        # Password field should be masked
        assert password_input.get_attribute('type') == 'password', 'Password field is not masked'
        assert password_input.get_attribute('value') == password, 'Password not entered correctly'

    def click_login(self):
        """
        Step 4: Click on the Login button
        """
        self.driver.find_element(*self.login_submit).click()

    def validate_post_login(self):
        """
        Validate successful login: dashboard and session
        """
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.dashboard_header)
        )
        assert self.driver.find_element(*self.dashboard_header).is_displayed(), 'Dashboard header not visible'
        assert self.driver.find_element(*self.user_profile_icon).is_displayed(), 'User profile icon not visible'

    def login(self, email, password):
        """
        Complete login workflow for TC_LOGIN_001
        """
        self.navigate()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        self.validate_post_login()

    # Additional validation methods for negative scenarios
    def get_error_message(self):
        try:
            return self.driver.find_element(*self.error_message).text
        except NoSuchElementException:
            return None

    def get_validation_error(self):
        try:
            return self.driver.find_element(*self.validation_error).text
        except NoSuchElementException:
            return None

    def is_empty_field_prompt_displayed(self):
        try:
            return self.driver.find_element(*self.empty_field_prompt).is_displayed()
        except NoSuchElementException:
            return False

    def is_on_login_page(self):
        try:
            return self.driver.current_url == self.url
        except Exception:
            return False

    def perform_invalid_login_and_validate(self, email, invalid_password):
        """
        Implements TC_LOGIN_003:
        1. Navigate to login page
        2. Enter valid username
        3. Enter invalid password
        4. Click Login
        5. Validate error message and user remains on login page
        """
        self.navigate()
        self.enter_email(email)
        self.enter_password(invalid_password)
        self.click_login()
        error_msg = None
        try:
            error_elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.error_message)
            )
            error_msg = error_elem.text
        except Exception:
            error_msg = self.get_error_message()
        assert error_msg is not None, 'Error message not found after invalid login.'
        assert "Invalid username or password" in error_msg, f"Expected error 'Invalid username or password', got '{error_msg}'"
        assert self.is_on_login_page(), 'User is not on login page after failed login.'
        return {
            'error_message': error_msg,
            'on_login_page': self.is_on_login_page()
        }

# Executive Summary:
# - LoginPage.py updated for TC_LOGIN_003: Negative login scenario with invalid password.
# - Strictly adheres to Selenium Python best practices.
# - Includes comprehensive error handling, robust validation, and structured method for downstream automation.
# - All imports validated and methods atomic for QA.
#
# Implementation Guide:
# 1. Instantiate LoginPage with Selenium WebDriver.
# 2. Call perform_invalid_login_and_validate(email, invalid_password) for TC_LOGIN_003.
# 3. Validate returned dict for error message and login page assertion.
#
# Quality Assurance Report:
# - All fields validated, error handling robust.
# - Peer review and static analysis recommended.
# - Ready for downstream integration.
#
# Troubleshooting Guide:
# - If error message not found, check locator accuracy in Locators.json.
# - If user not on login page after failed login, validate backend and UI flow.
#
# Future Considerations:
# - Extend for additional negative login scenarios.
# - Parameterize locators and URLs for multi-environment support.
# - Integrate with test reporting frameworks for automated QA.
