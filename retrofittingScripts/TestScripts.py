"""
TestScripts.py - Comprehensive Test Suite for Authentication Workflows
Contains test classes for Password Recovery, Login, and User Registration functionality
"""

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class PasswordRecoveryTests(unittest.TestCase):
    """Test suite for password recovery functionality"""
    
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
    
    def test_password_recovery_workflow(self):
        """
        Test Case: Password Recovery Workflow
        Validates the complete password recovery process
        """
        try:
            # Navigate to login page
            self.driver.get(f"{self.base_url}/login")
            
            # Click forgot password link
            forgot_password_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "forgot-password-link"))
            )
            forgot_password_link.click()
            
            # Enter email for password recovery
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "recovery-email"))
            )
            email_input.send_keys("testuser@example.com")
            
            # Submit recovery request
            submit_button = self.driver.find_element(By.ID, "submit-recovery")
            submit_button.click()
            
            # Verify success message
            success_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
            )
            self.assertIn("recovery email has been sent", success_message.text.lower())
            
        except TimeoutException as e:
            self.fail(f"Timeout waiting for element: {str(e)}")
        except Exception as e:
            self.fail(f"Password recovery test failed: {str(e)}")


class LoginTests(unittest.TestCase):
    """Test suite for login functionality"""
    
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
    
    def test_TC002_valid_login(self):
        """
        Test Case TC002: Valid Login Test
        Test Case ID: TC002
        Description: Validates successful login with valid credentials
        Priority: High
        """
        try:
            # Step 1: Navigate to login page
            self.driver.get(f"{self.base_url}/login")
            
            # Step 2: Verify login page is loaded
            page_title = self.driver.title
            self.assertIn("Login", page_title, "Login page not loaded correctly")
            
            # Step 3: Enter valid username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.clear()
            username_field.send_keys("validuser@example.com")
            
            # Step 4: Enter valid password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys("ValidPassword123!")
            
            # Step 5: Click login button
            login_button = self.driver.find_element(By.ID, "login-button")
            login_button.click()
            
            # Step 6: Wait for dashboard to load
            WebDriverWait(self.driver, 15).until(
                EC.url_contains("/dashboard")
            )
            
            # Step 7: Verify successful login
            welcome_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "welcome-message"))
            )
            self.assertTrue(welcome_message.is_displayed(), "Welcome message not displayed")
            
            # Step 8: Verify user is on dashboard
            current_url = self.driver.current_url
            self.assertIn("/dashboard", current_url, "User not redirected to dashboard")
            
        except TimeoutException as e:
            self.fail(f"Timeout waiting for element in TC002: {str(e)}")
        except NoSuchElementException as e:
            self.fail(f"Element not found in TC002: {str(e)}")
        except Exception as e:
            self.fail(f"TC002 valid login test failed: {str(e)}")
    
    def test_TC003_invalid_login(self):
        """
        Test Case TC003: Invalid Login Test
        Test Case ID: TC003
        Description: Validates error handling for invalid credentials
        Priority: High
        """
        try:
            # Step 1: Navigate to login page
            self.driver.get(f"{self.base_url}/login")
            
            # Step 2: Verify login page is loaded
            page_title = self.driver.title
            self.assertIn("Login", page_title, "Login page not loaded correctly")
            
            # Step 3: Enter invalid username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.clear()
            username_field.send_keys("invaliduser@example.com")
            
            # Step 4: Enter invalid password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys("WrongPassword123!")
            
            # Step 5: Click login button
            login_button = self.driver.find_element(By.ID, "login-button")
            login_button.click()
            
            # Step 6: Wait for error message
            error_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
            )
            
            # Step 7: Verify error message is displayed
            self.assertTrue(error_message.is_displayed(), "Error message not displayed")
            
            # Step 8: Verify error message content
            error_text = error_message.text.lower()
            self.assertTrue(
                "invalid" in error_text or "incorrect" in error_text,
                "Error message does not indicate invalid credentials"
            )
            
            # Step 9: Verify user remains on login page
            current_url = self.driver.current_url
            self.assertIn("/login", current_url, "User incorrectly redirected from login page")
            
        except TimeoutException as e:
            self.fail(f"Timeout waiting for element in TC003: {str(e)}")
        except NoSuchElementException as e:
            self.fail(f"Element not found in TC003: {str(e)}")
        except Exception as e:
            self.fail(f"TC003 invalid login test failed: {str(e)}")
    
    def test_TC101_basic_login_test(self):
        """
        Test Case TC-101: Basic Login Functionality Test
        Test Case ID: 1298
        Description: Test Case TC-101 - Comprehensive validation of basic login functionality
        Priority: High
        
        This test validates the complete basic login workflow including:
        - Page navigation and loading
        - Form field presence and interaction
        - Input validation
        - Authentication process
        - Successful login verification
        - Post-login state validation
        """
        try:
            # Step 1: Navigate to the login page
            self.driver.get(f"{self.base_url}/login")
            time.sleep(1)  # Allow page to stabilize
            
            # Step 2: Verify login page loaded successfully
            page_title = self.driver.title
            self.assertIsNotNone(page_title, "Page title is None")
            self.assertIn("Login", page_title, f"Expected 'Login' in page title, got: {page_title}")
            
            # Step 3: Verify all required form elements are present
            try:
                username_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                self.assertTrue(username_field.is_displayed(), "Username field is not visible")
                
                password_field = self.driver.find_element(By.ID, "password")
                self.assertTrue(password_field.is_displayed(), "Password field is not visible")
                
                login_button = self.driver.find_element(By.ID, "login-button")
                self.assertTrue(login_button.is_displayed(), "Login button is not visible")
                self.assertTrue(login_button.is_enabled(), "Login button is not enabled")
                
            except NoSuchElementException as e:
                self.fail(f"Required form element not found: {str(e)}")
            
            # Step 4: Verify form fields are empty/ready for input
            username_value = username_field.get_attribute("value")
            password_value = password_field.get_attribute("value")
            self.assertEqual(username_value, "", "Username field should be empty initially")
            self.assertEqual(password_value, "", "Password field should be empty initially")
            
            # Step 5: Enter valid username with validation
            test_username = "testuser@example.com"
            username_field.clear()
            username_field.send_keys(test_username)
            
            # Verify username was entered correctly
            entered_username = username_field.get_attribute("value")
            self.assertEqual(entered_username, test_username, 
                           f"Username not entered correctly. Expected: {test_username}, Got: {entered_username}")
            
            # Step 6: Enter valid password with validation
            test_password = "SecurePassword123!"
            password_field.clear()
            password_field.send_keys(test_password)
            
            # Verify password field has content (value will be masked)
            entered_password = password_field.get_attribute("value")
            self.assertIsNotNone(entered_password, "Password field is empty after input")
            self.assertTrue(len(entered_password) > 0, "Password was not entered")
            
            # Step 7: Verify login button is still enabled and clickable
            self.assertTrue(login_button.is_enabled(), "Login button became disabled")
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "login-button"))
            )
            
            # Step 8: Click the login button
            login_button.click()
            
            # Step 9: Wait for authentication to complete and redirection
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.url_changes(f"{self.base_url}/login")
                )
            except TimeoutException:
                self.fail("Page did not redirect after login attempt")
            
            # Step 10: Verify successful redirection to dashboard/home page
            current_url = self.driver.current_url
            self.assertNotIn("/login", current_url, 
                           f"User still on login page after successful login: {current_url}")
            self.assertTrue(
                "/dashboard" in current_url or "/home" in current_url,
                f"User not redirected to expected page. Current URL: {current_url}"
            )
            
            # Step 11: Verify user authentication state
            try:
                # Check for welcome message or user profile indicator
                user_indicator = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "user-profile"))
                )
                self.assertTrue(user_indicator.is_displayed(), 
                              "User profile indicator not displayed after login")
            except TimeoutException:
                # Alternative: Check for welcome message
                try:
                    welcome_message = self.driver.find_element(By.CLASS_NAME, "welcome-message")
                    self.assertTrue(welcome_message.is_displayed(), 
                                  "Welcome message not displayed after login")
                except NoSuchElementException:
                    self.fail("No user authentication indicator found after login")
            
            # Step 12: Verify no error messages are present
            try:
                error_elements = self.driver.find_elements(By.CLASS_NAME, "error-message")
                visible_errors = [e for e in error_elements if e.is_displayed()]
                self.assertEqual(len(visible_errors), 0, 
                               f"Error messages present after successful login: {[e.text for e in visible_errors]}")
            except NoSuchElementException:
                pass  # No error messages found, which is expected
            
            # Step 13: Verify page title changed from login page
            post_login_title = self.driver.title
            self.assertNotEqual(post_login_title, page_title, 
                              "Page title did not change after login")
            self.assertNotIn("Login", post_login_title, 
                           f"Page title still contains 'Login': {post_login_title}")
            
            # Step 14: Verify session is established (check for logout option)
            try:
                logout_button = self.driver.find_element(By.ID, "logout-button")
                self.assertTrue(logout_button.is_displayed(), 
                              "Logout button not available, session may not be established")
            except NoSuchElementException:
                # Try alternative logout element
                try:
                    logout_link = self.driver.find_element(By.LINK_TEXT, "Logout")
                    self.assertTrue(logout_link.is_displayed(), 
                                  "Logout link not available, session may not be established")
                except NoSuchElementException:
                    self.fail("No logout option found, cannot verify session establishment")
            
            # Step 15: Final validation - verify user can interact with authenticated page
            try:
                # Check that page has loaded interactive elements
                interactive_elements = self.driver.find_elements(By.TAG_NAME, "button")
                self.assertGreater(len(interactive_elements), 0, 
                                 "No interactive elements found on authenticated page")
            except Exception as e:
                self.fail(f"Could not verify interactive elements on authenticated page: {str(e)}")
            
            # Test completed successfully
            print("TC-101: Basic login test completed successfully")
            
        except TimeoutException as e:
            self.fail(f"Timeout occurred during TC-101 basic login test: {str(e)}")
        except NoSuchElementException as e:
            self.fail(f"Required element not found during TC-101: {str(e)}")
        except AssertionError as e:
            self.fail(f"Assertion failed in TC-101: {str(e)}")
        except Exception as e:
            self.fail(f"TC-101 basic login test failed with unexpected error: {str(e)}")
    
    def test_forgot_username_workflow(self):
        """
        Test Case: Forgot Username Workflow
        Validates the username recovery process
        """
        try:
            # Navigate to login page
            self.driver.get(f"{self.base_url}/login")
            
            # Click forgot username link
            forgot_username_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "forgot-username-link"))
            )
            forgot_username_link.click()
            
            # Enter email for username recovery
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "recovery-email"))
            )
            email_input.send_keys("testuser@example.com")
            
            # Submit recovery request
            submit_button = self.driver.find_element(By.ID, "submit-username-recovery")
            submit_button.click()
            
            # Verify success message
            success_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
            )
            self.assertIn("username has been sent", success_message.text.lower())
            
        except TimeoutException as e:
            self.fail(f"Timeout waiting for element: {str(e)}")
        except Exception as e:
            self.fail(f"Forgot username test failed: {str(e)}")


class UserRegistrationTests(unittest.TestCase):
    """Test suite for user registration functionality"""
    
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
    
    def test_new_user_registration(self):
        """
        Test Case: New User Registration
        Validates the complete user registration process
        """
        try:
            # Navigate to registration page
            self.driver.get(f"{self.base_url}/register")
            
            # Fill in registration form
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "reg-username"))
            )
            username_field.send_keys("newuser@example.com")
            
            password_field = self.driver.find_element(By.ID, "reg-password")
            password_field.send_keys("NewPassword123!")
            
            confirm_password_field = self.driver.find_element(By.ID, "confirm-password")
            confirm_password_field.send_keys("NewPassword123!")
            
            # Submit registration
            register_button = self.driver.find_element(By.ID, "register-button")
            register_button.click()
            
            # Verify successful registration
            success_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "registration-success"))
            )
            self.assertIn("successfully registered", success_message.text.lower())
            
        except TimeoutException as e:
            self.fail(f"Timeout waiting for element: {str(e)}")
        except Exception as e:
            self.fail(f"User registration test failed: {str(e)}")
    
    def test_duplicate_user_registration(self):
        """
        Test Case: Duplicate User Registration
        Validates error handling for duplicate username registration
        """
        try:
            # Navigate to registration page
            self.driver.get(f"{self.base_url}/register")
            
            # Fill in registration form with existing username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "reg-username"))
            )
            username_field.send_keys("existinguser@example.com")
            
            password_field = self.driver.find_element(By.ID, "reg-password")
            password_field.send_keys("Password123!")
            
            confirm_password_field = self.driver.find_element(By.ID, "confirm-password")
            confirm_password_field.send_keys("Password123!")
            
            # Submit registration
            register_button = self.driver.find_element(By.ID, "register-button")
            register_button.click()
            
            # Verify error message for duplicate user
            error_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
            )
            error_text = error_message.text.lower()
            self.assertTrue(
                "already exists" in error_text or "already registered" in error_text,
                "Error message does not indicate duplicate user"
            )
            
        except TimeoutException as e:
            self.fail(f"Timeout waiting for element: {str(e)}")
        except Exception as e:
            self.fail(f"Duplicate user registration test failed: {str(e)}")


if __name__ == "__main__":
    # Run all test suites
    unittest.main(verbosity=2)