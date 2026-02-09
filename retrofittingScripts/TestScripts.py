"""
Test Scripts Module - Automated Test Cases
Contains test classes for login functionality including forgot username workflow
"""

import unittest
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
    """Test Case: Invalid Login"""
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
    
    def test_invalid_login(self):
        """Verify error message with invalid credentials"""
        self.login_page.navigate_to_login()
        self.login_page.enter_username("invaliduser")
        self.login_page.enter_password("WrongPass")
        self.login_page.click_login()
        time.sleep(1)
        error = self.login_page.get_error_message()
        self.assertIsNotNone(error)
        self.assertIn("invalid", error.lower())
    
    def tearDown(self):
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


if __name__ == "__main__":
    unittest.main()