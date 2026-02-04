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

    # --- ADDED FOR TC_LOGIN_003 ---
    def login_invalid_credentials(self, invalid_email: str, valid_password: str):
        """
        TC_LOGIN_003: Attempt login with invalid username and valid password, expect error and stay on login page.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login] [Acceptance Criteria: AC_002_Invalid_Credentials]
        2. Enter invalid username [Test Data: Username: invaliduser@example.com] [Acceptance Criteria: AC_002_Invalid_Credentials]
        3. Enter valid password [Test Data: Password: Test@1234] [Acceptance Criteria: AC_002_Invalid_Credentials]
        4. Click on the Login button [Test Data: N/A] [Acceptance Criteria: AC_002_Invalid_Credentials]
        5. Verify error message is displayed: 'Invalid username or password' and user remains on login page
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(invalid_email), "Invalid username was not entered correctly!"
        assert self.enter_password(valid_password), "Password was not entered/masked correctly!"
        self.click_login()
        # Wait for error message
        time.sleep(1)
        error_message = self.get_error_message()
        assert error_message is not None, "Error message not displayed for invalid credentials!"
        assert "invalid username or password" in error_message.lower(), f"Expected error message 'Invalid username or password', got: {error_message}"
        assert self.driver.current_url == self.LOGIN_URL, "User did not remain on the login page after invalid login!"
        return True

    # --- ADDED FOR TC_LOGIN_018 ---
    def login_three_failed_attempts_warning(self, email: str, wrong_passwords: list):
        """
        TC_LOGIN_018: Attempt login with incorrect password three times, verify warning after third attempt.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login] [Acceptance Criteria: AC_009]
        2. Enter valid email address [Test Data: Email: testuser@example.com] [Acceptance Criteria: AC_009]
        3. Attempt login with incorrect password three times [Test Data: Password: WrongPass1, WrongPass2, WrongPass3] [Acceptance Criteria: AC_009]
        4. Verify warning message after third attempt [Acceptance Criteria: AC_009]
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
            assert self.driver.current_url == self.LOGIN_URL, f"User is not on login page after failed attempt {idx}!"
            if idx == 3:
                assert "Warning: Account will be locked after 2 more failed attempts" in error_message, \
                    f"Expected warning message not found on third attempt: {error_message}"
        return True

    # --- ADDED FOR TC_LOGIN_004 ---
    def login_invalid_credentials_valid_username_invalid_password(self, valid_email: str, invalid_password: str):
        """
        TC_LOGIN_004: Attempt login with valid username and invalid password, expect error and remain on login page.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login] [Acceptance Criteria: AC_002_Invalid_Credentials]
        2. Enter valid username [Test Data: Username: testuser@example.com] [Acceptance Criteria: AC_002_Invalid_Credentials]
        3. Enter invalid password [Test Data: Password: WrongPass@123] [Acceptance Criteria: AC_002_Invalid_Credentials]
        4. Click on the Login button [Test Data: N/A] [Acceptance Criteria: AC_002_Invalid_Credentials]
        5. Verify error message is displayed: 'Invalid username or password' and user remains on login page
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(valid_email), "Valid username was not entered correctly!"
        assert self.enter_password(invalid_password), "Invalid password was not entered/masked correctly!"
        self.click_login()
        # Wait for error message
        time.sleep(1)
        error_message = self.get_error_message()
        assert error_message is not None, "Error message not displayed for invalid credentials!"
        assert "invalid username or password" in error_message.lower(), f"Expected error message 'Invalid username or password', got: {error_message}"
        assert self.driver.current_url == self.LOGIN_URL, "User did not remain on the login page after invalid login!"
        return True

    # --- ADDED FOR TC_LOGIN_007 ---
    def login_empty_fields_validation(self):
        """
        TC_LOGIN_007: Validate login with both username and password fields left empty.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login] [Acceptance Criteria: AC_003_Empty_Fields_Validation]
        2. Leave username field empty [Test Data: Username: (empty)] [Acceptance Criteria: AC_003_Empty_Fields_Validation]
        3. Leave password field empty [Test Data: Password: (empty)] [Acceptance Criteria: AC_003_Empty_Fields_Validation]
        4. Click on the Login button [Test Data: N/A] [Acceptance Criteria: AC_003_Empty_Fields_Validation]
        5. Verify validation errors are displayed: 'Username is required' and 'Password is required'.
        6. Verify login is not processed, user remains on login page and is not authenticated.
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        # Leave both fields empty
        email_field = self.driver.find_element(*self.EMAIL_FIELD)
        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        email_field.clear()
        password_field.clear()
        assert email_field.get_attribute("value") == "", "Username field is not empty!"
        assert password_field.get_attribute("value") == "", "Password field is not empty!"
        self.click_login()
        time.sleep(0.5)
        # Check for validation errors
        validation_errors = []
        try:
            error_elems = self.driver.find_elements(*self.VALIDATION_ERROR)
            for elem in error_elems:
                if elem.is_displayed():
                    validation_errors.append(elem.text.strip())
        except NoSuchElementException:
            pass
        # Accept either combined or separate messages
        assert any("username is required".lower() in err.lower() for err in validation_errors), \
            f"Validation error for empty username not found! Errors: {validation_errors}"
        assert any("password is required".lower() in err.lower() for err in validation_errors), \
            f"Validation error for empty password not found! Errors: {validation_errors}"
        # Verify login is not processed
        assert self.driver.current_url == self.LOGIN_URL, "User is not on login page after empty field validation!"
        # Optionally check user is not authenticated by checking session/cookie/profile icon
        cookies = self.driver.get_cookies()
        session_token = next((cookie for cookie in cookies if 'session' in cookie['name'].lower()), None)
        assert session_token is None, "Session token should not be created for empty fields!"
        try:
            user_icon = self.driver.find_element(*self.USER_PROFILE_ICON)
            assert not user_icon.is_displayed(), "User profile icon should not be displayed for unauthenticated user!"
        except Exception:
            pass
        return True
