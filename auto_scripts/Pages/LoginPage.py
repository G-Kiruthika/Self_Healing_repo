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
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))

    def enter_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def click_remember_me(self):
        checkbox = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
        if not checkbox.is_selected():
            checkbox.click()

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_btn.click()

    def click_forgot_password(self):
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        link.click()

    def click_forgot_username(self):
        """
        Clicks the forgot username link to initiate the username recovery workflow.
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

    def navigate_to_login_screen(self):
        self.go_to_login_page()
        return self.is_on_login_page()

    def login_with_invalid_credentials(self, username, password):
        self.enter_email(username)
        self.enter_password(password)
        self.click_login()

    def verify_invalid_login_error(self, expected_error):
        error_msg = self.get_error_message()
        if error_msg == expected_error:
            return True
        else:
            print(f"Expected error: '{expected_error}', but got: '{error_msg}'")
            return False

    def run_tc_login_001_full_test(self, invalid_username, invalid_password, expected_error="Invalid username or password. Please try again."):
        results = {
            "test_case_id": "TC_LOGIN_001",
            "step_2_navigate_to_login": False,
            "step_3_invalid_login": False,
            "step_3_error_verification": False,
            "overall_pass": False,
            "errors": []
        }
        try:
            step_2_result = self.navigate_to_login_screen()
            results["step_2_navigate_to_login"] = step_2_result
            if not step_2_result:
                results["errors"].append("Step 2 failed: Could not navigate to login screen")
                return results
        except Exception as e:
            results["errors"].append(f"Step 2 error: {str(e)}")
            return results
        try:
            self.login_with_invalid_credentials(invalid_username, invalid_password)
            results["step_3_invalid_login"] = True
            step_3_verification = self.verify_invalid_login_error(expected_error)
            results["step_3_error_verification"] = step_3_verification
            if not step_3_verification:
                results["errors"].append(f"Step 3 failed: Expected error '{expected_error}' not displayed")
        except Exception as e:
            results["errors"].append(f"Step 3 error: {str(e)}")
            results["step_3_invalid_login"] = False
            results["step_3_error_verification"] = False
        results["overall_pass"] = (results["step_2_navigate_to_login"] and results["step_3_invalid_login"] and results["step_3_error_verification"])
        return results

    @staticmethod
    def validate_jwt_token(token: str, secret: Optional[str] = None, algorithms: Optional[list] = None) -> Dict:
        if algorithms is None:
            algorithms = ["HS256"]
        try:
            if secret:
                payload = jwt.decode(token, secret, algorithms=algorithms)
            else:
                payload = jwt.decode(token, options={"verify_signature": False}, algorithms=algorithms)
            assert "userId" in payload, "userId claim missing in token"
            assert "email" in payload, "email claim missing in token"
            assert "exp" in payload, "Expiration (exp) claim missing in token"
            exp_time = datetime.datetime.fromtimestamp(payload["exp"])
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
            assert "sub" in payload, "Subject (sub) claim missing in token"
            assert "exp" in payload, "Expiration (exp) claim missing in token"
            assert "iat" in payload, "Issued at (iat) claim missing in token"
            assert isinstance(payload["exp"], int), "Expiration (exp) must be integer timestamp"
            exp_time = datetime.datetime.fromtimestamp(payload["exp"])
            assert exp_time > datetime.datetime.utcnow(), "Token has expired"
            return payload
        except Exception as e:
            raise AssertionError(f"JWT decode/validation failed: {e}")

    def tc_login_002_navigate_to_login_screen(self):
        self.go_to_login_page()
        return self.is_on_login_page()

    def tc_login_002_check_remember_me_absence(self):
        try:
            remember_me_elements = self.driver.find_elements(*self.REMEMBER_ME_CHECKBOX)
            if len(remember_me_elements) > 0:
                raise AssertionError("'Remember Me' checkbox should NOT be present, but was found.")
            return True
        except Exception as e:
            if "'Remember Me' checkbox should NOT be present" in str(e):
                raise e
            return True

    def run_tc_login_002_full_test(self):
        results = {
            "test_case_id": "TC_LOGIN_002",
            "step_2_navigate_to_login": False,
            "step_3_remember_me_absent": False,
            "overall_pass": False,
            "errors": []
        }
        try:
            step_2_result = self.tc_login_002_navigate_to_login_screen()
            results["step_2_navigate_to_login"] = step_2_result
            if not step_2_result:
                results["errors"].append("Step 2 failed: Could not navigate to login screen")
                return results
        except Exception as e:
            results["errors"].append(f"Step 2 error: {str(e)}")
            return results
        try:
            step_3_result = self.tc_login_002_check_remember_me_absence()
            results["step_3_remember_me_absent"] = step_3_result
        except Exception as e:
            results["errors"].append(f"Step 3 error: {str(e)}")
            results["step_3_remember_me_absent"] = False
        results["overall_pass"] = results["step_2_navigate_to_login"] and results["step_3_remember_me_absent"]
        return results

    # --- TC_LOGIN_003 Specific Methods ---
    def tc_login_003_navigate_to_login_screen(self):
        """
        TC_LOGIN_003 Step 2: Navigate to the login screen.
        Expected result: Login screen is displayed.
        Returns:
            bool: True if login screen is displayed successfully.
        """
        self.go_to_login_page()
        return self.is_on_login_page()

    def tc_login_003_click_forgot_username_link(self):
        """
        TC_LOGIN_003 Step 3: Click on 'Forgot Username' link.
        Expected result: 'Forgot Username' workflow is initiated.
        Returns:
            bool: True if the forgot username link was clicked successfully.
        """
        try:
            self.click_forgot_username()
            return True
        except Exception as e:
            print(f"Error clicking forgot username link: {str(e)}")
            return False

    def run_tc_login_003_full_test(self, recovery_email):
        """
        Executes the complete TC_LOGIN_003 test case:
        1. Navigate to the login screen
        2. Click on 'Forgot Username' link
        3. Follow the instructions to recover username
        Args:
            recovery_email (str): Email address to use for username recovery
        Returns:
            dict: Test results with step-by-step validation
        """
        results = {
            "test_case_id": "TC_LOGIN_003",
            "step_2_navigate_to_login": False,
            "step_3_click_forgot_username": False,
            "step_4_username_recovery": False,
            "overall_pass": False,
            "errors": [],
            "recovery_result": None
        }
        
        try:
            # Step 2: Navigate to login screen
            step_2_result = self.tc_login_003_navigate_to_login_screen()
            results["step_2_navigate_to_login"] = step_2_result
            
            if not step_2_result:
                results["errors"].append("Step 2 failed: Could not navigate to login screen")
                return results
                
        except Exception as e:
            results["errors"].append(f"Step 2 error: {str(e)}")
            return results
        
        try:
            # Step 3: Click forgot username link
            step_3_result = self.tc_login_003_click_forgot_username_link()
            results["step_3_click_forgot_username"] = step_3_result
            
            if not step_3_result:
                results["errors"].append("Step 3 failed: Could not click forgot username link")
                return results
                
        except Exception as e:
            results["errors"].append(f"Step 3 error: {str(e)}")
            results["step_3_click_forgot_username"] = False
            return results
        
        try:
            # Step 4: Follow instructions to recover username
            from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
            username_recovery_page = UsernameRecoveryPage(self.driver)
            recovery_result = username_recovery_page.run_tc_login_003_username_recovery(recovery_email)
            results["recovery_result"] = recovery_result
            results["step_4_username_recovery"] = recovery_result.get("success", False)
            
            if not results["step_4_username_recovery"]:
                results["errors"].append(f"Step 4 failed: {recovery_result.get('message', 'Username recovery failed')}")
                
        except Exception as e:
            results["errors"].append(f"Step 4 error: {str(e)}")
            results["step_4_username_recovery"] = False
        
        # Overall test result
        results["overall_pass"] = (results["step_2_navigate_to_login"] and 
                                  results["step_3_click_forgot_username"] and 
                                  results["step_4_username_recovery"])
        
        return results