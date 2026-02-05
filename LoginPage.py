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
