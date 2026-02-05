import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators loaded from Locators.json
        self.login_url = "https://example-ecommerce.com/login"
        self.email_field = (By.ID, "login-email")
        self.password_field = (By.ID, "login-password")
        self.remember_me_checkbox = (By.ID, "remember-me")
        self.login_button = (By.ID, "login-submit")
        self.forgot_password_link = (By.CSS_SELECTOR, "a.forgot-password-link")
        self.error_message = (By.CSS_SELECTOR, "div.alert-danger")
        self.validation_error = (By.CSS_SELECTOR, ".invalid-feedback")
        self.empty_field_prompt = (By.XPATH, "//*[contains(text(), 'Mandatory fields are required')]")
        self.dashboard_header = (By.CSS_SELECTOR, "h1.dashboard-title")
        self.user_profile_icon = (By.CSS_SELECTOR, ".user-profile-name")

    def open_login_page(self):
        self.driver.get(self.login_url)

    def enter_email(self, email):
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.email_field)
        )
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.password_field)
        )
        password_input.clear()
        password_input.send_keys(password)

    def ensure_remember_me_unchecked(self):
        """
        Ensures the 'Remember Me' checkbox is NOT checked.
        """
        checkbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.remember_me_checkbox)
        )
        if checkbox.is_selected():
            checkbox.click()
        assert not checkbox.is_selected(), "'Remember Me' checkbox should be unchecked."

    def click_login(self):
        login_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        )
        login_btn.click()

    def get_error_message(self):
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message)
            )
            return error.text
        except TimeoutException:
            return None

    def get_password_field_value(self):
        try:
            password_input = self.driver.find_element(*self.password_field)
            return password_input.get_attribute("value")
        except NoSuchElementException:
            return None

    def is_user_logged_in(self):
        """
        Checks if dashboard header and user profile icon are visible (indicating user is logged in).
        """
        try:
            dashboard = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.dashboard_header)
            )
            profile_icon = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.user_profile_icon)
            )
            return dashboard.is_displayed() and profile_icon.is_displayed()
        except TimeoutException:
            return False

    def is_on_login_page(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.email_field)
            )
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.password_field)
            )
            return True
        except TimeoutException:
            return False

    def login_with_credentials(self, email, password):
        self.open_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def login_without_remember_me_and_validate_session(self, email, password, driver_factory):
        """
        Implements TC_LOGIN_08:
        1. Open login page
        2. Enter valid email and password
        3. Ensure 'Remember Me' is NOT checked
        4. Click login
        5. Validate user is logged in
        6. Close and reopen browser, revisit site
        7. Validate user is logged out and redirected to login page
        Args:
            email (str): User email
            password (str): User password
            driver_factory (callable): Function to instantiate a new WebDriver
        Returns:
            dict: Results of each step for validation
        """
        results = {}
        # Step 1: Open login page
        self.open_login_page()
        results['login_page_opened'] = self.is_on_login_page()
        # Step 2: Enter credentials
        self.enter_email(email)
        self.enter_password(password)
        results['credentials_entered'] = True
        # Step 3: Ensure 'Remember Me' is NOT checked
        self.ensure_remember_me_unchecked()
        results['remember_me_unchecked'] = True
        # Step 4: Click Login
        self.click_login()
        time.sleep(2)  # Wait for login to complete
        # Step 5: Validate user is logged in
        results['user_logged_in'] = self.is_user_logged_in()
        # Step 6: Close and reopen browser, revisit site
        self.driver.quit()
        new_driver = driver_factory()
        new_driver.get(self.login_url)
        # Step 7: Validate user is logged out (should see login page)
        try:
            WebDriverWait(new_driver, 10).until(
                EC.visibility_of_element_located(self.email_field)
            )
            results['user_logged_out_after_reopen'] = True
        except TimeoutException:
            results['user_logged_out_after_reopen'] = False
        # Clean up
        new_driver.quit()
        return results

    # TC006: Test login with valid email, empty password, check error message and login failure
    def login_with_valid_email_and_empty_password_tc006(self, email="user@example.com"):
        """
        Steps:
        1. Open login page
        2. Enter valid email ('user@example.com'), leave password empty
        3. Click login
        4. Verify password field remains empty
        5. Check for error message 'Password required'
        6. Confirm login fails
        Returns dict with results of each step.
        """
        results = {}
        self.open_login_page()
        results['page_opened'] = self.driver.current_url == self.login_url
        self.enter_email(email)
        # Leave password field empty (do not call enter_password)
        password_value = self.get_password_field_value()
        results['password_empty'] = (password_value == "" or password_value is None)
        self.click_login()
        time.sleep(1)  # Short wait for error message to appear
        error_msg = self.get_error_message()
        results['error_message_displayed'] = (error_msg == "Password required")
        results['login_failed'] = results['error_message_displayed']
        # Return details for validation
        return results

    # TC010: Multiple invalid login attempts followed by lockout and valid login attempt
    def login_attempts_with_lockout_tc010(self, email="user@example.com", invalid_password="WrongPassword", valid_password="ValidPassword123", attempts=5, lockout_error="Account locked due to multiple failed attempts"):
        """
        Test Case TC010 Implementation:
        1. Attempt login with invalid password 5 times.
        2. Verify error message is displayed after each failed attempt.
        3. Attempt login with correct credentials after lockout.
        4. Verify lockout error message is displayed.
        Args:
            email (str): User email for login.
            invalid_password (str): Invalid password to trigger lockout.
            valid_password (str): Correct password to test lockout.
            attempts (int): Number of invalid attempts before lockout.
            lockout_error (str): Expected lockout error message.
        Returns:
            dict: Detailed stepwise results for validation.
        """
        results = {
            'invalid_attempts': [],
            'lockout_attempt': None
        }
        self.open_login_page()
        for i in range(attempts):
            step_result = {}
            try:
                self.enter_email(email)
                self.enter_password(invalid_password)
                self.click_login()
                time.sleep(1)  # Wait for error message
                error_msg = self.get_error_message()
                step_result['error_message_displayed'] = error_msg is not None
                step_result['error_message_text'] = error_msg
                step_result['login_failed'] = error_msg is not None
            except Exception as ex:
                step_result['exception'] = str(ex)
            results['invalid_attempts'].append(step_result)
        # Attempt with correct credentials after lockout
        lockout_result = {}
        try:
            self.enter_email(email)
            self.enter_password(valid_password)
            self.click_login()
            time.sleep(1)  # Wait for error message
            error_msg = self.get_error_message()
            lockout_result['error_message_displayed'] = error_msg is not None and lockout_error in error_msg
            lockout_result['error_message_text'] = error_msg
            lockout_result['login_failed'] = error_msg is not None and lockout_error in error_msg
        except Exception as ex:
            lockout_result['exception'] = str(ex)
        results['lockout_attempt'] = lockout_result
        return results
