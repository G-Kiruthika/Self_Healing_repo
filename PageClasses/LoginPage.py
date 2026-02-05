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

    def click_forgot_username(self):
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK))
        link.click()

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None

    def is_on_login_page(self):
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
        if algorithms is None:
            algorithms = ['HS256']
        try:
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

    @staticmethod
    def login_api(username: str, password: str) -> Dict[str, Any]:
        """
        Sends POST request to /api/auth/login for API-based login.
        Args:
            username (str): Username for login.
            password (str): Password for login.
        Returns:
            dict: Response JSON with JWT tokens and user details.
        Raises:
            AssertionError: If login fails or required fields are missing.
        """
        api_url = "https://example-ecommerce.com/api/auth/login"
        payload = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}
        response = requests.post(api_url, json=payload, headers=headers)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
        data = response.json()
        required_fields = ["accessToken", "refreshToken", "tokenType", "userId", "username", "email"]
        for field in required_fields:
            assert field in data, f"Missing field {field} in login response"
        assert data["tokenType"] == "Bearer", "Token type must be 'Bearer'"
        return data

    # --- TC_SCRUM96_004: New Methods Below ---
    @staticmethod
    def register_user_api(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Registers a user via POST /api/users/register.
        Args:
            user_data (dict): Registration data (username, email, password, firstName, lastName).
        Returns:
            dict: API response JSON.
        Raises:
            AssertionError: If registration fails or required fields are missing.
        """
        api_url = "https://example-ecommerce.com/api/users/register"
        headers = {"Content-Type": "application/json"}
        response = requests.post(api_url, json=user_data, headers=headers)
        assert response.status_code == 201, f"Expected HTTP 201, got {response.status_code}. Response: {response.text}"
        data = response.json()
        required_fields = ["userId", "username", "email", "firstName", "lastName", "accountStatus"]
        for field in required_fields:
            assert field in data, f"Missing field {field} in registration response"
        assert data["accountStatus"] == "ACTIVE", "Account status must be ACTIVE"
        return data

    @staticmethod
    def decode_and_validate_jwt(token: str) -> Dict[str, Any]:
        """
        Decodes and validates JWT structure and claims (subject, expiration, issued at).
        Args:
            token (str): JWT token string.
        Returns:
            dict: Decoded JWT payload.
        Raises:
            AssertionError: If claims are missing or invalid.
        """
        try:
            payload = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256", "RS256"])
            assert 'sub' in payload, "Subject (sub) claim missing in token"
            assert 'exp' in payload, "Expiration (exp) claim missing in token"
            assert 'iat' in payload, "Issued at (iat) claim missing in token"
            assert isinstance(payload['exp'], int), "Expiration (exp) must be integer timestamp"
            exp_time = datetime.datetime.fromtimestamp(payload['exp'])
            assert exp_time > datetime.datetime.utcnow(), "Token has expired"
            return payload
        except Exception as e:
            raise AssertionError(f"JWT decode/validation failed: {e}")
