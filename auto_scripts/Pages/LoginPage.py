from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import jwt
import datetime
from typing import Optional, Dict, Any
import requests
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage

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
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")

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

    def click_forgot_username(self):
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK))
        link.click()

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return None

    def is_on_login_page(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            return True
        except Exception:
            return False

    def login_with_credentials(self, email, password):
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def perform_invalid_login_and_validate(self, email, invalid_password):
        expected_error = "Invalid username or password. Please try again."
        self.login_with_credentials(email, invalid_password)
        error_msg = self.get_error_message()
        assert error_msg is not None, "Error message not found after invalid login."
        assert error_msg.strip() == expected_error, f"Expected error '{expected_error}', got '{error_msg.strip()}'"
        assert self.is_on_login_page(), "User is not on the login page after failed login."

    # TC_LOGIN_002 functionality
    def navigate_and_verify_login_screen(self):
        """
        Step 2: Navigate to the login screen and verify it's displayed.
        Returns True if both email and password fields are visible, False otherwise.
        """
        self.go_to_login_page()
        return self.is_on_login_page()

    def verify_remember_me_checkbox_absence(self):
        """
        Step 3: Check for the presence of 'Remember Me' checkbox and verify it's NOT present.
        Returns True if checkbox is absent, False if present.
        """
        try:
            # Try to find the checkbox, wait 2 seconds max
            self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
            return False  # Checkbox found, should NOT be present
        except Exception:
            return True  # Checkbox not found, as expected

    def execute_tc_login_002(self):
        """
        Complete execution of TC_LOGIN_002 test case.
        Returns dict with step results and overall pass/fail status.
        """
        results = {}
        
        # Step 2: Navigate to login screen
        try:
            step2_result = self.navigate_and_verify_login_screen()
            results["step_2_navigate_login"] = step2_result
            assert step2_result, "Login screen is not displayed"
        except Exception as e:
            results["step_2_navigate_login"] = False
            results["step_2_error"] = str(e)
            results["overall_pass"] = False
            return results
        
        # Step 3: Verify Remember Me checkbox absence
        try:
            step3_result = self.verify_remember_me_checkbox_absence()
            results["step_3_checkbox_absent"] = step3_result
            assert step3_result, "'Remember Me' checkbox is present but should NOT be present"
        except Exception as e:
            results["step_3_checkbox_absent"] = False
            results["step_3_error"] = str(e)
            results["overall_pass"] = False
            return results
        
        results["overall_pass"] = True
        return results

    # TC_LOGIN_003 functionality
    def execute_tc_login_003(self, email):
        """
        Complete execution of TC_LOGIN_003 test case.
        Steps:
            1. Navigate to login screen
            2. Click on 'Forgot Username' link
            3. Follow the instructions to recover username
        Args:
            email (str): Email address for username recovery
        Returns:
            dict: Step-wise results and overall pass/fail status
        """
        results = {}
        try:
            # Step 1: Navigate to login screen
            self.go_to_login_page()
            results["step_1_navigate_login"] = self.is_on_login_page()
            assert results["step_1_navigate_login"], "Login screen is not displayed"

            # Step 2: Click 'Forgot Username' link
            self.click_forgot_username()
            results["step_2_forgot_username_clicked"] = True

            # Step 3: Follow instructions to recover username
            username_recovery_page = UsernameRecoveryPage(self.driver)
            username_recovery_page.go_to_username_recovery()
            username_recovery_page.enter_email(email)
            username_recovery_page.submit_recovery()
            confirmation = username_recovery_page.get_confirmation_message()
            error = username_recovery_page.get_error_message()
            if confirmation:
                results["step_3_recovery_success"] = True
                results["confirmation_message"] = confirmation
                results["overall_pass"] = True
            else:
                results["step_3_recovery_success"] = False
                results["error_message"] = error
                results["overall_pass"] = False
        except Exception as e:
            results["overall_pass"] = False
            results["exception"] = str(e)
        return results