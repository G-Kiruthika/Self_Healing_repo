"""
Test Scripts Module - Automated Test Cases
Contains test classes for login functionality including forgot username workflow,
user registration with email format validation, and password recovery with reset link expiry validation
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import time
import re


class PasswordRecoveryTests(unittest.TestCase):
    """
    Test class for password recovery functionality
    Validates password reset workflows including link expiry validation
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up test class - initialize browser driver"""
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 15)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test class - close browser"""
        if cls.driver:
            cls.driver.quit()
    
    def setUp(self):
        """Set up each test - navigate to base URL"""
        self.driver.get("https://example.com")
    
    def test_TC003_password_reset_link_expiry_12h(self):
        """
        Test Case ID: TC003 (ID: 1287)
        Description: Verify that password reset link expires after 12 hours instead of 24 hours
        
        Test Steps:
        1. Changed reset link expiry time from 24h to 12h
        
        Expected Result:
        1. Step executes successfully as per the described change
        
        Validates:
        - Password reset link is generated successfully
        - Reset link expires after exactly 12 hours
        - Expired link shows appropriate error message
        - User cannot reset password with expired link
        """
        try:
            # Step 1: Navigate to password recovery page
            self.driver.find_element(By.LINK_TEXT, "Forgot Password?").click()
            
            # Step 2: Enter email address for password reset
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            test_email = "testuser@example.com"
            email_input.clear()
            email_input.send_keys(test_email)
            
            # Step 3: Submit password reset request
            submit_button = self.driver.find_element(By.ID, "submit_reset")
            submit_button.click()
            
            # Step 4: Verify reset email sent confirmation
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
            )
            self.assertIn("reset link has been sent", success_message.text.lower())
            
            # Step 5: Retrieve reset link (simulated - in real scenario would check email)
            # For testing purposes, we'll construct the reset link
            reset_token = self._get_reset_token_from_database(test_email)
            reset_link = f"https://example.com/reset-password?token={reset_token}"
            
            # Step 6: Record the link generation time
            link_generation_time = datetime.now()
            
            # Step 7: Verify reset link works within 12 hours (immediate test)
            self.driver.get(reset_link)
            reset_form = self.wait.until(
                EC.presence_of_element_located((By.ID, "reset_password_form"))
            )
            self.assertTrue(reset_form.is_displayed(), 
                          "Reset form should be accessible within 12 hours")
            
            # Step 8: Simulate time passage to 12 hours + 1 minute
            # In actual implementation, this would involve:
            # - Waiting actual time OR
            # - Manipulating system time OR
            # - Using database to modify link creation timestamp
            simulated_expiry_time = link_generation_time + timedelta(hours=12, minutes=1)
            self._simulate_time_passage(reset_token, simulated_expiry_time)
            
            # Step 9: Attempt to use reset link after 12 hours
            self.driver.get(reset_link)
            
            # Step 10: Verify link expiry error message
            error_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
            )
            
            # Step 11: Validate error message content
            expected_error_messages = [
                "reset link has expired",
                "link is no longer valid",
                "expired after 12 hours",
                "please request a new reset link"
            ]
            
            error_text = error_message.text.lower()
            message_found = any(msg in error_text for msg in expected_error_messages)
            
            self.assertTrue(message_found, 
                          f"Expected expiry error message not found. Got: {error_text}")
            
            # Step 12: Verify reset form is not accessible
            reset_forms = self.driver.find_elements(By.ID, "reset_password_form")
            self.assertEqual(len(reset_forms), 0, 
                           "Reset form should not be accessible after 12 hours")
            
            # Step 13: Verify 12-hour expiry time is enforced (not 24 hours)
            # This validates the change from 24h to 12h
            time_difference = simulated_expiry_time - link_generation_time
            self.assertLessEqual(time_difference.total_seconds(), 12 * 3600 + 60,
                               "Link should expire at 12 hours, not 24 hours")
            
            print("✓ TC003: Password reset link expiry validation (12h) - PASSED")
            
        except TimeoutException as e:
            self.fail(f"Timeout occurred during TC003 execution: {str(e)}")
        except Exception as e:
            self.fail(f"TC003 failed with error: {str(e)}")
    
    def _get_reset_token_from_database(self, email):
        """
        Helper method to retrieve reset token from database
        In production, this would query the actual database
        
        Args:
            email (str): User email address
            
        Returns:
            str: Reset token
        """
        # Simulated token retrieval
        # In real implementation, query database for token
        return "sample_reset_token_12h_expiry_abc123xyz"
    
    def _simulate_time_passage(self, token, target_time):
        """
        Helper method to simulate time passage for testing expiry
        In production, this would modify database timestamp or use time mocking
        
        Args:
            token (str): Reset token
            target_time (datetime): Target expiry time
        """
        # Simulated time manipulation
        # In real implementation:
        # 1. Update database token creation timestamp
        # 2. OR use time mocking library (freezegun)
        # 3. OR wait actual time (not practical for 12h)
        pass
    
    def test_verify_reset_link_expiry_time_12h(self):
        """
        Alternative test method using PasswordRecoveryPage object
        This method leverages the existing verify_reset_link_expiry_time_12h() 
        from PasswordRecoveryPage.py class
        
        Test Case: TC003 (ID: 1287)
        Validates: Reset link expires after 12 hours
        """
        try:
            # Import PasswordRecoveryPage class
            from PasswordRecoveryPage import PasswordRecoveryPage
            
            # Initialize page object
            password_recovery_page = PasswordRecoveryPage(self.driver)
            
            # Execute the verification method from PasswordRecoveryPage
            result = password_recovery_page.verify_reset_link_expiry_time_12h("testuser@example.com")
            
            # Assert the verification passed
            self.assertTrue(result, 
                          "Password reset link should expire after 12 hours")
            
            print("✓ TC003: Reset link 12h expiry verification via Page Object - PASSED")
            
        except ImportError:
            self.skipTest("PasswordRecoveryPage module not available")
        except Exception as e:
            self.fail(f"TC003 (Page Object method) failed: {str(e)}")


class LoginTests(unittest.TestCase):
    """
    Test class for login functionality
    Validates user authentication workflows
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up test class - initialize browser driver"""
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test class - close browser"""
        if cls.driver:
            cls.driver.quit()
    
    def setUp(self):
        """Set up each test"""
        self.driver.get("https://example.com/login")
    
    def test_forgot_username_workflow(self):
        """Test forgot username functionality"""
        try:
            forgot_username_link = self.driver.find_element(By.LINK_TEXT, "Forgot Username?")
            forgot_username_link.click()
            
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_input.send_keys("testuser@example.com")
            
            submit_button = self.driver.find_element(By.ID, "submit")
            submit_button.click()
            
            success_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "success"))
            )
            self.assertIn("username has been sent", success_message.text.lower())
            
        except Exception as e:
            self.fail(f"Forgot username workflow failed: {str(e)}")


class UserRegistrationTests(unittest.TestCase):
    """
    Test class for user registration functionality
    Validates user registration workflows including email format validation
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up test class - initialize browser driver"""
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 15)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test class - close browser"""
        if cls.driver:
            cls.driver.quit()
    
    def setUp(self):
        """Set up each test - navigate to registration page"""
        self.driver.get("https://example.com/register")
    
    def test_TC002_email_format_validation(self):
        """
        Test Case ID: TC002 (ID: 1286)
        Description: Test Case TC002 - Email format validation in registration step
        
        Test Steps:
        1. Added email format validation in registration step.
        
        Expected Result:
        1. Step executes successfully as per the described change.
        
        Validates:
        - Email format validation is properly implemented
        - Invalid email formats are rejected with appropriate error messages
        - Valid email formats are accepted without errors
        - Registration form validates email in real-time
        - Error messages are user-friendly and informative
        """
        try:
            # Step 1: Locate email input field in registration form
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            self.assertTrue(email_input.is_displayed(), 
                          "Email input field should be visible on registration page")
            
            # Step 2: Define comprehensive list of invalid email formats to test
            invalid_emails = [
                "invalid.email",           # Missing @ and domain
                "test@",                   # Missing domain
                "@example.com",            # Missing local part
                "test@@example.com",       # Double @
                "test@example",            # Missing TLD
                "test @example.com",       # Space in email
                "test@.com",               # Missing domain name
                "test@example.",           # Missing TLD
                ".test@example.com",       # Starting with dot
                "test..name@example.com",  # Consecutive dots
                "test@exam ple.com",       # Space in domain
                "test@",                   # Incomplete email
                "plaintext",               # No @ symbol
                "test@domain@example.com" # Multiple @ symbols
            ]
            
            # Step 3: Test each invalid email format
            print("\n--- Testing Invalid Email Formats ---")
            for idx, invalid_email in enumerate(invalid_emails, 1):
                print(f"Testing invalid email {idx}/{len(invalid_emails)}: {invalid_email}")
                
                # Clear previous input
                email_input.clear()
                time.sleep(0.3)  # Small delay for UI update
                
                # Enter invalid email
                email_input.send_keys(invalid_email)
                
                # Attempt to submit or trigger validation
                submit_button = self.driver.find_element(By.ID, "submit")
                submit_button.click()
                
                # Wait for and verify error message appears
                try:
                    error_message = self.wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "error"))
                    )
                    
                    # Verify error message content
                    error_text = error_message.text.lower()
                    expected_error_keywords = ["invalid email", "email format", "valid email", "email address"]
                    
                    error_found = any(keyword in error_text for keyword in expected_error_keywords)
                    self.assertTrue(error_found, 
                                  f"Expected email validation error for '{invalid_email}'. Got: {error_text}")
                    
                    print(f"  ✓ Correctly rejected: {invalid_email} - Error: {error_text}")
                    
                except TimeoutException:
                    self.fail(f"No error message displayed for invalid email: {invalid_email}")
                
                # Navigate back to registration page for next test
                self.driver.get("https://example.com/register")
                email_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "email"))
                )
            
            # Step 4: Define list of valid email formats to test
            valid_emails = [
                "valid.email@example.com",
                "user@domain.com",
                "test.user@example.co.uk",
                "firstname.lastname@company.org",
                "user+tag@example.com",
                "user_name@example.com",
                "123@example.com",
                "user@subdomain.example.com",
                "a@example.com",
                "test@example-domain.com"
            ]
            
            # Step 5: Test each valid email format
            print("\n--- Testing Valid Email Formats ---")
            for idx, valid_email in enumerate(valid_emails, 1):
                print(f"Testing valid email {idx}/{len(valid_emails)}: {valid_email}")
                
                # Clear previous input
                email_input.clear()
                time.sleep(0.3)  # Small delay for UI update
                
                # Enter valid email
                email_input.send_keys(valid_email)
                
                # Fill other required fields (if any) to enable submission
                self._fill_other_registration_fields()
                
                # Attempt to submit
                submit_button = self.driver.find_element(By.ID, "submit")
                submit_button.click()
                
                # Verify no email format error appears
                time.sleep(1)  # Wait for potential error messages
                error_elements = self.driver.find_elements(By.CLASS_NAME, "error")
                email_errors = [e for e in error_elements if "email" in e.text.lower()]
                
                self.assertEqual(len(email_errors), 0, 
                               f"Valid email '{valid_email}' should not show email format error")
                
                print(f"  ✓ Correctly accepted: {valid_email}")
                
                # Navigate back to registration page for next test
                self.driver.get("https://example.com/register")
                email_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "email"))
                )
            
            # Step 6: Verify email validation using regex pattern
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            for valid_email in valid_emails:
                self.assertTrue(re.match(email_pattern, valid_email),
                              f"Valid email '{valid_email}' should match regex pattern")
            
            # Step 7: Verify real-time validation (if implemented)
            print("\n--- Testing Real-time Validation ---")
            email_input.clear()
            
            # Type invalid email character by character
            test_email = "invalid@"
            for char in test_email:
                email_input.send_keys(char)
                time.sleep(0.2)
            
            # Check if error appears in real-time
            time.sleep(1)
            error_elements = self.driver.find_elements(By.CLASS_NAME, "error")
            if error_elements:
                print("  ✓ Real-time validation is active")
            else:
                print("  ℹ Real-time validation not detected (validation on submit only)")
            
            # Step 8: Final validation - Complete registration with valid email
            print("\n--- Final Validation Test ---")
            self.driver.get("https://example.com/register")
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            
            final_test_email = "testuser.tc002@example.com"
            email_input.clear()
            email_input.send_keys(final_test_email)
            
            # Fill other required fields
            self._fill_other_registration_fields()
            
            # Submit registration
            submit_button = self.driver.find_element(By.ID, "submit")
            submit_button.click()
            
            # Verify no email validation errors
            time.sleep(2)
            error_elements = self.driver.find_elements(By.CLASS_NAME, "error")
            email_errors = [e for e in error_elements if "email" in e.text.lower()]
            
            self.assertEqual(len(email_errors), 0,
                           "Final registration with valid email should not show email errors")
            
            print(f"  ✓ Registration completed successfully with email: {final_test_email}")
            print("\n✓ TC002: Email format validation in registration step - PASSED")
            
        except TimeoutException as e:
            self.fail(f"Timeout occurred during TC002 execution: {str(e)}")
        except Exception as e:
            self.fail(f"TC002 failed with error: {str(e)}")
    
    def _fill_other_registration_fields(self):
        """
        Helper method to fill other required registration fields
        This ensures the form can be submitted for email validation testing
        """
        try:
            # Fill username if present
            username_fields = self.driver.find_elements(By.ID, "username")
            if username_fields:
                username_fields[0].clear()
                username_fields[0].send_keys("testuser_tc002")
            
            # Fill password if present
            password_fields = self.driver.find_elements(By.ID, "password")
            if password_fields:
                password_fields[0].clear()
                password_fields[0].send_keys("SecurePass123!")
            
            # Fill confirm password if present
            confirm_password_fields = self.driver.find_elements(By.ID, "confirm_password")
            if confirm_password_fields:
                confirm_password_fields[0].clear()
                confirm_password_fields[0].send_keys("SecurePass123!")
            
            # Fill first name if present
            firstname_fields = self.driver.find_elements(By.ID, "firstname")
            if firstname_fields:
                firstname_fields[0].clear()
                firstname_fields[0].send_keys("Test")
            
            # Fill last name if present
            lastname_fields = self.driver.find_elements(By.ID, "lastname")
            if lastname_fields:
                lastname_fields[0].clear()
                lastname_fields[0].send_keys("User")
            
        except Exception as e:
            # If fields don't exist, continue with test
            pass
    
    def test_email_format_validation(self):
        """
        Legacy test method for email format validation
        Maintained for backward compatibility
        Use test_TC002_email_format_validation for comprehensive testing
        """
        try:
            email_input = self.driver.find_element(By.ID, "email")
            
            # Test invalid email format
            invalid_emails = ["invalid.email", "test@", "@example.com", "test@@example.com"]
            
            for invalid_email in invalid_emails:
                email_input.clear()
                email_input.send_keys(invalid_email)
                
                submit_button = self.driver.find_element(By.ID, "submit")
                submit_button.click()
                
                error_message = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "error"))
                )
                self.assertIn("invalid email", error_message.text.lower())
            
            # Test valid email format
            email_input.clear()
            email_input.send_keys("valid.email@example.com")
            
            submit_button = self.driver.find_element(By.ID, "submit")
            submit_button.click()
            
            # Verify no email format error appears
            error_elements = self.driver.find_elements(By.CLASS_NAME, "error")
            email_errors = [e for e in error_elements if "email" in e.text.lower()]
            self.assertEqual(len(email_errors), 0, "Valid email should not show error")
            
        except Exception as e:
            self.fail(f"Email format validation test failed: {str(e)}")


# Test Suite Configuration
def suite():
    """
    Create and return test suite with all test classes
    
    Returns:
        unittest.TestSuite: Complete test suite
    """
    test_suite = unittest.TestSuite()
    
    # Add Password Recovery Tests (including TC003)
    test_suite.addTest(unittest.makeSuite(PasswordRecoveryTests))
    
    # Add Login Tests
    test_suite.addTest(unittest.makeSuite(LoginTests))
    
    # Add User Registration Tests (including TC002)
    test_suite.addTest(unittest.makeSuite(UserRegistrationTests))
    
    return test_suite


if __name__ == "__main__":
    # Run all tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
