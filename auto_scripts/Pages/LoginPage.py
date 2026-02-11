from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import jwt
import datetime
from typing import Optional, Dict, Any
import requests

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

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return None

    def get_validation_errors(self):
        errors = {}
        try:
            email_error_elem = self.driver.find_element(By.ID, "login-email")
            if "invalid" in email_error_elem.get_attribute("class") or email_error_elem.get_attribute("aria-invalid") == "true":
                errors["email"] = "Email is required"
        except Exception:
            pass
        try:
            password_error_elem = self.driver.find_element(By.ID, "login-password")
            if "invalid" in password_error_elem.get_attribute("class") or password_error_elem.get_attribute("aria-invalid") == "true":
                errors["password"] = "Password is required"
        except Exception:
            pass
        return errors

    def are_fields_highlighted_as_required(self):
        highlights = {}
        try:
            email_elem = self.driver.find_element(By.ID, "login-email")
            highlights["email"] = "invalid" in email_elem.get_attribute("class") or email_elem.get_attribute("aria-invalid") == "true"
        except Exception:
            highlights["email"] = False
        try:
            password_elem = self.driver.find_element(By.ID, "login-password")
            highlights["password"] = "invalid" in password_elem.get_attribute("class") or password_elem.get_attribute("aria-invalid") == "true"
        except Exception:
            highlights["password"] = False
        return highlights

    def is_on_login_page(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            return True
        except Exception:
            return False

    def run_tc_login_006(self):
        """
        TC_LOGIN_006: Leave both email and password fields empty, click login, validate error messages and highlights, prevent login.
        Steps:
            1. Navigate to login page.
            2. Leave both fields empty.
            3. Click Login.
            4. Validate errors for both fields.
            5. Verify highlights.
            6. Ensure login is prevented.
        Returns:
            dict: Structured results for validation.
        """
        results = {
            "test_case_id": "4157",
            "test_case_description": "TC_LOGIN_006: Both Email and Password Fields Empty - Validation & Prevention of Login",
            "step_1_navigate_login": False,
            "step_2_leave_fields_empty": False,
            "step_3_click_login": False,
            "step_4_validate_errors": False,
            "step_5_highlight_required": False,
            "step_6_prevent_login": False,
            "overall_pass": False,
            "errors": {},
            "highlights": {},
            "error_message_text": None
        }
        try:
            # Step 1: Navigate to login page
            self.go_to_login_page()
            results["step_1_navigate_login"] = self.is_on_login_page()
            if not results["step_1_navigate_login"]:
                results["error_message_text"] = "Login page is not displayed."
                return results
            # Step 2: Leave both fields empty
            email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_input.clear()
            password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_input.clear()
            results["step_2_leave_fields_empty"] = email_input.get_attribute("value") == "" and password_input.get_attribute("value") == ""
            # Step 3: Click Login
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
            results["step_3_click_login"] = True
            # Step 4: Validate errors for both fields
            errors = self.get_validation_errors()
            results["errors"] = errors
            results["step_4_validate_errors"] = "email" in errors and "password" in errors
            results["error_message_text"] = self.get_error_message()
            # Step 5: Verify highlights
            highlights = self.are_fields_highlighted_as_required()
            results["highlights"] = highlights
            results["step_5_highlight_required"] = highlights["email"] and highlights["password"]
            # Step 6: Ensure login is prevented (user remains on login page)
            results["step_6_prevent_login"] = self.is_on_login_page()
            # Overall pass if all steps pass
            results["overall_pass"] = (
                results["step_1_navigate_login"] and
                results["step_2_leave_fields_empty"] and
                results["step_3_click_login"] and
                results["step_4_validate_errors"] and
                results["step_5_highlight_required"] and
                results["step_6_prevent_login"]
            )
        except Exception as e:
            results["error_message_text"] = f"Test execution failed: {str(e)}"
        return results
