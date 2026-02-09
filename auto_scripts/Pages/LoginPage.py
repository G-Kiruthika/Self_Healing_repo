from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import jwt
import datetime
from typing import Optional, Dict, Any
import requests
import re

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

    def get_validation_error(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
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
        """
        TC_LOGIN_001: Performs invalid login and validates error message.
        Steps:
            1. Navigate to the login screen.
            2. Enter invalid username and/or password.
            3. Click Login button.
            4. Validate error message 'Invalid username or password. Please try again.' is displayed.
            5. Assert user remains on login page after failed login.
        Args:
            email (str): Invalid email/username.
            invalid_password (str): Invalid password.
        Returns:
            None
        Raises:
            AssertionError: If error message is not as expected or user is not on login page.
        """
        expected_error = "Invalid username or password. Please try again."
        self.login_with_credentials(email, invalid_password)
        error_msg = self.get_error_message()
        assert error_msg is not None, "Error message not found after invalid login."
        assert error_msg.strip() == expected_error, f"Expected error '{expected_error}', got '{error_msg.strip()}'"
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

    @staticmethod
    def register_user_api(user_data: Dict[str, Any]) -> Dict[str, Any]:
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

    def start_forgot_username_workflow(self, email):
        from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
        self.go_to_login_page()
        self.click_forgot_username()
        recovery_page = UsernameRecoveryPage(self.driver)
        return recovery_page.recover_username(email)

    def check_remember_me_checkbox_absence(self):
        self.go_to_login_page()
        elements = self.driver.find_elements(*self.REMEMBER_ME_CHECKBOX)
        assert len(elements) == 0, "'Remember Me' checkbox IS present, but expected to be ABSENT."
        print("'Remember Me' checkbox is absent as expected.")

    def validate_password_special_characters(self, password, expected_message=None):
        """
        Enhanced password validation logic to ensure password includes at least one special character.
        Steps:
            1. Navigate to the login page.
            2. Enter email (dummy or valid).
            3. Enter password.
            4. Click login or trigger validation.
            5. Assert validation error message if password does not meet special character requirement.
        Args:
            password (str): Password to test.
            expected_message (str): Expected validation error message (if any).
        Returns:
            None
        Raises:
            AssertionError: If validation error does not match expectation.
        """
        self.go_to_login_page()
        self.enter_email("test@example.com")  # Using dummy email
        self.enter_password(password)
        self.click_login()

        # Enhanced validation logic: check for at least one special character
        special_char_pattern = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_char_pattern, password):
            validation_error = self.get_validation_error()
            assert validation_error is not None, "No validation error found for password missing special characters."
            expected = expected_message or "Password must contain at least one special character."
            assert expected in validation_error, f"Expected message '{expected}', got '{validation_error}'"
        else:
            error_msg = self.get_error_message()
            assert error_msg is None or error_msg.strip() == "", "Unexpected error message for valid password with special character."

    def execute_tc_101_basic_login_test(self, email, password):
        """
        TC-101: Basic Login Test - Validates successful login functionality.
        Steps:
            1. Navigate to the login page.
            2. Enter valid email and password.
            3. Click Login button.
            4. Validate successful login by checking dashboard elements.
            5. Verify user profile icon is displayed.
        Args:
            email (str): Valid email address.
            password (str): Valid password.
        Returns:
            dict: Test results with step-by-step validation.
        Raises:
            AssertionError: If any validation step fails.
        """
        results = {
            "test_case_id": "1298",
            "test_case_description": "Test Case TC-101",
            "step_1_navigate": False,
            "step_2_enter_credentials": False,
            "step_3_click_login": False,
            "step_4_validate_dashboard": False,
            "step_5_verify_profile_icon": False,
            "overall_pass": False,
            "error_message": None
        }
        
        try:
            # Step 1: Navigate to login page
            self.go_to_login_page()
            results["step_1_navigate"] = self.is_on_login_page()
            assert results["step_1_navigate"], "Failed to navigate to login page"
            
            # Step 2: Enter credentials
            self.enter_email(email)
            self.enter_password(password)
            results["step_2_enter_credentials"] = True
            
            # Step 3: Click login
            self.click_login()
            results["step_3_click_login"] = True
            
            # Step 4: Validate dashboard header is displayed
            try:
                dashboard_header = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
                results["step_4_validate_dashboard"] = dashboard_header.is_displayed()
                assert results["step_4_validate_dashboard"], "Dashboard header not displayed after login"
            except Exception as e:
                results["error_message"] = f"Dashboard validation failed: {str(e)}"
                raise AssertionError(f"Dashboard validation failed: {str(e)}")
            
            # Step 5: Verify user profile icon
            try:
                profile_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
                results["step_5_verify_profile_icon"] = profile_icon.is_displayed()
                assert results["step_5_verify_profile_icon"], "User profile icon not displayed after login"
            except Exception as e:
                results["error_message"] = f"Profile icon validation failed: {str(e)}"
                raise AssertionError(f"Profile icon validation failed: {str(e)}")
            
            # Overall pass if all steps successful
            results["overall_pass"] = all([
                results["step_1_navigate"],
                results["step_2_enter_credentials"],
                results["step_3_click_login"],
                results["step_4_validate_dashboard"],
                results["step_5_verify_profile_icon"]
            ])
            
        except Exception as e:
            results["error_message"] = str(e)
            results["overall_pass"] = False
            raise AssertionError(f"TC-101 execution failed: {str(e)}")
        
        return results