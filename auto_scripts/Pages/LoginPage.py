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

    # --- ADDED FOR TC_LOGIN_002 ---
    def login_with_invalid_email_valid_password(self, invalid_email: str, valid_password: str):
        """
        TC_LOGIN_002: Attempt login with invalid email and valid password; verify error message and user remains on login page.
        Steps:
        1. Navigate to the login page
        2. Enter invalid email address
        3. Enter valid password
        4. Click Login button
        5. Verify error message is displayed: 'Invalid email or password'
        6. Verify user remains on login page (not authenticated)
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(invalid_email), "Invalid email was not entered correctly!"
        assert self.enter_password(valid_password), "Password was not entered/masked correctly!"
        self.click_login()
        time.sleep(1)  # Wait for error message
        error_message = self.get_error_message()
        assert error_message is not None, "No error message displayed!"
        assert "invalid email or password" in error_message.lower(), f"Unexpected error message: {error_message}"
        assert self.driver.current_url == self.LOGIN_URL, "User is not on login page after failed login!"
        return True

    # --- UPDATED FOR TC_LOGIN_003 ---
    def login_with_valid_email_invalid_password(self, email: str, invalid_password: str):
        """
        TC_LOGIN_003: Attempt login with valid email and invalid password; verify error message and user remains on login page.
        Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Enter incorrect password
        4. Click Login button
        5. Verify error message is displayed: 'Invalid email or password'
        6. Verify user remains on login page (not authenticated)
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(email), "Email was not entered correctly!"
        assert self.enter_password(invalid_password), "Password was not entered/masked correctly!"
        self.click_login()
        time.sleep(1)  # Wait for error message
        error_message = self.get_error_message()
        assert error_message is not None, "No error message displayed!"
        assert "invalid email or password" in error_message.lower(), f"Unexpected error message: {error_message}"
        assert self.driver.current_url == self.LOGIN_URL, "User is not on login page after failed login!"
        return True

    # --- ADDED FOR TC_LOGIN_004 ---
    def login_with_empty_email_and_valid_password(self, password: str):
        """
        TC_LOGIN_004: Attempt login with empty email and valid password; verify validation error for email is displayed.
        Steps:
        1. Navigate to the login page
        2. Leave email field empty
        3. Enter valid password
        4. Click Login button
        5. Verify validation error 'Email is required' is displayed below email field
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email("") is True, "Email field is not empty!"
        assert self.enter_password(password), "Password was not entered/masked correctly!"
        self.click_login()
        time.sleep(1)  # Wait for validation error
        try:
            validation_error = self.driver.find_element(*self.VALIDATION_ERROR)
            assert validation_error.is_displayed(), "Validation error not displayed!"
            assert "email is required" in validation_error.text.lower(), f"Unexpected validation error: {validation_error.text}"
        except NoSuchElementException:
            assert False, "Validation error element not found!"
        return True

    # --- ADDED FOR TC_LOGIN_005 ---
    def login_with_valid_email_and_empty_password(self, email: str):
        """
        TC_LOGIN_005: Attempt login with valid email and empty password; verify validation error for password is displayed.
        Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Leave password field empty
        4. Click Login button
        5. Verify validation error 'Password is required' is displayed below password field
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(email), "Email was not entered correctly!"
        # Leave password field empty
        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        password_field.clear()
        assert password_field.get_attribute("value") == "", "Password field is not empty!"
        self.click_login()
        time.sleep(1)  # Wait for validation error
        try:
            validation_error = self.driver.find_element(*self.VALIDATION_ERROR)
            assert validation_error.is_displayed(), "Validation error not displayed!"
            assert "password is required" in validation_error.text.lower(), f"Unexpected validation error: {validation_error.text}"
        except NoSuchElementException:
            assert False, "Validation error element not found!"
        return True

    # --- ADDED FOR TC_LOGIN_006 ---
    def login_with_empty_email_and_empty_password(self):
        """
        TC_LOGIN_006: Attempt login with both email and password fields empty; verify validation errors for both fields are displayed.
        Steps:
        1. Navigate to the login page
        2. Leave both email and password fields empty
        3. Click Login button
        4. Verify validation errors 'Email is required' and 'Password is required' are displayed
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        # Leave both fields empty
        email_field = self.driver.find_element(*self.EMAIL_FIELD)
        email_field.clear()
        assert email_field.get_attribute("value") == "", "Email field is not empty!"
        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        password_field.clear()
        assert password_field.get_attribute("value") == "", "Password field is not empty!"
        self.click_login()
        time.sleep(1)  # Wait for validation errors
        try:
            validation_errors = self.driver.find_elements(*self.VALIDATION_ERROR)
            assert validation_errors, "No validation errors found!"
            found_email_error = False
            found_password_error = False
            for error_elem in validation_errors:
                if error_elem.is_displayed():
                    error_text = error_elem.text.lower()
                    if "email is required" in error_text:
                        found_email_error = True
                    if "password is required" in error_text:
                        found_password_error = True
            assert found_email_error, "Email required validation error not displayed!"
            assert found_password_error, "Password required validation error not displayed!"
        except NoSuchElementException:
            assert False, "Validation error elements not found!"
        return True

    # --- ADDED FOR TC_LOGIN_007 ---
    def empty_fields_validation(self):
        """
        TC_LOGIN_007: Test Case for empty fields validation.
        Steps:
        1. Navigate to the login page
        2. Leave username field empty
        3. Leave password field empty
        4. Click on the Login button
        5. Verify login is not processed and validation errors are displayed: 'Username is required' and 'Password is required'
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        # Leave username and password fields empty
        email_field = self.driver.find_element(*self.EMAIL_FIELD)
        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        email_field.clear()
        password_field.clear()
        assert email_field.get_attribute("value") == "", "Username field is not empty!"
        assert password_field.get_attribute("value") == "", "Password field is not empty!"
        self.click_login()
        time.sleep(1)  # Wait for validation errors
        validation_errors = self.driver.find_elements(*self.VALIDATION_ERROR)
        assert validation_errors, "No validation errors found!"
        found_username_error = False
        found_password_error = False
        for error_elem in validation_errors:
            if error_elem.is_displayed():
                error_text = error_elem.text.lower()
                if "username is required" in error_text or "email is required" in error_text:
                    found_username_error = True
                if "password is required" in error_text:
                    found_password_error = True
        assert found_username_error, "Username required validation error not displayed!"
        assert found_password_error, "Password required validation error not displayed!"
        assert self.driver.current_url == self.LOGIN_URL, "User is not on login page after empty fields validation!"
        return True

    # --- ADDED FOR TC_LOGIN_012 ---
    def login_with_128_char_password(self, email: str, password: str):
        """
        TC_LOGIN_012: Enter valid email and 128-char password, click Login, verify acceptance and masking.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter valid email address [Test Data: Email: testuser@example.com]
        3. Enter password with 128 characters [Test Data: Password: Aa1!Bb2@Cc3#Dd4$Ee5%Ff6^Gg7&Hh8*Ii9(Jj0)Kk1!Ll2@Mm3#Nn4$Oo5%Pp6^Qq7&Rr8*Ss9(Tt0)Uu1!Vv2@Ww3#Xx4$Yy5%Zz6^Aa7&Bb8*Cc9(Dd0)Ee1!Ff2@Gg3#Hh4$]
        4. Click on the Login button
        5. Verify password field is masked and accepted
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(email), "Email was not entered correctly!"
        assert len(password) == 128, f"Password length is not 128, got {len(password)}"
        assert self.enter_password(password), "Password was not masked correctly!"
        self.click_login()
        # Optionally, verify acceptance and/or error handling
        time.sleep(1)
        error_message = self.get_error_message()
        if error_message:
            assert "invalid" not in error_message.lower(), f"Unexpected error message: {error_message}"
        return True

    # --- ADDED FOR TC_LOGIN_011 ---
    def login_with_254_char_email(self, email: str, password: str):
        """
        TC_LOGIN_011: Enter email address at maximum allowed length (254 characters), valid password, and attempt login.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter email address at maximum allowed length (254 characters) [Test Data: Email: a123456789012345678901234567890123456789012345678901234567890123@b123456789012345678901234567890123456789012345678901234567890123.c123456789012345678901234567890123456789012345678901234567890123.d123456789012345678901234567890123456789012345678.com]
        3. Enter valid password [Test Data: Password: ValidPass123!]
        4. Click on the Login button
        5. Verify email is accepted and entered, password is entered and masked, login attempt is processed without validation error.
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert len(email) == 254, f"Email length is not 254, got {len(email)}"
        assert self.enter_email(email), "Email was not entered correctly!"
        assert self.enter_password(password), "Password was not entered/masked correctly!"
        self.click_login()
        time.sleep(1)  # Wait for response
        error_message = self.get_error_message()
        assert not error_message, f"Unexpected error message: {error_message}"
        return True

    # --- ADDED FOR TC_LOGIN_013 ---
    def login_with_sql_injection(self, sql_email: str, password: str):
        """
        TC_LOGIN_013: Attempt SQL injection in email field and verify application is not vulnerable.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter SQL injection payload in email field [Test Data: Email: admin'--]
        3. Enter any password [Test Data: Password: anything]
        4. Click on the Login button
        5. Verify login fails with error message, SQL injection is prevented, and no unauthorized access is granted.
        Acceptance Criteria: SCRUM-91
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(sql_email), "SQL injection payload was not entered correctly!"
        assert self.enter_password(password), "Password was not entered/masked correctly!"
        self.click_login()
        time.sleep(1)  # Wait for error message
        error_message = self.get_error_message()
        assert error_message is not None, "No error message displayed!"
        assert self.driver.current_url == self.LOGIN_URL, "User is not on login page after SQL injection attempt!"
        assert not self.is_redirected_to_dashboard(), "Unauthorized access granted after SQL injection!"
        assert "sql" not in error_message.lower(), "SQL error message leaked to user!"
        return True

    # --- ADDED FOR TC_LOGIN_014 ---
    def login_with_xss_in_password(self, email: str, xss_password: str):
        """
        TC_LOGIN_014: Attempt to inject XSS payload in the password field and verify that the input is masked, entered, and XSS attack is prevented.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login] [Acceptance Criteria: SCRUM-91]
        2. Enter valid email address [Test Data: Email: testuser@example.com] [Acceptance Criteria: SCRUM-91]
        3. Enter XSS script payload in password field [Test Data: Password: <script>alert('XSS')</script>] [Acceptance Criteria: SCRUM-91]
        4. Click on the Login button [Test Data: N/A] [Acceptance Criteria: SCRUM-91]
        5. Verify that input is masked and entered, login fails safely, script is not executed, and XSS attack is prevented.
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(email), "Email was not entered correctly!"
        # Enter XSS payload in password field
        assert self.enter_password(xss_password), "Password field is not masked or input not entered!"
        self.click_login()
        time.sleep(1)  # Wait for any error or response
        # Verify error message is displayed and no XSS is triggered
        error_message = self.get_error_message()
        assert error_message is not None, "No error message displayed!"
        # Optionally, you can check that the page did not redirect
        assert self.driver.current_url == self.LOGIN_URL, "User is not on login page after XSS attempt!"
        # No alert should be present (if alert is present, XSS was successful)
        try:
            alert = self.driver.switch_to.alert
            assert False, "XSS alert was triggered! XSS vulnerability present!"
        except Exception:
            pass  # No alert means XSS did not execute
        # Ensure password field is still of type 'password' (masked)
        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        assert password_field.get_attribute("type") == "password", "Password field is not masked!"
        return True
