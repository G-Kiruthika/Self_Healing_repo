from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import jwt
import datetime
from typing import Optional, Dict
import time

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
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")  # Added for TC_LOGIN_003

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
        """
        Clicks the 'Forgot Username' link to initiate the recovery workflow.
        """
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK))
        link.click()

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

    @staticmethod
    def validate_jwt_token(token: str, secret: Optional[str] = None, algorithms: Optional[list] = None) -> Dict:
        """
        Decodes and validates a JWT authentication token.
        Checks for userId, email, and expiration time (exp claim).

        Args:
            token (str): JWT token string.
            secret (str, optional): Secret key for decoding (if required).
            algorithms (list, optional): List of algorithms to use for decoding (default ['HS256']).

        Returns:
            dict: Decoded payload if valid.

        Raises:
            AssertionError: If required claims are missing or token is expired.
            jwt.DecodeError: If token is invalid.
        """
        if algorithms is None:
            algorithms = ['HS256']
        try:
            # Decode without verifying signature if secret is not provided (for test env)
            if secret:
                payload = jwt.decode(token, secret, algorithms=algorithms)
            else:
                payload = jwt.decode(token, options={"verify_signature": False}, algorithms=algorithms)
            assert 'userId' in payload, "userId claim missing in token"
            assert 'email' in payload, "email claim missing in token"
            assert 'exp' in payload, "Expiration (exp) claim missing in token"
            exp_time = datetime.datetime.fromtimestamp(payload['exp'])
            assert exp_time > datetime.datetime.utcnow(), "Token has expired"
            return payload
        except jwt.ExpiredSignatureError:
            raise AssertionError("Token has expired")
        except jwt.DecodeError as e:
            raise AssertionError(f"Invalid JWT token: {e}")
        except Exception as e:
            raise AssertionError(f"JWT validation failed: {e}")

    def wait_for_session_timeout_and_verify_logout(self, timeout_duration=900, check_interval=10, max_wait=1800):
        """
        Waits for the session timeout duration and verifies that the user is automatically logged out.
        Args:
            timeout_duration (int): Expected session timeout duration in seconds (default 900s = 15min).
            check_interval (int): Interval in seconds to check for logout (default 10s).
            max_wait (int): Maximum time to wait for logout in seconds (default 1800s = 30min).
        Returns:
            bool: True if logout is detected as expected, raises AssertionError otherwise.
        """
        print(f"Waiting for session timeout ({timeout_duration} seconds)...")
        time.sleep(timeout_duration)
        total_wait = 0
        while total_wait < max_wait:
            # Check if redirected to login page or session expired message appears
            if self.is_on_login_page():
                print("User is on the login page after session timeout. Logout successful.")
                return True
            error_msg = self.get_error_message()
            if error_msg and ("session expired" in error_msg.lower() or "logged out" in error_msg.lower()):
                print(f"Session expired message detected: {error_msg}")
                return True
            time.sleep(check_interval)
            total_wait += check_interval
        raise AssertionError("Session timeout did not result in automatic logout within expected time.")
