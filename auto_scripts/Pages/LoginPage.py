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

    def is_forgot_password_link_visible(self):
        """Check if 'Forgot Password' link is visible on the login page."""
        try:
            link = self.driver.find_element(*self.FORGOT_PASSWORD_LINK)
            return link.is_displayed()
        except NoSuchElementException:
            return False

    def click_forgot_password_link(self):
        """Click on the 'Forgot Password' link."""
        try:
            link = self.driver.find_element(*self.FORGOT_PASSWORD_LINK)
            link.click()
            return True
        except NoSuchElementException:
            return False

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

    # --- ADDED FOR TC_LOGIN_006 ---
    def login_with_empty_email_and_empty_password(self):
        """
        TC_LOGIN_006: Attempt login with both email and password fields empty. Expect validation errors for both fields and login prevented.
        Steps:
        1. Navigate to the login page
        2. Leave both email and password fields empty
        3. Click on the Login button
        4. Verify validation errors: 'Email is required' and 'Password is required'
        5. Verify user remains on login page, login not attempted
        """
        self.go_to_login_page()
        self.enter_email("")  # Leave email empty
        self.enter_password("")  # Leave password empty
        self.click_login()
        try:
            validation_errors = self.driver.find_elements(*self.VALIDATION_ERROR)
            error_texts = [el.text for el in validation_errors if el.is_displayed()]
            email_error = any("Email is required" in txt for txt in error_texts)
            password_error = any("Password is required" in txt for txt in error_texts)
            still_on_login_page = self.driver.current_url == self.LOGIN_URL
            return email_error and password_error and still_on_login_page
        except NoSuchElementException:
            return False

    # --- ADDED FOR TC_LOGIN_008 ---
    def login_without_remember_me(self, email: str, password: str):
        """
        TC_LOGIN_008: Login with valid credentials, leave 'Remember Me' unchecked, close and restart browser, verify user is logged out.
        Steps:
        1. Navigate to the login page
        2. Enter valid email and password
        3. Ensure 'Remember Me' is unchecked
        4. Click on Login button
        5. Close and restart browser (to be handled in test, not here)
        6. Navigate to the application
        7. Assert user is redirected to login page (not dashboard)
        """
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        if checkbox.is_selected():
            checkbox.click()
        self.click_login()
        return self.is_redirected_to_dashboard()

    def verify_logged_out_after_restart(self):
        """
        TC_LOGIN_008: After browser restart, verify user is logged out and redirected to login page.
        This method should be called after closing and restarting the browser.
        """
        self.driver.get(self.LOGIN_URL)
        time.sleep(2)
        # User should NOT be redirected to dashboard, but see login page
        try:
            login_visible = self.is_login_fields_visible()
            dashboard_visible = self.is_redirected_to_dashboard()
            return login_visible and not dashboard_visible
        except Exception:
            return False

    # --- ADDED FOR TC_LOGIN_009 ---
    def go_to_forgot_password(self):
        """
        TC_LOGIN_009 - Step 1 & 2: Navigate to login page and click 'Forgot Password' link.
        Returns True if redirected to password recovery page.
        """
        self.go_to_login_page()
        if self.is_forgot_password_link_visible():
            self.click_forgot_password_link()
            # Small wait for redirect (adjust as needed)
            time.sleep(2)
            return True
        return False

    # --- ADDED FOR TC_LOGIN_010 ---
    def forgot_password_workflow(self, email: str):
        """
        TC_LOGIN_010: Complete Forgot Password workflow.
        Steps:
        1. Navigate to the password recovery page via Forgot Password link
        2. Enter registered email address
        3. Click on the Submit button
        4. Check for success message
        """
        self.go_to_login_page()
        assert self.is_forgot_password_link_visible(), "Forgot Password link not visible."
        self.click_forgot_password_link()
        # Assuming navigation to PasswordRecoveryPage is successful
        from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
        recovery_page = PasswordRecoveryPage(self.driver)
        assert recovery_page.is_loaded(), "Password Recovery page did not load."
        assert recovery_page.is_email_input_visible(), "Email input not visible on recovery page."
        recovery_page.enter_email(email)
        assert recovery_page.is_submit_button_visible(), "Submit button not visible on recovery page."
        recovery_page.submit_recovery()
        assert recovery_page.is_success_message_displayed(), "Success message not displayed after password recovery."
        return True

    # --- ADDED FOR TC_LOGIN_011 ---
    def login_with_max_length_email(self, email: str, password: str):
        """
        TC_LOGIN_011: Login with email address of maximum valid length (254 characters) and valid password.
        Steps:
        1. Navigate to the login page
        2. Enter email address with 254 characters
        3. Enter valid password
        4. Click on the Login button
        5. Assert email is accepted and displayed, password is masked, and login is processed (success if registered, error if not)
        """
        self.go_to_login_page()
        email_accepted = self.enter_email(email)
        password_masked = self.enter_password(password)
        self.click_login()
        # Accept both possible outcomes: login success or error
        login_success = self.is_redirected_to_dashboard()
        login_error = self.is_error_message_displayed()
        return email_accepted and password_masked and (login_success or login_error)

    # --- ADDED FOR TC_LOGIN_012 ---
    def login_with_email_exceeding_max_length(self, email: str):
        """
        TC_LOGIN_012: Attempt to enter email address exceeding maximum length (255+ characters) and verify validation.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Attempt to enter email address exceeding maximum length (255+ characters)
        3. Verify validation message
        Acceptance Criteria: AC_007
        Expected: Email field either truncates input or shows validation error 'Email exceeds maximum length' or input is truncated.
        """
        self.go_to_login_page()
        email_field = self.driver.find_element(*self.EMAIL_FIELD)
        email_field.clear()
        email_field.send_keys(email)
        actual_value = email_field.get_attribute("value")
        is_truncated = len(actual_value) <= 255
        # Try to submit login to trigger validation
        self.click_login()
        validation_error_msg = None
        try:
            validation_error = self.driver.find_element(*self.VALIDATION_ERROR)
            if validation_error.is_displayed():
                validation_error_msg = validation_error.text
        except NoSuchElementException:
            pass
        error_message_displayed = False
        if validation_error_msg:
            error_message_displayed = "Email exceeds maximum length" in validation_error_msg or "maximum length" in validation_error_msg.lower()
        return is_truncated or error_message_displayed

    # --- ADDED FOR TC_LOGIN_013 ---
    def login_with_sql_injection(self, email: str = "admin'--", password: str = "anything"): 
        """
        TC_LOGIN_013: Attempt login with SQL injection payload in email field.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter SQL injection payload in email field [Test Data: Email: admin'--]
        3. Enter any password [Test Data: Password: anything]
        4. Click on the Login button
        Expected: Login fails with error message, SQL injection is prevented, no unauthorized access granted.
        Acceptance Criteria: SCRUM-91
        """
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        # Assert login fails, error message is displayed, and user is not redirected
        error_displayed = self.is_error_message_displayed()
        not_redirected = self.driver.current_url == self.LOGIN_URL
        unauthorized_access = not self.is_redirected_to_dashboard()
        return error_displayed and not_redirected and unauthorized_access

    # --- ADDED FOR TC_LOGIN_014 ---
    def login_with_sql_injection_email(self, email: str = "admin'--", password: str = "anything"):
        """
        TC_LOGIN_014: Test Case for SQL Injection in Login (Email Field)
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login] [Acceptance Criteria: AC_008]
        2. Enter SQL injection payload in email field [Test Data: Email: admin'--] [Acceptance Criteria: AC_008]
        3. Enter any password [Test Data: Password: anything] [Acceptance Criteria: AC_008]
        4. Click on the Login button [Test Data: N/A] [Acceptance Criteria: AC_008]
        5. Verify system security [Test Data: N/A] [Acceptance Criteria: AC_008]
        Expected:
            - Login page is displayed
            - Input is entered
            - Password is entered
            - Login fails with error message, SQL injection is prevented
            - No unauthorized access granted, system remains secure
        Returns True if all criteria are met
        """
        self.go_to_login_page()
        email_entered = self.enter_email(email)
        password_entered = self.enter_password(password)
        self.click_login()
        # Validation: login fails, error message shown, not redirected, no unauthorized access
        error_displayed = self.is_error_message_displayed()
        still_on_login_page = self.driver.current_url == self.LOGIN_URL
        unauthorized_access = not self.is_redirected_to_dashboard()
        return email_entered and password_entered and error_displayed and still_on_login_page and unauthorized_access
