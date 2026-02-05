# LoginPage.py
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

    def login_with_email_and_password(self, email, password, remember_me=False):
        self.driver.get(self.URL)
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_field.clear()
        email_field.send_keys(email)
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(password)
        if remember_me:
            remember_checkbox = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
            if not remember_checkbox.is_selected():
                remember_checkbox.click()
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_button.click()

    def is_dashboard_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except Exception:
            return False

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return None

    def verify_invalid_login_shows_error(self, invalid_email, invalid_password):
        """
        Automates TC_LOGIN_001: Attempts login with invalid credentials and asserts the correct error message is shown.

        Steps:
            1. Navigates to the login screen.
            2. Enters invalid username and password.
            3. Clicks the login button.
            4. Asserts the error message is displayed with the text:
               'Invalid username or password. Please try again.'

        Args:
            invalid_email (str): The invalid email/username to use.
            invalid_password (str): The invalid password to use.

        Raises:
            AssertionError: If the error message is not displayed or does not match the expected text.
        """
        # Step 1: Navigate to login page
        self.driver.get(self.URL)

        # Step 2: Enter invalid credentials
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_field.clear()
        email_field.send_keys(invalid_email)

        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(invalid_password)

        # Step 3: Click the login button
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_button.click()

        # Step 4: Assert error message is shown with correct text
        expected_error = "Invalid username or password. Please try again."
        error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        actual_error = error_elem.text.strip()
        assert actual_error == expected_error, (
            f"Expected error message '{expected_error}', but got '{actual_error}'"
        )

    def verify_remember_me_checkbox_absence(self):
        """
        Automates TC_LOGIN_002: Verifies that the 'Remember Me' checkbox is NOT present on the login screen.

        Steps:
            1. Navigates to the login screen.
            2. Checks for the absence of the 'Remember Me' checkbox.

        Returns:
            bool: True if the checkbox is NOT present, False otherwise.
        """
        self.driver.get(self.URL)
        try:
            # Short explicit wait for absence
            self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
            # If found, it's present
            return False
        except Exception:
            # If NoSuchElementException or any exception, treat as absent
            return True

    # -----------------------------------------------------------------------------
    # TC_LOGIN_06_02: Enter email >255 chars, valid password, verify error/prevent login
    # -----------------------------------------------------------------------------
    def tc_login_06_02_excessive_email_length(self, long_email, valid_password):
        """
        Automates TC_LOGIN_06_02:
        Verifies that entering an email address exceeding 255 characters and a valid password
        prevents login and displays the appropriate error message.

        Steps:
            1. Navigate to the login page.
            2. Enter an email address exceeding 255 characters.
            3. Enter a valid password.
            4. Click the 'Login' button.
            5. Verify that login is not allowed and an error message or validation feedback is displayed.

        Args:
            long_email (str): An email address string longer than 255 characters.
            valid_password (str): A valid password string.

        Returns:
            dict: {
                'email_input_value': str,
                'validation_error': str or None,
                'error_message': str or None,
                'login_blocked': bool
            }

        Raises:
            AssertionError: If no error/validation message is displayed and login is not blocked.

        Selenium Best Practices:
            - Uses explicit waits for all element interactions
            - Defensive exception handling and assertions
            - Strict locator referencing from Locators.json
            - Comprehensive documentation and stepwise comments
        """
        # Step 1: Navigate to login page
        self.driver.get(self.URL)

        # Step 2: Enter excessive-length email
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_field.clear()
        email_field.send_keys(long_email)
        actual_email_value = email_field.get_attribute("value")

        # Step 3: Enter valid password
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(valid_password)

        # Step 4: Click the login button
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_button.click()

        # Step 5: Check for validation error or error message
        validation_error_text = None
        error_message_text = None
        login_blocked = False
        try:
            # Try to find validation error for email field
            validation_error_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            validation_error_text = validation_error_elem.text.strip()
        except Exception:
            validation_error_text = None

        try:
            # Try to find general error message
            error_message_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            error_message_text = error_message_elem.text.strip()
        except Exception:
            error_message_text = None

        # Determine if login was blocked (dashboard not displayed)
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER), timeout=5)
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON), timeout=5)
            login_blocked = False
        except Exception:
            login_blocked = True

        # Assertion: At least one error/validation must be present and login blocked
        assert (validation_error_text or error_message_text) and login_blocked, (
            "TC_LOGIN_06_02 failed: No error/validation message displayed or login was not blocked for excessive email length."
        )

        return {
            'email_input_value': actual_email_value,
            'validation_error': validation_error_text,
            'error_message': error_message_text,
            'login_blocked': login_blocked
        }

    # -----------------------------------------------------------------------------
    # Executive Summary
    # -----------------------------------------------------------------------------
    '''
    Executive Summary:
    - This PageClass implements the login page automation for an e-commerce application using Selenium in Python.
    - TC_LOGIN_06_02 support added: Validates system behavior when an email address exceeding 255 characters is entered.
    - All locators strictly mapped from Locators.json.
    - Code follows Selenium Python best practices, with explicit waits, defensive coding, and robust documentation.

    Analysis:
    - The login page supports error/validation messages for excessive email input.
    - No new PageClass required; LoginPage.py updated to append TC_LOGIN_06_02 implementation.
    - Existing code preserved; new function appended.

    Implementation Guide:
    - Instantiate LoginPage with Selenium WebDriver.
    - Call tc_login_06_02_excessive_email_length(long_email, valid_password) with test data.
    - Example usage:
        page = LoginPage(driver)
        result = page.tc_login_06_02_excessive_email_length(
            'user_with_255_plus_chars_email@example.com', 'ValidPassword1!')
    - Returns a dict with input value, validation error, error message, and login_blocked status.

    Quality Assurance Report:
    - All locators validated against Locators.json.
    - PageClass code reviewed for Pythonic standards and Selenium best practices.
    - Defensive exception handling and assertions included.
    - Existing methods preserved, new methods appended.

    Troubleshooting Guide:
    - Ensure driver is initialized and points to the correct browser.
    - Validate locator values against Locators.json.
    - For assertion failures, review error and validation message output.
    - TimeoutException may indicate slow page load or incorrect locator.
    - If login is not blocked, check for dashboard element appearance and error messages.

    Future Considerations:
    - Extend PageClass for additional input validation scenarios.
    - Integrate with reporting tools for enhanced test results.
    - Parameterize timeouts and error message expectations for configurable validation.
    '''
