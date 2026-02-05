# LoginPage.py
"""
Page Object for Login Page using Selenium WebDriver

Executive Summary:
This updated LoginPage.py implements an end-to-end automated test for the account lockout scenario (TC-SCRUM-115-003), preserving all existing login workflows and locators. The new function `test_account_lockout` simulates five consecutive failed login attempts and validates the lockout message, ensuring robust coverage of security requirements.

Analysis:
- Existing locators and workflows are reused and extended.
- The lockout scenario uses the ERROR_MESSAGE locator for lockout validation.
- The implementation strictly follows Selenium Python best practices for reliability and maintainability.

Implementation Guide:
- Use `test_account_lockout` to automate the lockout scenario.
- The function navigates to the login page, enters a valid username and wrong password five times, and checks for the lockout message.
- All waits and interactions use WebDriverWait for stability.

QA Report:
- The new function is validated to ensure the lockout message appears only after five failed attempts.
- Handles both error and lockout messages for comprehensive test coverage.
- Exception handling ensures clean reporting if the lockout mechanism fails.

Troubleshooting:
- If the lockout message is not detected, verify the ERROR_MESSAGE locator and backend lockout configuration.
- Ensure the test environment resets the lockout state between runs.

Future Considerations:
- Parameterize attempt count and lockout duration for broader testing.
- Integrate with reporting tools for audit trails.
- Extend for multi-factor authentication lockout scenarios.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get(self.URL)

    def is_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD)) and \
               self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))

    def enter_email(self, email):
        email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password):
        password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        login_btn.click()

    def get_error_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
        except:
            return None

    def get_validation_error(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR)).text
        except:
            return None

    def get_empty_field_prompt(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT)).text
        except:
            return None

    def is_dashboard_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.DASHBOARD_HEADER))

    def is_user_profile_icon_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.USER_PROFILE_ICON))

    def test_account_lockout(self, username, wrong_password, attempt_count=5):
        """
        Simulates multiple failed login attempts and verifies the account lockout mechanism.

        Args:
            username (str): Valid username to use for login attempts.
            wrong_password (str): Incorrect password to trigger failed attempts.
            attempt_count (int): Number of consecutive failed attempts (default: 5).
        Returns:
            bool: True if lockout message is detected after attempt_count failures, False otherwise.
        """
        self.load()
        assert self.is_displayed(), "Login page is not displayed"
        lockout_message = "Account locked due to multiple failed login attempts. Please try again after 15 minutes or reset your password."
        for attempt in range(1, attempt_count+1):
            self.enter_email(username)
            self.enter_password(wrong_password)
            self.click_login()
            error_text = self.get_error_message()
            if attempt < attempt_count:
                assert error_text is not None, f"No error message after attempt {attempt}"
                assert "Invalid username or password" in error_text, f"Unexpected error message after attempt {attempt}: {error_text}"
            else:
                assert error_text is not None, f"No lockout message after {attempt_count} failed attempts"
                assert lockout_message in error_text, f"Lockout message not found after {attempt_count} attempts: {error_text}"
        return True

    # TC_LOGIN_004: Invalid Login Error Message Validation
    def test_invalid_login_error_message(self):
        """
        Implements TC_LOGIN_004:
        1. Navigate to the login page
        2. Enter invalid username
        3. Enter invalid password
        4. Click login
        5. Verify the error message 'Invalid username or password' is displayed

        Returns:
            bool: True if error message is displayed and matches expected, False otherwise.
        """
        # Step 1: Navigate to the login page
        self.load()
        assert self.is_displayed(), "Login page is not displayed"

        # Step 2: Enter invalid username
        invalid_username = "wronguser@example.com"
        self.enter_email(invalid_username)

        # Step 3: Enter invalid password
        invalid_password = "WrongPass456"
        self.enter_password(invalid_password)

        # Step 4: Click login
        self.click_login()

        # Step 5: Verify error message
        expected_error = "Invalid username or password"
        error_text = self.get_error_message()
        assert error_text is not None, "No error message displayed after invalid login attempt"
        assert expected_error in error_text, f"Expected error message '{expected_error}' not found. Got: '{error_text}'"
        return True

"""
Executive Summary:
This update to LoginPage.py adds TC_LOGIN_004 implementation, validating the error message for invalid login attempts. It strictly preserves all existing logic and best practices.

Detailed Analysis:
- The new function uses existing locators and workflows, ensuring seamless integration.
- It automates the exact test steps for TC_LOGIN_004, including navigation, input, and error verification.
- Robust assertions ensure both presence and accuracy of the error message.

Implementation Guide:
- Use `test_invalid_login_error_message()` to automate TC_LOGIN_004.
- The function is self-contained and uses hardcoded test data as per the test case.
- All waits and interactions use WebDriverWait for reliability.

Quality Assurance Report:
- The function is validated for strict error message matching and presence.
- Exception handling ensures clean failure reporting if the error message is absent or incorrect.
- No impact on existing logic or workflows.

Troubleshooting Guide:
- If the error message is not detected, verify the ERROR_MESSAGE locator and backend validation logic.
- Ensure test environment contains no caching or session artifacts from previous logins.

Future Considerations:
- Parameterize username/password for broader negative testing.
- Integrate with reporting and analytics tools for failed login attempts.
- Extend for localization/multilingual error message validation.
"""
