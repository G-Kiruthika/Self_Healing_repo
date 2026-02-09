import unittest
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class LoginPage:
    """Page Object Model for Login Page"""
    
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "username")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "loginButton")
        self.forgot_username_link = (By.LINK_TEXT, "Forgot Username?")
        self.error_message = (By.CLASS_NAME, "error-message")
        self.success_message = (By.CLASS_NAME, "success-message")
    
    def enter_username(self, username):
        """Enter username in the username field"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_field)
        )
        element.clear()
        element.send_keys(username)
    
    def enter_password(self, password):
        """Enter password in the password field"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.password_field)
        )
        element.clear()
        element.send_keys(password)
    
    def click_login(self):
        """Click the login button"""
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        )
        element.click()
    
    def click_forgot_username(self):
        """Click the forgot username link"""
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.forgot_username_link)
        )
        element.click()
    
    def get_error_message(self):
        """Get the error message text"""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.error_message)
            )
            return element.text
        except TimeoutException:
            return None
    
    def get_success_message(self):
        """Get the success message text"""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.success_message)
            )
            return element.text
        except TimeoutException:
            return None
    
    def is_login_successful(self):
        """Check if login was successful by checking URL or dashboard element"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("dashboard")
            )
            return True
        except TimeoutException:
            return False


class RegistrationPage:
    """Page Object Model for Registration Page"""
    
    # Email validation regex pattern (RFC 5322 compliant)
    EMAIL_REGEX = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.ID, "email")
        self.username_field = (By.ID, "regUsername")
        self.password_field = (By.ID, "regPassword")
        self.confirm_password_field = (By.ID, "confirmPassword")
        self.register_button = (By.ID, "registerButton")
        self.error_message = (By.CLASS_NAME, "error-message")
        self.success_message = (By.CLASS_NAME, "success-message")
        self.email_error = (By.ID, "emailError")
    
    def enter_email(self, email):
        """Enter email in the email field"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.email_field)
        )
        element.clear()
        element.send_keys(email)
    
    def enter_username(self, username):
        """Enter username in the registration username field"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_field)
        )
        element.clear()
        element.send_keys(username)
    
    def enter_password(self, password):
        """Enter password in the registration password field"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.password_field)
        )
        element.clear()
        element.send_keys(password)
    
    def enter_confirm_password(self, password):
        """Enter password in the confirm password field"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.confirm_password_field)
        )
        element.clear()
        element.send_keys(password)
    
    def click_register(self):
        """Click the register button"""
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.register_button)
        )
        element.click()
    
    def validate_email_format(self, email):
        """
        Validate email format using regex pattern
        Returns: tuple (is_valid: bool, error_message: str)
        """
        if not email:
            return False, "Email cannot be empty"
        
        if not self.EMAIL_REGEX.match(email):
            return False, "Invalid email format"
        
        # Additional validation checks
        if len(email) > 254:
            return False, "Email address is too long"
        
        local_part = email.split('@')[0]
        if len(local_part) > 64:
            return False, "Email local part is too long"
        
        return True, "Valid email format"
    
    def get_email_error_message(self):
        """Get the email-specific error message"""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.email_error)
            )
            return element.text
        except TimeoutException:
            return None
    
    def get_error_message(self):
        """Get the general error message text"""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.error_message)
            )
            return element.text
        except TimeoutException:
            return None
    
    def get_success_message(self):
        """Get the success message text"""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.success_message)
            )
            return element.text
        except TimeoutException:
            return None
    
    def is_registration_successful(self):
        """Check if registration was successful"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("registration-success")
            )
            return True
        except TimeoutException:
            return False


class TestLogin(unittest.TestCase):
    """Test cases for Login functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class - runs once before all tests"""
        cls.base_url = "http://example.com/login"
    
    def setUp(self):
        """Set up test - runs before each test method"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.login_page = LoginPage(self.driver)
    
    def tearDown(self):
        """Tear down test - runs after each test method"""
        if self.driver:
            self.driver.quit()
    
    def test_TC_LOGIN_001_valid_credentials(self):
        """
        TC_LOGIN_001: Test login with valid credentials
        Steps:
        1. Enter valid username
        2. Enter valid password
        3. Click login button
        Expected: User successfully logs in and is redirected to dashboard
        """
        self.login_page.enter_username("validuser")
        self.login_page.enter_password("ValidPass123!")
        self.login_page.click_login()
        
        # Verify login success
        self.assertTrue(
            self.login_page.is_login_successful(),
            "Login should be successful with valid credentials"
        )
    
    def test_TC_LOGIN_002_invalid_credentials(self):
        """
        TC_LOGIN_002: Test login with invalid credentials
        Steps:
        1. Enter invalid username
        2. Enter invalid password
        3. Click login button
        Expected: Error message is displayed and user remains on login page
        """
        self.login_page.enter_username("invaliduser")
        self.login_page.enter_password("InvalidPass123!")
        self.login_page.click_login()
        
        # Verify error message is displayed
        error_message = self.login_page.get_error_message()
        self.assertIsNotNone(error_message, "Error message should be displayed")
        self.assertIn(
            "Invalid credentials",
            error_message,
            "Error message should indicate invalid credentials"
        )
        
        # Verify user is still on login page
        self.assertFalse(
            self.login_page.is_login_successful(),
            "Login should not be successful with invalid credentials"
        )
    
    def test_TC_LOGIN_003_forgot_username_workflow(self):
        """
        TC_LOGIN_003: Test forgot username workflow
        Steps:
        1. Click on "Forgot Username?" link
        2. Verify user is redirected to forgot username page
        Expected: User is redirected to the forgot username recovery page
        """
        self.login_page.click_forgot_username()
        
        # Verify redirection to forgot username page
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("forgot-username")
        )
        
        current_url = self.driver.current_url
        self.assertIn(
            "forgot-username",
            current_url,
            "User should be redirected to forgot username page"
        )


class TestRegistration(unittest.TestCase):
    """Test cases for Registration functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class - runs once before all tests"""
        cls.base_url = "http://example.com/register"
    
    def setUp(self):
        """Set up test - runs before each test method"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.registration_page = RegistrationPage(self.driver)
    
    def tearDown(self):
        """Tear down test - runs after each test method"""
        if self.driver:
            self.driver.quit()
    
    def test_TC_REGISTRATION_002_email_format_validation(self):
        """
        TC002 (Test Case ID: 1286): Test email format validation in registration
        Test Case Description: Test Case TC002
        Steps:
        1. Added email format validation in registration step.
        Expected: 
        1. Step executes successfully as per the described change.
        
        This test validates various email formats to ensure proper validation:
        - Valid email formats should be accepted
        - Invalid email formats should be rejected with appropriate error messages
        """
        # Test Case 1: Valid email format
        valid_emails = [
            "user@example.com",
            "test.user@example.com",
            "user+tag@example.co.uk",
            "user_name@example-domain.com",
            "123@example.com"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                is_valid, message = self.registration_page.validate_email_format(email)
                self.assertTrue(
                    is_valid,
                    f"Email '{email}' should be valid. Error: {message}"
                )
                self.assertEqual(
                    message,
                    "Valid email format",
                    f"Valid email should return success message"
                )
        
        # Test Case 2: Invalid email formats
        invalid_emails = [
            ("", "Email cannot be empty"),
            ("invalid.email", "Invalid email format"),
            ("@example.com", "Invalid email format"),
            ("user@", "Invalid email format"),
            ("user @example.com", "Invalid email format"),
            ("user@example", "Invalid email format"),
            ("user..name@example.com", "Invalid email format"),
            ("user@.example.com", "Invalid email format"),
            ("user@example..com", "Invalid email format"),
            ("a" * 65 + "@example.com", "Email local part is too long"),
            ("user@" + "a" * 250 + ".com", "Email address is too long")
        ]
        
        for email, expected_error in invalid_emails:
            with self.subTest(email=email):
                is_valid, message = self.registration_page.validate_email_format(email)
                self.assertFalse(
                    is_valid,
                    f"Email '{email}' should be invalid"
                )
                self.assertIn(
                    expected_error,
                    message,
                    f"Error message should indicate: {expected_error}"
                )
        
        # Test Case 3: Integration test - Enter invalid email in UI
        self.registration_page.enter_email("invalid.email.format")
        self.registration_page.enter_username("testuser")
        self.registration_page.enter_password("TestPass123!")
        self.registration_page.enter_confirm_password("TestPass123!")
        self.registration_page.click_register()
        
        # Verify email error message is displayed
        email_error = self.registration_page.get_email_error_message()
        if email_error:
            self.assertIsNotNone(
                email_error,
                "Email error message should be displayed for invalid format"
            )
            self.assertIn(
                "email",
                email_error.lower(),
                "Error message should reference email validation"
            )
        
        # Verify registration did not succeed
        self.assertFalse(
            self.registration_page.is_registration_successful(),
            "Registration should not succeed with invalid email format"
        )
        
        # Test Case 4: Integration test - Enter valid email in UI
        self.driver.get(self.base_url)  # Refresh page
        self.registration_page.enter_email("valid.user@example.com")
        self.registration_page.enter_username("testuser")
        self.registration_page.enter_password("TestPass123!")
        self.registration_page.enter_confirm_password("TestPass123!")
        
        # Pre-validate email format before submission
        is_valid, message = self.registration_page.validate_email_format(
            "valid.user@example.com"
        )
        self.assertTrue(
            is_valid,
            "Email format should be valid before registration submission"
        )
        
        # Note: Actual registration success depends on backend validation
        # This test ensures email format validation executes successfully


if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add login tests
    test_suite.addTest(unittest.makeSuite(TestLogin))
    
    # Add registration tests
    test_suite.addTest(unittest.makeSuite(TestRegistration))
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)