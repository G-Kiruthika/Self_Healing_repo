from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import jwt
import datetime
from typing import Optional, Dict, Any
import requests

class LoginPage:
    """
    Page Object Model for LoginPage.
    Strictly covers TC_LOGIN_001 and all acceptance criteria using locators:
    - URL: https://example-ecommerce.com/login
    - Email field: id=login-email
    - Password field: id=login-password
    - Remember Me: id=remember-me
    - Login button: id=login-submit
    - Forgot Password: a.forgot-password-link
    - Error: div.alert-danger
    - Validation error: .invalid-feedback
    - Empty field prompt: text='Mandatory fields are required'
    - Dashboard header: h1.dashboard-title
    - User profile: .user-profile-name
    """
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to_login_page(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))

    def enter_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_btn.click()

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return None

    def is_on_login_page(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            return True
        except Exception:
            return False

    def login_with_credentials(self, email, password):
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def verify_successful_login(self):
        # Wait for dashboard header and user profile icon
        dashboard_header = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
        user_profile_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
        return dashboard_header.is_displayed() and user_profile_icon.is_displayed()

    def validate_login_workflow(self, email, password):
        """
        Strict E2E validation for TC_LOGIN_001:
        1. Navigate to login page
        2. Enter valid credentials
        3. Click login
        4. Assert redirect to dashboard and user session
        5. Assert user profile visible
        """
        self.login_with_credentials(email, password)
        assert self.verify_successful_login(), "Dashboard and user profile not displayed after login."

    def validate_all_fields_present(self):
        """
        Ensures all required fields and buttons are present on the login page.
        """
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_SUBMIT_BUTTON))
        self.wait.until(EC.visibility_of_element_located(self.FORGOT_PASSWORD_LINK))
        self.wait.until(EC.visibility_of_element_located(self.REMEMBER_ME_CHECKBOX))

    def validate_empty_field_prompts(self):
        """
        Checks for empty field validation prompts.
        """
        self.go_to_login_page()
        self.click_login()
        try:
            prompt = self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return prompt.text
        except Exception:
            return None

    def perform_invalid_login_and_validate(self, email, invalid_password):
        """
        Performs invalid login and validates error message.
        Steps:
            1. Navigate to the login screen.
            2. Enter invalid username and/or password.
            3. Click Login button.
            4. Validate error message 'Invalid username or password. Please try again.' is displayed.
            5. Assert user remains on login page after failed login.
        Args:
            email (str): Invalid email/username.
            invalid_password (str): Invalid password.
        Returns:
            None
        Raises:
            AssertionError: If error message is not as expected or user is not on login page.
        """
        expected_error = "Invalid username or password. Please try again."
        self.login_with_credentials(email, invalid_password)
        error_msg = self.get_error_message()
        assert error_msg is not None, "Error message not found after invalid login."
        assert error_msg.strip() == expected_error, f"Expected error '{expected_error}', got '{error_msg.strip()}'"
        assert self.is_on_login_page(), "User is not on the login page after failed login."
