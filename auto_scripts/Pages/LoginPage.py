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
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")

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
        return password_field.get_attribute("type") == "password"

    def check_remember_me(self):
        """Check the Remember Me checkbox."""
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()
        return checkbox.is_selected()

    def uncheck_remember_me(self):
        """Ensure the Remember Me checkbox is unchecked."""
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        if checkbox.is_selected():
            checkbox.click()
        return not checkbox.is_selected()

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

    def get_error_message(self):
        """Fetch error message displayed on login page."""
        try:
            error_elem = self.driver.find_element(*self.ERROR_MESSAGE)
            if error_elem.is_displayed():
                return error_elem.text.strip()
        except NoSuchElementException:
            pass
        return None

    # --- ADDED FOR TC_LOGIN_001 ---
    def login_successful(self, email: str, password: str):
        """
        TC_LOGIN_001: End-to-end login workflow with valid credentials.
        Steps:
        1. Navigate to the login page
        2. Enter valid username
        3. Enter valid password
        4. Click Login button
        5. Verify user session is created and user is redirected to dashboard
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(email), "Username was not entered correctly!"
        assert self.enter_password(password), "Password was not entered/masked correctly!"
        self.click_login()
        assert self.is_redirected_to_dashboard(), "User was not redirected to dashboard!"
        assert self.is_session_token_created(), "User session was not created!"
        return True

    # --- ADDED FOR TC_LOGIN_017 ---
    def login_account_lockout(self, email: str, wrong_passwords: list, correct_password: str):
        """
        TC_LOGIN_017: Test account lockout after multiple failed attempts, and verify lockout persists after correct password.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter valid email and incorrect password, click Login (Attempts 1-5) [Test Data: Email: testuser@example.com, Password: WrongPass1/2/3/4/5]
        3. Verify error message displayed for each failed attempt
        4. On 5th attempt, verify account lockout error message
        5. Attempt login with correct password [Test Data: Password: ValidPass123!]
        6. Verify login is prevented, account remains locked
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        for idx, wrong_password in enumerate(wrong_passwords, 1):
            assert self.enter_email(email), f"Email was not entered correctly for attempt {idx}!"
            assert self.enter_password(wrong_password), f"Wrong password was not entered correctly for attempt {idx}!"
            self.click_login()
            time.sleep(1)
            error_message = self.get_error_message()
            assert error_message is not None, f"No error message displayed for attempt {idx}!"
            if idx < 5:
                assert "invalid" in error_message.lower() or "error" in error_message.lower(), f"Unexpected error message on attempt {idx}: {error_message}"
                assert self.driver.current_url == self.LOGIN_URL, f"User is not on login page after failed attempt {idx}!"
            elif idx == 5:
                assert "account locked" in error_message.lower(), f"Expected account lockout message, got: {error_message}"
        # Attempt login with correct password after lockout
        assert self.enter_email(email), "Email was not entered correctly for locked account!"
        assert self.enter_password(correct_password), "Correct password was not entered correctly for locked account!"
        self.click_login()
        time.sleep(1)
        error_message = self.get_error_message()
        assert error_message is not None, "No error message displayed when account is locked!"
        assert "account locked" in error_message.lower(), f"Expected account locked message after correct password, got: {error_message}"
        assert self.driver.current_url == self.LOGIN_URL, "User is not on login page after locked account attempt!"
        return True

    # --- ADDED FOR TC_LOGIN_020 ---
    def login_invalid_email_format(self, invalid_email: str, password: str):
        """
        TC_LOGIN_020: Attempt login with email missing '@' symbol and verify validation error.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter email in invalid format (missing @ symbol) [Test Data: Email: testuserexample.com]
        3. Enter valid password [Test Data: Password: ValidPass123!]
        4. Click on the Login button
        5. Validation error 'Please enter a valid email address' is displayed
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(invalid_email), "Invalid email was not entered correctly!"
        assert self.enter_password(password), "Password was not entered/masked correctly!"
        self.click_login()
        # Wait for validation error
        time.sleep(0.5)
        try:
            validation_error_elem = self.driver.find_element(*self.VALIDATION_ERROR)
            assert validation_error_elem.is_displayed(), "Validation error element is not displayed!"
            error_text = validation_error_elem.text.strip()
            assert "valid email" in error_text.lower(), f"Expected validation error for invalid email, got: {error_text}"
            assert error_text == "Please enter a valid email address", f"Unexpected error message: {error_text}"
        except NoSuchElementException:
            raise AssertionError("Validation error for invalid email not found!")
        return True
