import jwt
import datetime
from typing import Optional, Dict, Any
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = 'https://example-ecommerce.com/login'
    EMAIL_FIELD = (By.ID, 'login-email')
    PASSWORD_FIELD = (By.ID, 'login-password')
    REMEMBER_ME_CHECKBOX = (By.ID, 'remember-me')
    LOGIN_SUBMIT_BUTTON = (By.ID, 'login-submit')
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, 'a.forgot-password-link')
    ERROR_MESSAGE = (By.CSS_SELECTOR, 'div.alert-danger')
    VALIDATION_ERROR = (By.CSS_SELECTOR, '.invalid-feedback')
    EMPTY_FIELD_PROMPT = (By.XPATH, '//*[text()="Mandatory fields are required"]')
    DASHBOARD_HEADER = (By.CSS_SELECTOR, 'h1.dashboard-title')
    USER_PROFILE_ICON = (By.CSS_SELECTOR, '.user-profile-name')
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, 'a.forgot-username-link')

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def go_to_login_page(self):
        self.driver.get(self.URL)

    def enter_email(self, email):
        email_field = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD)
        )
        email_field.clear()
        email_field.send_keys(email)

    def enter_password(self, password):
        password_field = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD)
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        login_button = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON)
        )
        login_button.click()

    def click_forgot_username(self):
        forgot_username_link = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK)
        )
        forgot_username_link.click()

    def get_error_message(self) -> Optional[str]:
        try:
            error_element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text
        except Exception:
            return None

    def is_on_login_page(self) -> bool:
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.EMAIL_FIELD)
            )
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.PASSWORD_FIELD)
            )
            return True
        except Exception:
            return False

    def login_with_credentials(self, email, password):
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.DASHBOARD_HEADER)
            )
            return True
        except Exception:
            return False

    def perform_invalid_login_and_validate(self, email, invalid_password):
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(invalid_password)
        self.click_login()
        error_message = self.get_error_message()
        return error_message is not None

    # TC_LOGIN_002 functionality
    def is_remember_me_checkbox_absent(self) -> bool:
        try:
            self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
            return False
        except Exception:
            return True

    def execute_tc_login_002(self) -> Dict[str, Any]:
        results = {
            "step_navigate_to_login": False,
            "step_verify_login_screen": False,
            "step_check_remember_me_absence": False,
            "overall_result": False
        }
        try:
            self.go_to_login_page()
            results["step_navigate_to_login"] = True

            results["step_verify_login_screen"] = self.is_on_login_page()

            results["step_check_remember_me_absence"] = self.is_remember_me_checkbox_absent()

            results["overall_result"] = (
                results["step_navigate_to_login"] and
                results["step_verify_login_screen"] and
                results["step_check_remember_me_absence"]
            )
        except Exception as e:
            results["error"] = str(e)
            results["overall_result"] = False
        return results