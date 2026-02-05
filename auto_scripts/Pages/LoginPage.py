from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
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

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to_login_page(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

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
        except:
            return None

    def is_on_login_page(self):
        # Check for presence of login form elements
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            return True
        except:
            return False

    def login_with_credentials(self, email, password):
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def perform_invalid_login_and_validate(self, email, invalid_password, expected_error):
        self.login_with_credentials(email, invalid_password)
        error_msg = self.get_error_message()
        assert error_msg == expected_error, f"Expected error '{expected_error}', got '{error_msg}'"
        assert self.is_on_login_page(), "User is not on the login page after failed login."

    def login_with_unicode_and_special_characters(self, email="üser+name@example.com", password="P@sswørd!🔒"):
        """
        Test Case TC019: Enter valid email and password containing special characters and Unicode.
        - Inputs: email (default: üser+name@example.com), password (default: P@sswørd!🔒)
        - Verifies that input fields accept Unicode and special characters
        - Submits login and verifies successful login via dashboard header and user profile icon
        """
        self.go_to_login_page()

        # Enter email and validate input value
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)
        actual_email_value = email_input.get_attribute("value")
        assert actual_email_value == email, f"Email field did not accept Unicode/special characters. Expected: {email}, Got: {actual_email_value}"

        # Enter password and validate input value
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)
        actual_password_value = password_input.get_attribute("value")
        assert actual_password_value == password, f"Password field did not accept Unicode/special characters. Expected: {password}, Got: {actual_password_value}"

        # Submit login
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_btn.click()

        # Verify successful login via dashboard header and user profile icon
        dashboard_header = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
        user_profile_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
        assert dashboard_header.is_displayed(), "Dashboard header is not displayed after login."
        assert user_profile_icon.is_displayed(), "User profile icon is not displayed after login."

    def tc_login_08_remember_me_not_checked(self, email="user1@example.com", password="ValidPassword123", driver_factory=None):
        """
        Test Case TC_LOGIN_08:
        1. Navigate to the login page.
        2. Enter a valid registered email and password.
        3. Ensure 'Remember Me' is NOT checked.
        4. Click on the 'Login' button.
        5. Close and reopen the browser, revisit the site, and verify the user is logged out and redirected to the login page.

        Args:
            email (str): Valid registered email.
            password (str): Valid password.
            driver_factory (callable): Function that returns a new WebDriver instance. Required for browser restart simulation.
        """
        assert driver_factory is not None, "A driver_factory callable must be provided to reopen the browser."

        # Step 1: Navigate to login page
        self.go_to_login_page()
        assert self.is_on_login_page(), "Login page is not displayed."

        # Step 2: Enter valid credentials
        self.enter_email(email)
        self.enter_password(password)

        # Step 3: Ensure 'Remember Me' is NOT checked
        remember_me_elem = self.wait.until(EC.visibility_of_element_located(self.REMEMBER_ME_CHECKBOX))
        if remember_me_elem.is_selected():
            remember_me_elem.click()  # Uncheck if checked
        assert not remember_me_elem.is_selected(), "'Remember Me' checkbox should NOT be selected."

        # Step 4: Click Login
        self.click_login()
        dashboard_header = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
        user_profile_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
        assert dashboard_header.is_displayed(), "Dashboard header is not displayed after login."
        assert user_profile_icon.is_displayed(), "User profile icon is not displayed after login."

        # Step 5: Close and reopen browser, revisit site
        self.driver.quit()
        new_driver = driver_factory()
        try:
            new_wait = WebDriverWait(new_driver, 10)
            new_driver.get(self.URL)
            # Should be redirected to login page (not logged in)
            email_field = new_wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            password_field = new_wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            assert email_field.is_displayed(), "Email field is not displayed after reopening browser. User may still be logged in."
            assert password_field.is_displayed(), "Password field is not displayed after reopening browser. User may still be logged in."
        finally:
            new_driver.quit()
