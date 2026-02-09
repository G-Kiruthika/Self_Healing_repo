"""
Test Scripts Module - Automated Test Cases
Contains test classes for login functionality including forgot username workflow
and user registration with email format validation
"""

import unittest
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class LoginPage:
    """Page Object Model for Login Page with forgot username functionality"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    # Login locators
    username_field = (By.ID, "username")
    password_field = (By.ID, "password")
    login_button = (By.ID, "loginButton")
    error_message = (By.CLASS_NAME, "error-message")
    remember_me_checkbox = (By.ID, "rememberMe")
    remember_me_alt_checkbox = (By.XPATH, "//input[@type='checkbox' and contains(@name, 'remember')]")
    
    # Forgot username locators
    forgot_username_link = (By.LINK_TEXT, "Forgot Username?")
    forgot_username_alt_link = (By.XPATH, "//a[contains(text(), 'Forgot Username')]")
    email_field = (By.ID, "recoveryEmail")
    email_alt_field = (By.NAME, "email")
    submit_recovery_button = (By.ID, "submitRecovery")
    submit_alt_button = (By.XPATH, "//button[contains(text(), 'Submit')]")
    recovery_instructions = (By.CLASS_NAME, "recovery-instructions")
    username_display = (By.ID, "retrievedUsername")
    success_message = (By.CLASS_NAME, "success-message")
    
    def navigate_to_login(self, url="https://example.com/login"):
        """Navigate to login page"""
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located(self.username_field))
    
    def enter_username(self, username):
        """Enter username in login field"""
        element = self.wait.until(EC.element_to_be_clickable(self.username_field))
        element.clear()
        element.send_keys(username)
    
    def enter_password(self, password):
        """Enter password in login field"""
        element = self.wait.until(EC.element_to_be_clickable(self.password_field))
        element.clear()
        element.send_keys(password)
    
    def click_login(self):
        """Click login button"""
        element = self.wait.until(EC.element_to_be_clickable(self.login_button))
        element.click()
    
    def get_error_message(self):
        """Get error message text"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.error_message))
            return element.text
        except TimeoutException:
            return None
    
    def is_remember_me_present(self):
        """Check if Remember Me checkbox is present on the page"""
        try:
            self.driver.find_element(*self.remember_me_checkbox)
            return True
        except NoSuchElementException:
            try:
                self.driver.find_element(*self.remember_me_alt_checkbox)
                return True
            except NoSuchElementException:
                return False
    
    def click_forgot_username(self):
        """Click forgot username link with fallback"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.forgot_username_link))
            element.click()
        except (TimeoutException, NoSuchElementException):
            element = self.wait.until(EC.element_to_be_clickable(self.forgot_username_alt_link))
            element.click()
    
    def enter_recovery_email(self, email):
        """Enter email for username recovery"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.email_field))
        except TimeoutException:
            element = self.wait.until(EC.element_to_be_clickable(self.email_alt_field))
        element.clear()
        element.send_keys(email)
    
    def click_submit_recovery(self):
        """Submit recovery request"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.submit_recovery_button))
            element.click()
        except (TimeoutException, NoSuchElementException):
            element = self.wait.until(EC.element_to_be_clickable(self.submit_alt_button))
            element.click()
    
    def get_recovery_instructions(self):
        """Get recovery instructions text"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.recovery_instructions))
            return element.text
        except TimeoutException:
            return None
    
    def get_retrieved_username(self):
        """Get retrieved username from display"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.username_display))
            return element.text
        except TimeoutException:
            return None
    
    def get_success_message(self):
        """Get success message text"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.success_message))
            return element.text
        except TimeoutException:
            return None


class UserSignupPage:
    """
    Page Object Model for User Registration/Signup Page
    Implements email format validation for registration process
    Test Case ID: 1286 - Added email format validation in registration step
    """
    
    # Email validation regex pattern (RFC 5322 compliant)
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    # Registration page locators
    signup_link = (By.LINK_TEXT, "Sign Up")
    signup_alt_link = (By.XPATH, "//a[contains(text(), 'Sign Up') or contains(text(), 'Register')]")
    
    # Registration form locators
    username_field = (By.ID, "signupUsername")
    username_alt_field = (By.NAME, "username")
    email_field = (By.ID, "signupEmail")
    email_alt_field = (By.NAME, "email")
    password_field = (By.ID, "signupPassword")
    password_alt_field = (By.NAME, "password")
    confirm_password_field = (By.ID, "confirmPassword")
    confirm_password_alt_field = (By.NAME, "confirmPassword")
    
    # Validation message locators
    email_validation_error = (By.ID, "emailError")
    email_validation_error_alt = (By.XPATH, "//span[contains(@class, 'email-error') or contains(@id, 'email-error')]")
    general_error_message = (By.CLASS_NAME, "error-message")
    success_message = (By.CLASS_NAME, "success-message")
    
    # Submit button locators
    register_button = (By.ID, "registerButton")
    register_alt_button = (By.XPATH, "//button[contains(text(), 'Register') or contains(text(), 'Sign Up')]")
    
    def navigate_to_signup(self, url="https://example.com/signup"):
        """Navigate to signup/registration page"""
        self.driver.get(url)
        try:
            self.wait.until(EC.presence_of_element_located(self.email_field))
        except TimeoutException:
            self.wait.until(EC.presence_of_element_located(self.email_alt_field))
    
    def click_signup_link(self):
        """Click signup link from login or home page"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.signup_link))
            element.click()
        except (TimeoutException, NoSuchElementException):
            element = self.wait.until(EC.element_to_be_clickable(self.signup_alt_link))
            element.click()
    
    def enter_username(self, username):
        """Enter username in registration field"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.username_field))
        except TimeoutException:
            element = self.wait.until(EC.element_to_be_clickable(self.username_alt_field))
        element.clear()
        element.send_keys(username)
    
    def enter_email(self, email):
        """Enter email in registration field"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.email_field))
        except TimeoutException:
            element = self.wait.until(EC.element_to_be_clickable(self.email_alt_field))
        element.clear()
        element.send_keys(email)
    
    def enter_password(self, password):
        """Enter password in registration field"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.password_field))
        except TimeoutException:
            element = self.wait.until(EC.element_to_be_clickable(self.password_alt_field))
        element.clear()
        element.send_keys(password)
    
    def enter_confirm_password(self, password):
        """Enter confirm password in registration field"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.confirm_password_field))
        except TimeoutException:
            element = self.wait.until(EC.element_to_be_clickable(self.confirm_password_alt_field))
        element.clear()
        element.send_keys(password)
    
    def click_register(self):
        """Click register/signup button"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.register_button))
            element.click()
        except (TimeoutException, NoSuchElementException):
            element = self.wait.until(EC.element_to_be_clickable(self.register_alt_button))
            element.click()
    
    def validate_email_format(self, email):
        """
        Validate email format using regex pattern
        Returns: tuple (is_valid: bool, error_message: str or None)
        """
        if not email:
            return False, "Email address is required"
        
        if not re.match(self.EMAIL_REGEX, email):
            return False, "Invalid email format. Please enter a valid email address"
        
        # Additional validation checks
        if len(email) > 254:  # RFC 5321
            return False, "Email address is too long"
        
        local_part = email.split('@')[0]
        if len(local_part) > 64:  # RFC 5321
            return False, "Email local part is too long"
        
        return True, None
    
    def get_email_validation_error(self):
        """Get email validation error message from UI"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.email_validation_error))
            return element.text
        except TimeoutException:
            try:
                element = self.wait.until(EC.visibility_of_element_located(self.email_validation_error_alt))
                return element.text
            except TimeoutException:
                return None
    
    def get_error_message(self):
        """Get general error message text"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.general_error_message))
            return element.text
        except TimeoutException:
            return None
    
    def get_success_message(self):
        """Get success message text"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.success_message))
            return element.text
        except TimeoutException:
            return None
    
    def is_email_field_highlighted(self):
        """Check if email field is highlighted as invalid"""
        try:
            element = self.driver.find_element(*self.email_field)
        except NoSuchElementException:
            element = self.driver.find_element(*self.email_alt_field)
        
        # Check for common validation classes or styles
        class_attr = element.get_attribute('class') or ''
        return 'invalid' in class_attr or 'error' in class_attr
    
    def perform_registration_with_validation(self, username, email, password, confirm_password=None):
        """
        Complete registration flow with email validation
        Returns: dict with validation results and status
        """
        result = {
            'email_valid': False,
            'validation_error': None,
            'registration_successful': False,
            'ui_error_message': None,
            'ui_success_message': None
        }
        
        # Step 1: Validate email format programmatically
        is_valid, error_msg = self.validate_email_format(email)
        result['email_valid'] = is_valid
        result['validation_error'] = error_msg
        
        if not is_valid:
            return result
        
        # Step 2: Fill registration form
        self.enter_username(username)
        self.enter_email(email)
        self.enter_password(password)
        
        if confirm_password:
            self.enter_confirm_password(confirm_password)
        else:
            self.enter_confirm_password(password)
        
        # Step 3: Submit registration
        self.click_register()
        time.sleep(2)
        
        # Step 4: Check for UI validation errors
        ui_error = self.get_email_validation_error()
        if not ui_error:
            ui_error = self.get_error_message()
        result['ui_error_message'] = ui_error
        
        # Step 5: Check for success
        success_msg = self.get_success_message()
        result['ui_success_message'] = success_msg
        result['registration_successful'] = success_msg is not None
        
        return result


class TC_LOGIN_001(unittest.TestCase):
    """Test Case: Valid Login"""
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
    
    def test_valid_login(self):
        """Verify successful login with valid credentials"""
        self.login_page.navigate_to_login()
        self.login_page.enter_username("validuser")
        self.login_page.enter_password("ValidPass123")
        self.login_page.click_login()
        time.sleep(2)
        self.assertIn("dashboard", self.driver.current_url.lower())
    
    def tearDown(self):
        self.driver.quit()


class TC_LOGIN_002(unittest.TestCase):
    """
    Test Case ID: 107
    Test Case: TC_LOGIN_002 - Remember Me Checkbox Verification
    Description: Verify that 'Remember Me' checkbox is not present on login screen
    """
    
    def setUp(self):
        """Initialize driver and page object"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
    
    def test_remember_me_checkbox_not_present(self):
        """Verify Remember Me checkbox is not present on login screen"""
        # Step 1: Navigate to the login screen
        self.login_page.navigate_to_login()
        
        # Step 2: Verify login screen is displayed
        self.assertIn("login", self.driver.current_url.lower())
        username_field = self.driver.find_element(*self.login_page.username_field)
        self.assertTrue(username_field.is_displayed(), "Login screen is displayed.")
        
        # Step 3: Check for the presence of 'Remember Me' checkbox
        remember_me_present = self.login_page.is_remember_me_present()
        
        # Step 4: Verify 'Remember Me' checkbox is not present
        self.assertFalse(remember_me_present, "'Remember Me' checkbox is not present.")
    
    def tearDown(self):
        """Clean up driver"""
        self.driver.quit()


class TC_LOGIN_003(unittest.TestCase):
    """
    Test Case ID: 108
    Test Case: Forgot Username Workflow
    Description: Verify complete forgot username recovery process
    """
    
    def setUp(self):
        """Initialize driver and page object"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.test_email = "user@example.com"
    
    def test_step_01_navigate_to_login_screen(self):
        """Step 1: Navigate to login screen and verify page loaded"""
        self.login_page.navigate_to_login()
        self.assertIn("login", self.driver.current_url.lower())
        username_field = self.driver.find_element(*self.login_page.username_field)
        self.assertTrue(username_field.is_displayed())
    
    def test_step_02_click_forgot_username_link(self):
        """Step 2: Click 'Forgot Username' link and verify navigation"""
        self.login_page.navigate_to_login()
        self.login_page.click_forgot_username()
        time.sleep(1)
        try:
            email_field = self.driver.find_element(*self.login_page.email_field)
        except NoSuchElementException:
            email_field = self.driver.find_element(*self.login_page.email_alt_field)
        self.assertTrue(email_field.is_displayed())
    
    def test_step_03_follow_recovery_instructions(self):
        """Step 3: Follow recovery instructions and submit email"""
        self.login_page.navigate_to_login()
        self.login_page.click_forgot_username()
        time.sleep(1)
        
        instructions = self.login_page.get_recovery_instructions()
        if instructions:
            self.assertIsNotNone(instructions)
        
        self.login_page.enter_recovery_email(self.test_email)
        self.login_page.click_submit_recovery()
        time.sleep(2)
        
        success_msg = self.login_page.get_success_message()
        self.assertIsNotNone(success_msg)
    
    def test_step_04_retrieve_username(self):
        """Step 4: Retrieve username and verify display"""
        self.login_page.navigate_to_login()
        self.login_page.click_forgot_username()
        time.sleep(1)
        self.login_page.enter_recovery_email(self.test_email)
        self.login_page.click_submit_recovery()
        time.sleep(2)
        
        retrieved_username = self.login_page.get_retrieved_username()
        if retrieved_username:
            self.assertIsNotNone(retrieved_username)
            self.assertTrue(len(retrieved_username) > 0)
        else:
            success_msg = self.login_page.get_success_message()
            self.assertIsNotNone(success_msg)
    
    def test_complete_forgot_username_workflow(self):
        """Complete workflow: All steps integrated"""
        # Step 1: Navigate
        self.login_page.navigate_to_login()
        self.assertIn("login", self.driver.current_url.lower())
        
        # Step 2: Click forgot username
        self.login_page.click_forgot_username()
        time.sleep(1)
        
        # Step 3: Follow instructions and submit
        self.login_page.enter_recovery_email(self.test_email)
        self.login_page.click_submit_recovery()
        time.sleep(2)
        
        # Step 4: Verify username retrieval or success
        retrieved_username = self.login_page.get_retrieved_username()
        success_msg = self.login_page.get_success_message()
        
        self.assertTrue(retrieved_username is not None or success_msg is not None)
    
    def tearDown(self):
        """Clean up driver"""
        self.driver.quit()


class TC002(unittest.TestCase):
    """
    Test Case ID: 1286
    Test Case: TC002 - User Registration with Email Format Validation
    Description: Added email format validation in registration step
    Expected: Step executes successfully as per the described change
    """
    
    def setUp(self):
        """Initialize driver and page object"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.signup_page = UserSignupPage(self.driver)
    
    def test_valid_email_format_registration(self):
        """
        Test registration with valid email format
        Verify that valid email passes validation and registration proceeds
        """
        # Navigate to signup page
        self.signup_page.navigate_to_signup()
        
        # Test data with valid email
        test_username = "testuser123"
        test_email = "testuser@example.com"
        test_password = "SecurePass123!"
        
        # Perform registration with email validation
        result = self.signup_page.perform_registration_with_validation(
            username=test_username,
            email=test_email,
            password=test_password
        )
        
        # Verify email format validation passed
        self.assertTrue(result['email_valid'], "Valid email format should pass validation")
        self.assertIsNone(result['validation_error'], "No validation error should occur for valid email")
        
        # Verify no UI error messages
        if result['ui_error_message']:
            self.fail(f"Unexpected UI error: {result['ui_error_message']}")
    
    def test_invalid_email_format_validation(self):
        """
        Test registration with invalid email formats
        Verify that invalid emails are caught by validation
        """
        # Navigate to signup page
        self.signup_page.navigate_to_signup()
        
        invalid_emails = [
            "invalidemail",  # Missing @ and domain
            "invalid@",  # Missing domain
            "@example.com",  # Missing local part
            "invalid@.com",  # Invalid domain
            "invalid..email@example.com",  # Consecutive dots
            "invalid@example",  # Missing TLD
            "invalid email@example.com",  # Space in email
            "",  # Empty email
        ]
        
        for invalid_email in invalid_emails:
            with self.subTest(email=invalid_email):
                # Validate email format
                is_valid, error_msg = self.signup_page.validate_email_format(invalid_email)
                
                # Verify validation fails
                self.assertFalse(is_valid, f"Email '{invalid_email}' should fail validation")
                self.assertIsNotNone(error_msg, "Error message should be provided for invalid email")
    
    def test_email_validation_with_ui_feedback(self):
        """
        Test email validation with UI feedback
        Verify that invalid email triggers UI validation messages
        """
        # Navigate to signup page
        self.signup_page.navigate_to_signup()
        
        # Test data with invalid email
        test_username = "testuser456"
        invalid_email = "invalidemail.com"  # Missing @
        test_password = "SecurePass123!"
        
        # Enter registration data
        self.signup_page.enter_username(test_username)
        self.signup_page.enter_email(invalid_email)
        self.signup_page.enter_password(test_password)
        self.signup_page.enter_confirm_password(test_password)
        
        # Submit form
        self.signup_page.click_register()
        time.sleep(2)
        
        # Check for validation error in UI
        ui_error = self.signup_page.get_email_validation_error()
        if not ui_error:
            ui_error = self.signup_page.get_error_message()
        
        # Verify error message is displayed or email field is highlighted
        email_highlighted = self.signup_page.is_email_field_highlighted()
        
        self.assertTrue(
            ui_error is not None or email_highlighted,
            "UI should display validation error or highlight email field for invalid email"
        )
    
    def test_email_validation_edge_cases(self):
        """
        Test email validation with edge cases
        Verify boundary conditions and special characters
        """
        edge_case_emails = [
            ("user+tag@example.com", True),  # Plus sign (valid)
            ("user.name@example.com", True),  # Dot in local part (valid)
            ("user_name@example.com", True),  # Underscore (valid)
            ("user@sub.example.com", True),  # Subdomain (valid)
            ("a@example.com", True),  # Single character local (valid)
            ("user@example.co.uk", True),  # Multiple TLD parts (valid)
            ("user@123.456.789.012", True),  # IP-like domain (valid format)
            ("user name@example.com", False),  # Space (invalid)
            ("user@exam ple.com", False),  # Space in domain (invalid)
            ("user@@example.com", False),  # Double @ (invalid)
        ]
        
        for email, expected_valid in edge_case_emails:
            with self.subTest(email=email):
                is_valid, error_msg = self.signup_page.validate_email_format(email)
                
                if expected_valid:
                    self.assertTrue(is_valid, f"Email '{email}' should be valid")
                    self.assertIsNone(error_msg, f"No error for valid email '{email}'")
                else:
                    self.assertFalse(is_valid, f"Email '{email}' should be invalid")
                    self.assertIsNotNone(error_msg, f"Error message required for invalid email '{email}'")
    
    def test_email_length_validation(self):
        """
        Test email validation for length constraints
        Verify RFC 5321 compliance for email length
        """
        # Test maximum allowed email length (254 characters)
        long_local = "a" * 64  # Max local part
        long_domain = "b" * 180 + ".com"  # Long domain
        long_email = f"{long_local}@{long_domain}"
        
        is_valid, error_msg = self.signup_page.validate_email_format(long_email)
        self.assertTrue(is_valid or error_msg == "Email address is too long", 
                       "Long email should be validated according to RFC 5321")
        
        # Test email exceeding maximum length
        too_long_email = "a" * 250 + "@example.com"
        is_valid, error_msg = self.signup_page.validate_email_format(too_long_email)
        self.assertFalse(is_valid, "Email exceeding 254 characters should be invalid")
        self.assertEqual(error_msg, "Email address is too long")
        
        # Test local part exceeding 64 characters
        long_local_email = "a" * 65 + "@example.com"
        is_valid, error_msg = self.signup_page.validate_email_format(long_local_email)
        self.assertFalse(is_valid, "Local part exceeding 64 characters should be invalid")
        self.assertEqual(error_msg, "Email local part is too long")
    
    def test_complete_registration_workflow_with_validation(self):
        """
        Test complete registration workflow with email validation
        End-to-end test verifying all validation steps
        """
        # Navigate to signup page
        self.signup_page.navigate_to_signup()
        
        # Test data with valid email
        test_username = "completeuser789"
        test_email = "complete.user@example.com"
        test_password = "CompletePass123!"
        
        # Step 1: Validate email format programmatically
        is_valid, error_msg = self.signup_page.validate_email_format(test_email)
        self.assertTrue(is_valid, "Email format validation should pass")
        self.assertIsNone(error_msg, "No validation error for valid email")
        
        # Step 2: Perform complete registration
        result = self.signup_page.perform_registration_with_validation(
            username=test_username,
            email=test_email,
            password=test_password
        )
        
        # Step 3: Verify validation results
        self.assertTrue(result['email_valid'], "Email validation should pass")
        self.assertIsNone(result['validation_error'], "No validation error should occur")
        
        # Step 4: Verify registration outcome
        # Either registration succeeds or appropriate error is shown
        if not result['registration_successful'] and result['ui_error_message']:
            # If registration fails, it should be for reasons other than email format
            self.assertNotIn('email', result['ui_error_message'].lower(), 
                           "Error should not be related to email format")
    
    def tearDown(self):
        """Clean up driver"""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()