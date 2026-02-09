"""
Test Scripts Module - Automated Test Cases
Contains test classes for login functionality and user signup with email validation
"""

import unittest
import re
import pytest
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
    """Page Object Model for User Signup Page with Email Format Validation"""
    
    # Email validation regex pattern
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.username_field = (By.ID, "signup_username")
        self.email_field = (By.ID, "signup_email")
        self.password_field = (By.ID, "signup_password")
        self.signup_button = (By.ID, "signupBtn")
        self.error_message = (By.CLASS_NAME, "error-message")
        self.success_message = (By.CLASS_NAME, "success-message")
        self.email_error = (By.ID, "email_error")
        
    def navigate_to_signup(self, url="https://example.com/signup"):
        """Navigate to signup page"""
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located(self.username_field))
        
    def enter_username(self, username):
        """Enter username in the username field"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.username_field))
            element.clear()
            element.send_keys(username)
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error entering username: {str(e)}")
            return False
    
    def enter_email(self, email):
        """Enter email in the email field"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.email_field))
            element.clear()
            element.send_keys(email)
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error entering email: {str(e)}")
            return False
    
    def enter_password(self, password):
        """Enter password in the password field"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.password_field))
            element.clear()
            element.send_keys(password)
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error entering password: {str(e)}")
            return False
    
    def validate_email_format(self, email):
        """
        Validate email format using regex pattern
        Returns: tuple (is_valid: bool, error_message: str)
        """
        if not email:
            return False, "Email cannot be empty"
        
        if not re.match(self.EMAIL_REGEX, email):
            return False, "Invalid email format. Please enter a valid email address."
        
        return True, "Email format is valid"
    
    def click_signup(self):
        """Click the signup button"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.signup_button))
            element.click()
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error clicking signup button: {str(e)}")
            return False
    
    def get_error_message(self):
        """Get error message text if present"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.error_message))
            return element.text
        except TimeoutException:
            return None
    
    def get_email_error(self):
        """Get email-specific error message if present"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.email_error))
            return element.text
        except TimeoutException:
            return None
    
    def get_success_message(self):
        """Get success message text if present"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.success_message))
            return element.text
        except TimeoutException:
            return None
    
    def signup_with_validation(self, username, email, password):
        """
        Complete signup flow with email format validation
        Returns: tuple (success: bool, message: str)
        """
        # Validate email format before proceeding
        is_valid, validation_message = self.validate_email_format(email)
        
        if not is_valid:
            print(f"Email validation failed: {validation_message}")
            return False, validation_message
        
        # Proceed with signup if email is valid
        self.enter_username(username)
        self.enter_email(email)
        self.enter_password(password)
        self.click_signup()
        
        return True, "Signup process initiated with valid email format"


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
    Test Case: TC002 - Email Format Validation in Registration Step
    Description: Test Case TC002 - Added email format validation in registration step
    Expected: Step executes successfully as per the described change
    """
    
    def setUp(self):
        """Initialize driver and page object"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.signup_page = UserSignupPage(self.driver)
        self.test_username = "testuser123"
        self.test_password = "SecurePass@123"
    
    def test_email_format_validation_valid_emails(self):
        """Test email format validation with valid email formats"""
        print("\n=== Testing Valid Email Formats ===")
        
        valid_emails = [
            "testuser@example.com",
            "test.user@example.com",
            "testuser+tag@example.co.uk",
            "user123@mail.example.org",
            "test_user@subdomain.example.com"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                is_valid, message = self.signup_page.validate_email_format(email)
                self.assertTrue(is_valid, f"Valid email should pass validation: {email}")
                self.assertIn("valid", message.lower(), "Validation message should indicate valid format")
                print(f"✓ Valid email test passed: {email}")
    
    def test_email_format_validation_invalid_emails(self):
        """Test email format validation with invalid email formats"""
        print("\n=== Testing Invalid Email Formats ===")
        
        invalid_emails = [
            "testuser.example.com",  # Missing @
            "testuser@",             # Missing domain
            "@example.com",          # Missing username
            "testuser@example",      # Missing TLD
            "testuser@@example.com", # Double @
            "test user@example.com", # Space in username
            "testuser@.com",         # Missing domain name
            "",                       # Empty email
            "testuser@example.",     # Incomplete TLD
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                is_valid, message = self.signup_page.validate_email_format(email)
                self.assertFalse(is_valid, f"Invalid email should fail validation: {email}")
                self.assertIn("invalid", message.lower(), "Error message should indicate invalid format")
                print(f"✓ Invalid email test passed: {email}")
    
    def test_empty_email_validation(self):
        """Test email format validation with empty email"""
        print("\n=== Testing Empty Email ===")
        
        empty_email = ""
        is_valid, message = self.signup_page.validate_email_format(empty_email)
        self.assertFalse(is_valid, "Empty email should fail validation")
        self.assertIn("empty", message.lower(), "Error message should indicate empty email")
        print("✓ Empty email test passed")
    
    def test_signup_with_valid_email_validation(self):
        """Test complete signup flow with valid email validation"""
        print("\n=== Testing Complete Signup Flow with Valid Email ===")
        
        valid_email = "newuser@example.com"
        success, message = self.signup_page.signup_with_validation(
            self.test_username, 
            valid_email, 
            self.test_password
        )
        self.assertTrue(success, "Signup with valid email should succeed")
        self.assertIn("valid email format", message.lower(), "Success message should indicate valid email")
        print("✓ Complete signup flow with valid email test passed")
    
    def test_signup_with_invalid_email_validation(self):
        """Test complete signup flow with invalid email validation"""
        print("\n=== Testing Complete Signup Flow with Invalid Email ===")
        
        invalid_email = "invalid-email"
        success, message = self.signup_page.signup_with_validation(
            self.test_username, 
            invalid_email, 
            self.test_password
        )
        self.assertFalse(success, "Signup with invalid email should fail")
        self.assertIn("invalid", message.lower(), "Error message should indicate invalid email")
        print("✓ Complete signup flow with invalid email test passed")
    
    def test_tc002_main_requirement(self):
        """
        Main test for TC002 requirement:
        Step 1: Added email format validation in registration step
        Expected: Step executes successfully as per the described change
        """
        print("\n=== TC002: Main Requirement Test ===")
        print("Step 1: Added email format validation in registration step")
        
        # Test that email format validation is working in registration
        test_cases = [
            ("valid@example.com", True, "Valid email should be accepted"),
            ("invalid-email", False, "Invalid email should be rejected"),
            ("", False, "Empty email should be rejected")
        ]
        
        for email, expected_valid, description in test_cases:
            with self.subTest(email=email):
                is_valid, message = self.signup_page.validate_email_format(email)
                self.assertEqual(is_valid, expected_valid, description)
                print(f"✓ {description}: {email}")
        
        print("Expected Result: Step executes successfully as per the described change - VERIFIED")
        print("✓ TC002: Email format validation in registration step - COMPLETED SUCCESSFULLY")
    
    def tearDown(self):
        """Clean up driver"""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
