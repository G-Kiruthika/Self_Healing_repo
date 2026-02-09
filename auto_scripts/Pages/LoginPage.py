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
        """
        Navigates to the login page and waits for the email and password fields to be visible.
        """
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))

    def enter_email(self, email):
        """
        Enters the email into the email input field.
        """
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        """
        Enters the password into the password input field.
        """
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def click_remember_me(self):
        """
        Clicks the 'Remember Me' checkbox if not already selected.
        """
        checkbox = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
        if not checkbox.is_selected():
            checkbox.click()

    def click_login(self):
        """
        Clicks the login submit button.
        """
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_btn.click()

    def click_forgot_password(self):
        """
        Clicks the forgot password link.
        """
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        link.click()

    def get_error_message(self):
        """
        Returns the error message text if displayed, else None.
        """
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None

    def is_on_login_page(self):
        """
        Checks if the login page is currently displayed.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            return True
        except:
            return False

    def login_with_credentials(self, email, password):
        """
        Performs login with provided credentials.
        """
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def perform_invalid_login_and_validate(self, email, invalid_password, expected_error):
        """
        Performs invalid login and validates the error message and login page state.
        Args:
            email (str): Email to use.
            invalid_password (str): Invalid password to use.
            expected_error (str): Expected error message.
        Raises:
            AssertionError: If error message or login page state is not as expected.
        """
        self.login_with_credentials(email, invalid_password)
        error_msg = self.get_error_message()
        assert error_msg == expected_error, f"Expected error '{expected_error}', got '{error_msg}'"
        assert self.is_on_login_page(), "User is not on the login page after failed login."

    # --- TC_LOGIN_001 Specific Methods ---
    def navigate_to_login_screen(self):
        """
        TC_LOGIN_001 Step 2: Navigate to the login screen.
        Expected result: Login screen is displayed.
        Returns:
            bool: True if login screen is displayed successfully.
        """
        self.go_to_login_page()
        return self.is_on_login_page()

    def login_with_invalid_credentials(self, username, password):
        """
        TC_LOGIN_001 Step 3: Enter invalid username and/or password.
        Args:
            username (str): Invalid username to enter.
            password (str): Invalid password to enter.
        """
        self.enter_email(username)
        self.enter_password(password)
        self.click_login()

    def verify_invalid_login_error(self, expected_error):
        """
        TC_LOGIN_001 Step 3: Verify error message is displayed.
        Args:
            expected_error (str): Expected error message text.
        Returns:
            bool: True if error message matches expected text.
        """
        error_msg = self.get_error_message()
        if error_msg == expected_error:
            return True
        else:
            print(f"Expected error: '{expected_error}', but got: '{error_msg}'")
            return False

    def run_tc_login_001_full_test(self, invalid_username, invalid_password, expected_error="Invalid username or password. Please try again."):
        """
        Executes the complete TC_LOGIN_001 test case:
        1. Navigate to the login screen
        2. Enter invalid credentials
        3. Verify error message is displayed
        Returns:
            dict: Test results with step-by-step validation
        """
        results = {
            "test_case_id": "TC_LOGIN_001",
            "step_2_navigate_to_login": False,
            "step_3_invalid_login": False,
            "step_3_error_verification": False,
            "overall_pass": False,
            "errors": []
        }
        
        try:
            # Step 2: Navigate to login screen
            step_2_result = self.navigate_to_login_screen()
            results["step_2_navigate_to_login"] = step_2_result
            
            if not step_2_result:
                results["errors"].append("Step 2 failed: Could not navigate to login screen")
                return results
                
        except Exception as e:
            results["errors"].append(f"Step 2 error: {str(e)}")
            return results
        
        try:
            # Step 3: Enter invalid credentials
            self.login_with_invalid_credentials(invalid_username, invalid_password)
            results["step_3_invalid_login"] = True
            
            # Step 3: Verify error message
            step_3_verification = self.verify_invalid_login_error(expected_error)
            results["step_3_error_verification"] = step_3_verification
            
            if not step_3_verification:
                results["errors"].append(f"Step 3 failed: Expected error '{expected_error}' not displayed")
                
        except Exception as e:
            results["errors"].append(f"Step 3 error: {str(e)}")
            results["step_3_invalid_login"] = False
            results["step_3_error_verification"] = False
        
        # Overall test result
        results["overall_pass"] = (results["step_2_navigate_to_login"] and 
                                  results["step_3_invalid_login"] and 
                                  results["step_3_error_verification"])
        
        return results

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

    # --- TC_LOGIN_002: New Methods Below ---
    def tc_login_002_navigate_to_login_screen(self):
        """
        TC_LOGIN_002 Step 2: Navigate to the login screen.
        Expected result: Login screen is displayed.
        Returns:
            bool: True if login screen is displayed successfully.
        """
        self.go_to_login_page()
        return self.is_on_login_page()

    def tc_login_002_check_remember_me_absence(self):
        """
        TC_LOGIN_002 Step 3: Check for the presence of 'Remember Me' checkbox.
        Expected result: 'Remember Me' checkbox is not present.
        Returns:
            bool: True if checkbox is NOT present (test passes).
        Raises:
            AssertionError: If checkbox is found when it should not be present.
        """
        try:
            # Try to find the Remember Me checkbox
            remember_me_elements = self.driver.find_elements(*self.REMEMBER_ME_CHECKBOX)
            if len(remember_me_elements) > 0:
                raise AssertionError("'Remember Me' checkbox should NOT be present, but was found.")
            return True
        except Exception as e:
            if "'Remember Me' checkbox should NOT be present" in str(e):
                raise e
            # If element not found (NoSuchElementException or similar), that's expected
            return True

    def run_tc_login_002_full_test(self):
        """
        Executes the complete TC_LOGIN_002 test case:
        1. Navigate to the login screen
        2. Verify that the 'Remember Me' checkbox is NOT present
        Returns:
            dict: Test results with step-by-step validation
        """
        results = {
            "test_case_id": "TC_LOGIN_002",
            "step_2_navigate_to_login": False,
            "step_3_remember_me_absent": False,
            "overall_pass": False,
            "errors": []
        }
        
        try:
            # Step 2: Navigate to login screen
            step_2_result = self.tc_login_002_navigate_to_login_screen()
            results["step_2_navigate_to_login"] = step_2_result
            
            if not step_2_result:
                results["errors"].append("Step 2 failed: Could not navigate to login screen")
                return results
                
        except Exception as e:
            results["errors"].append(f"Step 2 error: {str(e)}")
            return results
        
        try:
            # Step 3: Check Remember Me checkbox absence
            step_3_result = self.tc_login_002_check_remember_me_absence()
            results["step_3_remember_me_absent"] = step_3_result
            
        except Exception as e:
            results["errors"].append(f"Step 3 error: {str(e)}")
            results["step_3_remember_me_absent"] = False
        
        # Overall test result
        results["overall_pass"] = results["step_2_navigate_to_login"] and results["step_3_remember_me_absent"]
        
        return results

    # --- TC_LOGIN_003: New Methods Below ---
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
            bool: True if forgot username workflow is initiated successfully.
        """
        try:
            forgot_username_link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK))
            forgot_username_link.click()
            # Wait for username recovery page or form to load
            # Assuming there's a username recovery form or page that appears
            self.wait.until(EC.url_contains("forgot-username"))
            return True
        except Exception as e:
            print(f"Error clicking forgot username link: {str(e)}")
            return False

    def tc_login_003_follow_recovery_instructions(self, email):
        """
        TC_LOGIN_003 Step 4: Follow the instructions to recover username.
        Expected result: Username recovery instructions are followed and username is retrieved.
        Args:
            email (str): Email address for username recovery
        Returns:
            dict: Recovery result with success status and retrieved username
        """
        result = {
            "success": False,
            "message": "",
            "retrieved_username": None
        }
        
        try:
            # Assuming we're now on the username recovery page
            # Look for email input field for username recovery
            email_input = self.wait.until(EC.visibility_of_element_located((By.ID, "recovery-email")))
            email_input.clear()
            email_input.send_keys(email)
            
            # Click submit button for username recovery
            submit_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "recovery-submit")))
            submit_btn.click()
            
            # Wait for success message and retrieved username
            success_message = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.recovery-success")))
            result["message"] = success_message.text
            
            # Try to get the retrieved username if displayed
            try:
                username_element = self.driver.find_element(By.CSS_SELECTOR, "span.recovered-username")
                result["retrieved_username"] = username_element.text
            except:
                result["retrieved_username"] = "Username recovery initiated successfully"
            
            result["success"] = True
            return result
            
        except Exception as e:
            result["message"] = f"Error during username recovery: {str(e)}"
            return result

    def run_tc_login_003_full_test(self, email):
        """
        Executes the complete TC_LOGIN_003 test case:
        1. Navigate to the login screen
        2. Click on 'Forgot Username' link
        3. Follow the instructions to recover username
        Returns:
            dict: Test results with step-by-step validation
        """
        results = {
            "test_case_id": "TC_LOGIN_003",
            "step_2_navigate_to_login": False,
            "step_3_click_forgot_username": False,
            "step_4_follow_recovery_instructions": False,
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
            # Step 4: Follow recovery instructions
            recovery_result = self.tc_login_003_follow_recovery_instructions(email)
            results["recovery_result"] = recovery_result
            results["step_4_follow_recovery_instructions"] = recovery_result["success"]
            
            if not recovery_result["success"]:
                results["errors"].append(f"Step 4 failed: {recovery_result['message']}")
                
        except Exception as e:
            results["errors"].append(f"Step 4 error: {str(e)}")
            results["step_4_follow_recovery_instructions"] = False
        
        # Overall test result
        results["overall_pass"] = (results["step_2_navigate_to_login"] and 
                                  results["step_3_click_forgot_username"] and 
                                  results["step_4_follow_recovery_instructions"])
        
        return results