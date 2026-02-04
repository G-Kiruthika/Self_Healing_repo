# Selenium Page Object for LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
import time

class LoginPage:
    LOGIN_URL = "https://app.example.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def go_to_login_page(self):
        """Navigate to the login page."""
        self.driver.get(self.LOGIN_URL)

    def is_login_fields_visible(self):
        """Check if login fields are visible."""
        email_visible = self.driver.find_element(*self.EMAIL_FIELD).is_displayed()
        password_visible = self.driver.find_element(*self.PASSWORD_FIELD).is_displayed()
        return email_visible and password_visible

    def enter_email(self, email: str):
        """Enter email address in the email field."""
        email_field = self.driver.find_element(*self.EMAIL_FIELD)
        email_field.clear()
        email_field.send_keys(email)
        return email_field.get_attribute("value") == email

    def enter_password(self, password: str):
        """Enter password in the password field."""
        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)
        # Password field is masked by default; check type attribute
        return password_field.get_attribute("type") == "password"

    def click_login(self):
        """Click the Login button."""
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def is_redirected_to_dashboard(self):
        """Check if redirected to Dashboard."""
        try:
            dashboard_header = self.driver.find_element(*self.DASHBOARD_HEADER)
            user_icon = self.driver.find_element(*self.USER_PROFILE_ICON)
            return dashboard_header.is_displayed() and user_icon.is_displayed()
        except Exception:
            return False

    def is_session_token_created(self):
        """Verify user session is created and profile is displayed."""
        cookies = self.driver.get_cookies()
        session_token = next((cookie for cookie in cookies if 'session' in cookie['name'].lower()), None)
        user_profile_visible = False
        try:
            user_icon = self.driver.find_element(*self.USER_PROFILE_ICON)
            user_profile_visible = user_icon.is_displayed()
        except Exception:
            pass
        return session_token is not None and user_profile_visible

    def is_error_message_displayed(self, expected_message: str = "Invalid email or password"):
        """Verify if error message is displayed after invalid login."""
        try:
            error_element = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_element.is_displayed() and expected_message in error_element.text
        except NoSuchElementException:
            return False

    # --- ADDED FOR TC_LOGIN_002 ---
    def login_with_invalid_credentials(self, email: str, password: str):
        """
        Perform login with invalid credentials and check for error message.
        Steps:
        1. Enter invalid email.
        2. Enter password.
        3. Click login.
        4. Assert error message is displayed and user is not redirected.
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self.is_error_message_displayed("Invalid email or password") and not self.is_redirected_to_dashboard()

    # --- ADDED FOR TC_LOGIN_003 ---
    def login_with_valid_email_and_invalid_password(self, email: str, wrong_password: str):
        """
        Perform login with valid email and invalid password for TC_LOGIN_003.
        Steps:
        1. Navigate to login page
        2. Enter valid email address
        3. Enter incorrect password
        4. Click Login button
        5. Assert error message 'Invalid email or password' is displayed and user remains on login page
        """
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(wrong_password)
        self.click_login()
        error_displayed = self.is_error_message_displayed("Invalid email or password")
        still_on_login_page = self.driver.current_url == self.LOGIN_URL
        return error_displayed and still_on_login_page

    # --- ADDED FOR TC_LOGIN_005 ---
    def login_with_email_and_empty_password(self, email: str):
        """
        TC_LOGIN_005: Attempt login with valid email and empty password, expect 'Password is required' validation error.
        Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Leave password field empty
        4. Click on the Login button
        5. Assert validation error 'Password is required' is displayed below password field
        """
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password("")  # Leave password empty
        self.click_login()
        try:
            validation_error = self.driver.find_element(*self.VALIDATION_ERROR)
            return validation_error.is_displayed() and "Password is required" in validation_error.text
        except NoSuchElementException:
            return False

    # --- ADDED FOR TC_LOGIN_004 ---
    def login_with_empty_email_and_valid_password(self, password: str):
        """
        TC_LOGIN_004: Attempt login with empty email and valid password, expect 'Email is required' validation error.
        Steps:
        1. Navigate to the login page
        2. Leave email field empty
        3. Enter valid password
        4. Click on the Login button
        5. Assert validation error 'Email is required' is displayed below email field and login is prevented
        """
        self.go_to_login_page()
        self.enter_email("")  # Leave email empty
        self.enter_password(password)
        self.click_login()
        try:
            validation_error = self.driver.find_element(*self.VALIDATION_ERROR)
            error_text = validation_error.text if validation_error.is_displayed() else ""
            still_on_login_page = self.driver.current_url == self.LOGIN_URL
            return ("Email is required" in error_text) and still_on_login_page
        except NoSuchElementException:
            return False

    # --- ADDED FOR TC_LOGIN_007 ---
    def check_remember_me_checkbox(self):
        """
        TC_LOGIN_007: Check the 'Remember Me' checkbox on the login page.
        Returns True if checkbox is checked after click.
        """
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()
        return checkbox.is_selected()

    def login_with_remember_me(self, email: str, password: str):
        """
        TC_LOGIN_007: Perform login with 'Remember Me' checked.
        Steps:
        1. Navigate to login page
        2. Enter valid credentials
        3. Check 'Remember Me'
        4. Click login
        """
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.check_remember_me_checkbox()
        self.click_login()
        return self.is_redirected_to_dashboard()

    def verify_remembered_session(self):
        """
        TC_LOGIN_007: After browser restart, verify user is still logged in and redirected to dashboard without login prompt.
        This method assumes cookies/session are restored externally if needed.
        """
        self.driver.get(self.LOGIN_URL)
        # Wait for possible redirect
        time.sleep(2)
        return self.is_redirected_to_dashboard()
