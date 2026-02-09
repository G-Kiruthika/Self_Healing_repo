"""
TestScripts.py

Comprehensive test suite containing automated test cases for:
- Password Recovery functionality
- User Login functionality  
- User Registration functionality
- TC-101: Additional test case (ID: 1298)

This module uses unittest framework and includes all test classes
with their respective test methods organized by functionality.
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class PasswordRecoveryTests(unittest.TestCase):
    """Test cases for Password Recovery functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.base_url = "https://example.com"
    
    def tearDown(self):
        """Clean up after each test method"""
        if self.driver:
            self.driver.quit()
    
    def test_password_recovery_valid_email(self):
        """Test password recovery with valid email address"""
        self.driver.get(f"{self.base_url}/password-recovery")
        
        email_field = self.driver.find_element(By.ID, "email")
        email_field.send_keys("valid@example.com")
        
        submit_button = self.driver.find_element(By.ID, "submit")
        submit_button.click()
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        
        self.assertIn("recovery email sent", success_message.text.lower())
    
    def test_password_recovery_invalid_email(self):
        """Test password recovery with invalid email address"""
        self.driver.get(f"{self.base_url}/password-recovery")
        
        email_field = self.driver.find_element(By.ID, "email")
        email_field.send_keys("invalid-email")
        
        submit_button = self.driver.find_element(By.ID, "submit")
        submit_button.click()
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
        )
        
        self.assertIn("invalid email", error_message.text.lower())


class LoginTests(unittest.TestCase):
    """Test cases for User Login functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.base_url = "https://example.com"
    
    def tearDown(self):
        """Clean up after each test method"""
        if self.driver:
            self.driver.quit()
    
    def test_login_valid_credentials(self):
        """Test login with valid username and password"""
        self.driver.get(f"{self.base_url}/login")
        
        username_field = self.driver.find_element(By.ID, "username")
        username_field.send_keys("testuser")
        
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("Test@123")
        
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard")
        )
        
        self.assertIn("dashboard", self.driver.current_url)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        self.driver.get(f"{self.base_url}/login")
        
        username_field = self.driver.find_element(By.ID, "username")
        username_field.send_keys("invaliduser")
        
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("WrongPass")
        
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
        )
        
        self.assertIn("invalid", error_message.text.lower())
    
    def test_login_empty_fields(self):
        """Test login with empty username and password fields"""
        self.driver.get(f"{self.base_url}/login")
        
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
        )
        
        self.assertTrue(error_message.is_displayed())


class UserRegistrationTests(unittest.TestCase):
    """Test cases for User Registration functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.base_url = "https://example.com"
    
    def tearDown(self):
        """Clean up after each test method"""
        if self.driver:
            self.driver.quit()
    
    def test_registration_valid_data(self):
        """Test user registration with valid data"""
        self.driver.get(f"{self.base_url}/register")
        
        username_field = self.driver.find_element(By.ID, "username")
        username_field.send_keys("newuser123")
        
        email_field = self.driver.find_element(By.ID, "email")
        email_field.send_keys("newuser@example.com")
        
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("SecurePass@123")
        
        confirm_password_field = self.driver.find_element(By.ID, "confirm-password")
        confirm_password_field.send_keys("SecurePass@123")
        
        register_button = self.driver.find_element(By.ID, "register-button")
        register_button.click()
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        
        self.assertIn("registration successful", success_message.text.lower())
    
    def test_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        self.driver.get(f"{self.base_url}/register")
        
        username_field = self.driver.find_element(By.ID, "username")
        username_field.send_keys("newuser123")
        
        email_field = self.driver.find_element(By.ID, "email")
        email_field.send_keys("newuser@example.com")
        
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("SecurePass@123")
        
        confirm_password_field = self.driver.find_element(By.ID, "confirm-password")
        confirm_password_field.send_keys("DifferentPass@123")
        
        register_button = self.driver.find_element(By.ID, "register-button")
        register_button.click()
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
        )
        
        self.assertIn("password", error_message.text.lower())
    
    def test_registration_existing_user(self):
        """Test registration with already existing username"""
        self.driver.get(f"{self.base_url}/register")
        
        username_field = self.driver.find_element(By.ID, "username")
        username_field.send_keys("existinguser")
        
        email_field = self.driver.find_element(By.ID, "email")
        email_field.send_keys("existing@example.com")
        
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("SecurePass@123")
        
        confirm_password_field = self.driver.find_element(By.ID, "confirm-password")
        confirm_password_field.send_keys("SecurePass@123")
        
        register_button = self.driver.find_element(By.ID, "register-button")
        register_button.click()
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
        )
        
        self.assertIn("already exists", error_message.text.lower())


class TC101Tests(unittest.TestCase):
    """
    Test Case TC-101 (ID: 1298)
    
    Automated test case for TC-101 functionality.
    This test class contains test methods specific to test case ID 1298.
    """
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.base_url = "https://example.com"
    
    def tearDown(self):
        """Clean up after each test method"""
        if self.driver:
            self.driver.quit()
    
    def test_tc101_main_functionality(self):
        """
        Test Case TC-101: Main functionality test
        Test ID: 1298
        
        This test validates the main functionality of TC-101.
        """
        try:
            # Navigate to the application
            self.driver.get(f"{self.base_url}/tc101")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "main-content"))
            )
            
            # Perform test actions specific to TC-101
            main_element = self.driver.find_element(By.ID, "tc101-element")
            self.assertTrue(main_element.is_displayed(), "TC-101 main element should be visible")
            
            # Interact with the element
            action_button = self.driver.find_element(By.ID, "tc101-action-button")
            action_button.click()
            
            # Verify expected result
            result_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "tc101-result"))
            )
            
            self.assertIsNotNone(result_element, "TC-101 result should be present")
            self.assertIn("success", result_element.text.lower(), "TC-101 should complete successfully")
            
        except TimeoutException as e:
            self.fail(f"TC-101 test failed due to timeout: {str(e)}")
        except NoSuchElementException as e:
            self.fail(f"TC-101 test failed - element not found: {str(e)}")
    
    def test_tc101_validation(self):
        """
        Test Case TC-101: Validation test
        Test ID: 1298
        
        This test validates the validation logic of TC-101.
        """
        self.driver.get(f"{self.base_url}/tc101")
        
        # Test validation scenarios
        input_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "tc101-input"))
        )
        
        # Test with valid input
        input_field.clear()
        input_field.send_keys("valid_input")
        
        validate_button = self.driver.find_element(By.ID, "tc101-validate")
        validate_button.click()
        
        validation_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "validation-message"))
        )
        
        self.assertIn("valid", validation_message.text.lower(), "Validation should pass for valid input")
    
    def test_tc101_error_handling(self):
        """
        Test Case TC-101: Error handling test
        Test ID: 1298
        
        This test validates error handling in TC-101.
        """
        self.driver.get(f"{self.base_url}/tc101")
        
        # Trigger error condition
        error_trigger = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "tc101-error-trigger"))
        )
        error_trigger.click()
        
        # Verify error is handled gracefully
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
        )
        
        self.assertTrue(error_message.is_displayed(), "Error message should be displayed")
        self.assertIsNotNone(error_message.text, "Error message should have content")


def suite():
    """
    Create and return a test suite containing all test cases.
    
    Returns:
        unittest.TestSuite: Complete test suite with all test classes
    """
    test_suite = unittest.TestSuite()
    
    # Add PasswordRecoveryTests
    test_suite.addTest(unittest.makeSuite(PasswordRecoveryTests))
    
    # Add LoginTests
    test_suite.addTest(unittest.makeSuite(LoginTests))
    
    # Add UserRegistrationTests
    test_suite.addTest(unittest.makeSuite(UserRegistrationTests))
    
    # Add TC101Tests
    test_suite.addTest(unittest.makeSuite(TC101Tests))
    
    return test_suite


if __name__ == '__main__':
    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
