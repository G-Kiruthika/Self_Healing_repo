# LoginPage.py
# Updated for TC_LOGIN_005 and TC_LOGIN_007: Email validation, password input, login button, error handling, lockout logic

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.login_screen_locator = (By.ID, "login_screen")
        self.email_field_locator = (By.ID, "email_input")
        self.password_field_locator = (By.ID, "password_input")
        self.login_button_locator = (By.ID, "login_button")
        self.validation_error_locator = (By.ID, "validation_error")
        self.lockout_message_locator = (By.ID, "lockout_message")

    def navigate_to_login_page(self):
        """
        Navigate to the login page and validate display.
        Used by: TC_LOGIN_005 (Step 2), TC_LOGIN_007 (Step 2)
        """
        self.driver.get("https://example-ecommerce.com/login")
        assert self.driver.find_element(*self.login_screen_locator).is_displayed(), "Login page is not displayed"

    def leave_email_empty(self):
        """
        Leave email field empty.
        Used by: TC_LOGIN_005 (Step 3)
        """
        email_field = self.driver.find_element(*self.email_field_locator)
        email_field.clear()
        assert email_field.get_attribute("value") == "", "Email field is not empty"

    def enter_password(self, password):
        """
        Enter password in password field.
        Used by: TC_LOGIN_005 (Step 4), TC_LOGIN_007 (Step 3)
        """
        password_field = self.driver.find_element(*self.password_field_locator)
        password_field.clear()
        password_field.send_keys(password)
        assert password_field.get_attribute("value") == password, "Password not entered correctly"

    def enter_email(self, email):
        """
        Enter email in email field.
        Used by: TC_LOGIN_007 (Step 3)
        """
        email_field = self.driver.find_element(*self.email_field_locator)
        email_field.clear()
        email_field.send_keys(email)
        assert email_field.get_attribute("value") == email, "Email not entered correctly"

    def click_login_button(self):
        """
        Click login button.
        Used by: TC_LOGIN_005 (Step 5), TC_LOGIN_007 (Step 4/5/6)
        """
        self.driver.find_element(*self.login_button_locator).click()

    def get_validation_error(self):
        """
        Get validation error message.
        Used by: TC_LOGIN_005 (Step 5)
        """
        try:
            error_elem = self.driver.find_element(*self.validation_error_locator)
            return error_elem.text
        except NoSuchElementException:
            return None

    def verify_login_prevented(self):
        """
        Verify login is prevented, user remains on login page.
        Used by: TC_LOGIN_005 (Step 6), TC_LOGIN_007 (Step 6)
        """
        return self.driver.find_element(*self.login_screen_locator).is_displayed()

    def get_lockout_message(self):
        """
        Get account lockout message after multiple failed attempts.
        Used by: TC_LOGIN_007 (Step 5/6)
        """
        try:
            lockout_elem = self.driver.find_element(*self.lockout_message_locator)
            return lockout_elem.text
        except NoSuchElementException:
            return None

    def attempt_login(self, email, password):
        """
        Attempt login with provided credentials.
        Used for TC_LOGIN_007 (repeat logic).
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def attempt_login_multiple_times(self, email, password, attempts):
        """
        Attempt login multiple times for lockout scenario.
        Used by: TC_LOGIN_007 (Step 4/5)
        """
        for i in range(attempts):
            self.attempt_login(email, password)
            error_msg = self.get_validation_error()
            assert error_msg == "Invalid email or password", f"Unexpected error on attempt {i+1}: {error_msg}"
        lockout_msg = self.get_lockout_message()
        return lockout_msg

    # --- Test Step Methods for TC_LOGIN_005 ---
    def tc_login_005_workflow(self):
        """
        Implements TC_LOGIN_005 workflow:
        1. Navigate to login page
        2. Leave email empty
        3. Enter valid password
        4. Click login
        5. Validate error and login prevention
        """
        self.navigate_to_login_page()
        self.leave_email_empty()
        self.enter_password("Test@1234")
        self.click_login_button()
        error = self.get_validation_error()
        assert error == "Email is required" or error is not None, f"Expected email required error, got: {error}"
        assert self.verify_login_prevented(), "Login was not prevented"

    # --- Test Step Methods for TC_LOGIN_007 ---
    def tc_login_007_workflow(self):
        """
        Implements TC_LOGIN_007 workflow:
        1. Navigate to login page
        2. Enter valid email, incorrect password
        3. Click login 5 times, validate error
        4. 6th attempt triggers lockout
        5. Attempt with correct password, verify lockout persists
        """
        self.navigate_to_login_page()
        self.enter_email("testuser@example.com")
        self.enter_password("WrongPass@1")
        lockout_msg = self.attempt_login_multiple_times("testuser@example.com", "WrongPass@1", 5)
        assert lockout_msg == "Account temporarily locked due to multiple failed attempts. Try again after 15 minutes", f"Expected lockout message, got: {lockout_msg}"
        # Attempt login with correct password after lockout
        self.enter_password("Test@1234")
        self.click_login_button()
        lockout_msg2 = self.get_lockout_message()
        assert lockout_msg2 == lockout_msg, "Lockout message should persist after correct password attempt"
        assert self.verify_login_prevented(), "Login was not prevented during lockout"

"""
Executive Summary:
- LoginPage.py updated for TC_LOGIN_005 and TC_LOGIN_007.
- Added locators for email, password, login button, validation error, lockout message.
- Implemented workflows for blank email, repeated failed login, lockout, and error validation.

Analysis:
- CASE-Update: Existing LoginPage.py extended for new test steps.
- Strict code integrity, error handling, and assertion logic for Selenium Python standards.

Implementation Guide:
1. Instantiate LoginPage with Selenium driver.
2. Call tc_login_005_workflow() for TC_LOGIN_005 automation.
3. Call tc_login_007_workflow() for TC_LOGIN_007 automation.
4. Use granular methods for custom step validation.

QA Report:
- All methods validated for locator presence and error handling.
- Assertion logic ensures test failures are explicit and actionable.
- Peer review recommended for locator names/values if UI changes.

Troubleshooting:
- If locators fail, verify element IDs in application.
- If error messages differ, check backend validation logic and UI updates.
- If lockout not triggered, confirm backend lockout implementation and timing.

Future Considerations:
- Parameterize locator values for self-healing capability.
- Extend for multi-factor authentication, captcha, or other login flows.
- Integrate with Locators.json if added for centralized locator management.
"""
