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
    def remember_me_session_persistence(self, email: str, password: str, driver_factory):
        """
        TC_LOGIN_007: End-to-end test for 'Remember Me' session persistence after browser restart.
        Steps:
        1. Navigate to the login page
        2. Enter valid email and password
        3. Check the 'Remember Me' checkbox
        4. Click Login button
        5. Verify user is logged in and redirected to dashboard
        6. Save session cookies, quit browser, start new browser
        7. Load cookies, navigate to app, verify user is still logged in (no login prompt)
        Args:
            email (str): User email
            password (str): User password
            driver_factory (Callable): Function to generate a new WebDriver instance
        Returns:
            bool: True if session persists, False otherwise
        """
        # Step 1-5: Login with remember me
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(email), "Email was not entered correctly!"
        assert self.enter_password(password), "Password was not entered/masked correctly!"
        assert self.check_remember_me(), "Remember Me checkbox was not checked!"
        self.click_login()
        assert self.is_redirected_to_dashboard(), "User was not redirected to dashboard!"
        assert self.is_session_token_created(), "User session was not created!"
        # Step 6: Save cookies
        cookies = self.driver.get_cookies()
        # Step 7: Close and restart browser
        self.driver.quit()
        new_driver = driver_factory()
        new_driver.get(self.LOGIN_URL)
        for cookie in cookies:
            new_driver.add_cookie(cookie)
        new_driver.get(self.LOGIN_URL)
        # Step 8: Verify user is still logged in
        try:
            dashboard_header = new_driver.find_element(*self.DASHBOARD_HEADER)
            user_icon = new_driver.find_element(*self.USER_PROFILE_ICON)
            session_persistent = dashboard_header.is_displayed() and user_icon.is_displayed()
        except Exception:
            session_persistent = False
        new_driver.quit()
        return session_persistent

    # --- ADDED FOR TC_LOGIN_008 ---
    def login_without_remember_me_and_verify_logout_on_restart(self, email: str, password: str, driver_factory):
        """
        TC_LOGIN_008: End-to-end test for login WITHOUT 'Remember Me' and verifying logout after browser restart.
        Steps:
        1. Navigate to the login page
        2. Enter valid email and password
        3. Leave 'Remember Me' checkbox unchecked
        4. Click Login button
        5. Verify user is logged in and redirected to dashboard
        6. Save session cookies, quit browser, start new browser
        7. Load cookies, navigate to app, verify user is logged out and redirected to login page
        Args:
            email (str): User email
            password (str): User password
            driver_factory (Callable): Function to generate a new WebDriver instance
        Returns:
            bool: True if user is logged out after browser restart, False otherwise
        """
        # Step 1-5: Login without remember me
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(email), "Email was not entered correctly!"
        assert self.enter_password(password), "Password was not entered/masked correctly!"
        assert self.uncheck_remember_me(), "Remember Me checkbox was not left unchecked!"
        self.click_login()
        assert self.is_redirected_to_dashboard(), "User was not redirected to dashboard!"
        assert self.is_session_token_created(), "User session was not created!"
        # Step 6: Save cookies
        cookies = self.driver.get_cookies()
        # Step 7: Close and restart browser
        self.driver.quit()
        new_driver = driver_factory()
        new_driver.get(self.LOGIN_URL)
        for cookie in cookies:
            new_driver.add_cookie(cookie)
        new_driver.get(self.LOGIN_URL)
        # Step 8: Verify user is logged out and redirected to login page
        try:
            # If login fields are visible, user is logged out
            login_fields_visible = (
                new_driver.find_element(*self.EMAIL_FIELD).is_displayed() and
                new_driver.find_element(*self.PASSWORD_FIELD).is_displayed()
            )
            redirected_to_login = new_driver.current_url == self.LOGIN_URL
            logged_out = login_fields_visible and redirected_to_login
        except Exception:
            logged_out = False
        new_driver.quit()
        return logged_out

    # --- ADDED FOR TC_LOGIN_019 ---
    def login_failed_counter_reset_workflow(self, email: str, wrong_passwords: list, correct_password: str, wrong_password_after_logout: str):
        """
        TC_LOGIN_019: Test login failed attempt counter reset after successful login and logout.
        Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Attempt login with incorrect password twice
        4. Enter correct password and login
        5. Logout and attempt login with incorrect password
        6. Verify failed attempt counter is reset and no warning about previous failures
        Args:
            email (str): User's email address
            wrong_passwords (list): List of two incorrect passwords
            correct_password (str): The correct password
            wrong_password_after_logout (str): Incorrect password to test after logout
        Returns:
            bool: True if failed attempt counter resets and no warning is shown, False otherwise
        """
        assert len(wrong_passwords) == 2, "Must provide exactly two wrong passwords for initial failed attempts."
        # Step 1: Navigate to login page
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        # Step 2-3: Enter email and attempt login with two wrong passwords
        for wrong_pass in wrong_passwords:
            assert self.enter_email(email), "Email was not entered correctly!"
            assert self.enter_password(wrong_pass), "Wrong password was not entered!"
            self.click_login()
            time.sleep(1)
            error_msg = self.get_error_message()
            assert error_msg is not None, "Expected error message not displayed after wrong password!"
            assert "invalid email or password" in error_msg.lower(), f"Unexpected error message: {error_msg}"
        # Step 4: Enter correct password and login
        assert self.enter_email(email), "Email was not entered correctly!"
        assert self.enter_password(correct_password), "Correct password was not entered!"
        self.click_login()
        assert self.is_redirected_to_dashboard(), "User was not redirected to dashboard after correct login!"
        # Step 5: Logout
        # For demonstration, assume logout is via clicking user icon and a logout button (not shown in locators)
        # This should be implemented as per actual application logic
        try:
            user_icon = self.driver.find_element(*self.USER_PROFILE_ICON)
            user_icon.click()
            logout_button = self.driver.find_element(By.CSS_SELECTOR, "button.logout")
            logout_button.click()
            time.sleep(1)
            assert self.driver.current_url == self.LOGIN_URL, "User was not redirected to login page after logout!"
        except Exception as e:
            raise AssertionError(f"Logout failed: {e}")
        # Step 6: Attempt login again with wrong password
        assert self.enter_email(email), "Email was not entered correctly after logout!"
        assert self.enter_password(wrong_password_after_logout), "Wrong password after logout was not entered!"
        self.click_login()
        time.sleep(1)
        error_msg = self.get_error_message()
        assert error_msg is not None, "Expected error message not displayed after wrong password post-logout!"
        # Step 7: Verify there is NO warning about previous failed attempts (assume any such warning would be present in error_msg)
        assert "previous failures" not in error_msg.lower(), "Warning about previous failures should NOT be displayed!"
        return True

    # --- ADDED FOR TC_LOGIN_020 ---
    def login_with_invalid_email_format_and_valid_password(self, invalid_email: str, valid_password: str):
        """
        TC_LOGIN_020: Attempt login with invalid email format (missing @ symbol) and valid password; verify validation error and login is prevented.
        Steps:
        1. Navigate to the login page
        2. Enter invalid email format (missing @ symbol)
        3. Enter valid password
        4. Click Login button
        5. Verify validation error is displayed: 'Please enter a valid email address'
        6. Verify user remains on login page, login not attempted
        Args:
            invalid_email (str): Email address missing '@' symbol
            valid_password (str): Valid password string
        Returns:
            bool: True if validation error is shown and login is prevented, False otherwise
        """
        self.go_to_login_page()
        assert self.is_login_fields_visible(), "Login fields are not visible!"
        assert self.enter_email(invalid_email), "Invalid email format was not entered correctly!"
        assert self.enter_password(valid_password), "Password was not entered/masked correctly!"
        self.click_login()
        time.sleep(1)  # Wait for validation error
        try:
            validation_error = self.driver.find_element(*self.VALIDATION_ERROR)
            assert validation_error.is_displayed(), "Validation error not displayed!"
            assert "please enter a valid email address" in validation_error.text.lower(), f"Unexpected validation error: {validation_error.text}"
        except NoSuchElementException:
            assert False, "Validation error element not found!"
        # Ensure user remains on login page
        assert self.driver.current_url == self.LOGIN_URL, "User was not on login page after invalid email format!"
        return True
