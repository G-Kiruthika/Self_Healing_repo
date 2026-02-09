"""
Test Scripts for Login Functionality
Automated Test Cases with Page Object Model

Test Case Coverage:
- TC_LOGIN_002: Remember Me Checkbox Verification
- TC_LOGIN_003: Forgot Username Recovery Workflow
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class LoginPage:
    """
    Page Object Model for Login Page
    Handles all login-related interactions and forgot username workflow
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Login Page Locators
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "loginButton")
        self.forgot_username_link = (By.LINK_TEXT, "Forgot Username")
        self.forgot_username_alt_link = (By.XPATH, "//a[contains(text(), 'Forgot Username')]")
        self.remember_me_checkbox = (By.ID, "rememberMe")
        self.remember_me_checkbox_alt = (By.XPATH, "//input[@type='checkbox' and contains(@name, 'remember')]")
        
        # Forgot Username Page Locators
        self.email_input = (By.ID, "recoveryEmail")
        self.recovery_submit_button = (By.ID, "submitRecovery")
        self.recovery_instructions = (By.CLASS_NAME, "recovery-instructions")
        self.username_display = (By.ID, "retrievedUsername")
        self.success_message = (By.CLASS_NAME, "success-message")
        
    def navigate_to_login_screen(self, url):
        """
        Navigate to the login screen
        
        Args:
            url (str): The URL of the login page
            
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located(self.username_input))
            print("✓ Successfully navigated to login screen")
            return True
        except Exception as e:
            print(f"✗ Failed to navigate to login screen: {str(e)}")
            return False
    
    def verify_login_screen_displayed(self):
        """
        Verify that the login screen is displayed
        
        Returns:
            bool: True if login screen is displayed, False otherwise
        """
        try:
            username_field = self.wait.until(
                EC.visibility_of_element_located(self.username_input)
            )
            password_field = self.driver.find_element(*self.password_input)
            login_btn = self.driver.find_element(*self.login_button)
            
            if username_field.is_displayed() and password_field.is_displayed() and login_btn.is_displayed():
                print("✓ Login screen is displayed with all required elements")
                return True
            return False
        except Exception as e:
            print(f"✗ Login screen verification failed: {str(e)}")
            return False
    
    def verify_remember_me_checkbox_absent(self):
        """
        Verify that the 'Remember Me' checkbox is not present on the login screen
        
        Returns:
            bool: True if 'Remember Me' checkbox is absent, False if present
        """
        try:
            # Try to find the checkbox using primary locator
            try:
                checkbox = self.driver.find_element(*self.remember_me_checkbox)
                if checkbox.is_displayed():
                    print("✗ 'Remember Me' checkbox is present (should be absent)")
                    return False
            except NoSuchElementException:
                pass  # Expected - checkbox not found with primary locator
            
            # Try alternative locator
            try:
                checkbox_alt = self.driver.find_element(*self.remember_me_checkbox_alt)
                if checkbox_alt.is_displayed():
                    print("✗ 'Remember Me' checkbox is present (should be absent)")
                    return False
            except NoSuchElementException:
                pass  # Expected - checkbox not found with alternative locator
            
            # If we reach here, checkbox is not present
            print("✓ 'Remember Me' checkbox is not present as expected")
            return True
            
        except Exception as e:
            # Any other exception means we couldn't verify properly
            print(f"✗ Failed to verify 'Remember Me' checkbox absence: {str(e)}")
            return False
    
    def click_forgot_username_link(self):
        """
        Click on the 'Forgot Username' link
        
        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            # Try primary locator first
            try:
                forgot_link = self.wait.until(
                    EC.element_to_be_clickable(self.forgot_username_link)
                )
            except TimeoutException:
                # Fallback to alternative locator
                forgot_link = self.wait.until(
                    EC.element_to_be_clickable(self.forgot_username_alt_link)
                )
            
            forgot_link.click()
            print("✓ Successfully clicked 'Forgot Username' link")
            return True
        except Exception as e:
            print(f"✗ Failed to click 'Forgot Username' link: {str(e)}")
            return False
    
    def verify_forgot_username_workflow_initiated(self):
        """
        Verify that the 'Forgot Username' workflow is initiated
        
        Returns:
            bool: True if workflow initiated, False otherwise
        """
        try:
            # Wait for recovery page elements to be visible
            recovery_field = self.wait.until(
                EC.visibility_of_element_located(self.email_input)
            )
            instructions = self.driver.find_element(*self.recovery_instructions)
            
            if recovery_field.is_displayed() and instructions.is_displayed():
                print("✓ 'Forgot Username' workflow is initiated successfully")
                return True
            return False
        except Exception as e:
            print(f"✗ Failed to verify forgot username workflow: {str(e)}")
            return False
    
    def follow_username_recovery_instructions(self, recovery_email):
        """
        Follow the instructions to recover username
        
        Args:
            recovery_email (str): Email address for username recovery
            
        Returns:
            bool: True if instructions followed successfully, False otherwise
        """
        try:
            # Read recovery instructions
            instructions = self.driver.find_element(*self.recovery_instructions)
            instruction_text = instructions.text
            print(f"Recovery Instructions: {instruction_text}")
            
            # Enter recovery email
            email_field = self.driver.find_element(*self.email_input)
            email_field.clear()
            email_field.send_keys(recovery_email)
            print(f"✓ Entered recovery email: {recovery_email}")
            
            # Submit recovery request
            submit_button = self.driver.find_element(*self.recovery_submit_button)
            submit_button.click()
            print("✓ Submitted username recovery request")
            
            return True
        except Exception as e:
            print(f"✗ Failed to follow recovery instructions: {str(e)}")
            return False
    
    def verify_username_retrieved(self):
        """
        Verify that username is retrieved successfully
        
        Returns:
            tuple: (bool, str) - Success status and retrieved username
        """
        try:
            # Wait for success message
            success_msg = self.wait.until(
                EC.visibility_of_element_located(self.success_message)
            )
            
            # Get retrieved username
            username_element = self.wait.until(
                EC.visibility_of_element_located(self.username_display)
            )
            retrieved_username = username_element.text
            
            if success_msg.is_displayed() and retrieved_username:
                print(f"✓ Username retrieved successfully: {retrieved_username}")
                return True, retrieved_username
            return False, None
        except Exception as e:
            print(f"✗ Failed to verify username retrieval: {str(e)}")
            return False, None


class TC_LOGIN_002:
    """
    Test Case: TC_LOGIN_002 - Remember Me Checkbox Verification
    
    Test Case ID: 107
    Description: Test Case TC_LOGIN_002
    
    Test Steps:
    1. Navigate to the login screen
    2. Verify login screen is displayed
    3. Check for the presence of 'Remember Me' checkbox (Expected: Not present)
    """
    
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.login_page = LoginPage(driver)
        self.test_case_id = "TC_LOGIN_002"
        self.test_case_number = "107"
        self.test_results = []
        
    def execute(self):
        """
        Execute TC_LOGIN_002 test case
        
        Returns:
            dict: Test execution results
        """
        print(f"\n{'='*60}")
        print(f"Executing Test Case: {self.test_case_id}")
        print(f"Test Case ID: {self.test_case_number}")
        print(f"{'='*60}\n")
        
        test_passed = True
        
        # Step 1: Navigate to the login screen
        print("Step 1: Navigate to the login screen")
        step1_result = self.login_page.navigate_to_login_screen(self.base_url)
        self.test_results.append({
            "step": 1,
            "description": "Navigate to the login screen",
            "expected": "Login screen is displayed",
            "status": "PASS" if step1_result else "FAIL"
        })
        test_passed = test_passed and step1_result
        time.sleep(1)
        
        # Step 2: Verify login screen is displayed
        print("\nStep 2: Verify login screen is displayed")
        step2_result = self.login_page.verify_login_screen_displayed()
        self.test_results.append({
            "step": 2,
            "description": "Verify login screen is displayed",
            "expected": "Login screen is displayed",
            "status": "PASS" if step2_result else "FAIL"
        })
        test_passed = test_passed and step2_result
        time.sleep(1)
        
        # Step 3: Check for the presence of 'Remember Me' checkbox
        print("\nStep 3: Check for the presence of 'Remember Me' checkbox")
        step3_result = self.login_page.verify_remember_me_checkbox_absent()
        self.test_results.append({
            "step": 3,
            "description": "Check for the presence of 'Remember Me' checkbox",
            "expected": "'Remember Me' checkbox is not present",
            "status": "PASS" if step3_result else "FAIL"
        })
        test_passed = test_passed and step3_result
        
        # Print test summary
        self.print_test_summary(test_passed)
        
        return {
            "test_case_id": self.test_case_id,
            "test_case_number": self.test_case_number,
            "overall_status": "PASS" if test_passed else "FAIL",
            "steps": self.test_results
        }
    
    def print_test_summary(self, test_passed):
        """Print test execution summary"""
        print(f"\n{'='*60}")
        print("Test Execution Summary")
        print(f"{'='*60}")
        print(f"Test Case: {self.test_case_id}")
        print(f"Test Case ID: {self.test_case_number}")
        print(f"Overall Status: {'PASS' if test_passed else 'FAIL'}")
        print(f"\nStep-by-Step Results:")
        for result in self.test_results:
            status_symbol = "✓" if result['status'] == "PASS" else "✗"
            print(f"  {status_symbol} Step {result['step']}: {result['description']} - {result['status']}")
        print(f"{'='*60}\n")


class TC_LOGIN_003:
    """
    Test Case: TC_LOGIN_003 - Forgot Username Recovery
    
    Test Case ID: 108
    Description: Test Case TC_LOGIN_003
    
    Test Steps:
    1. Navigate to the login screen
    2. Verify login screen is displayed
    3. Click on 'Forgot Username' link
    4. Verify 'Forgot Username' workflow is initiated
    5. Follow the instructions to recover username
    6. Verify username is retrieved successfully
    """
    
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.login_page = LoginPage(driver)
        self.test_case_id = "TC_LOGIN_003"
        self.test_case_number = "108"
        self.test_results = []
        
    def execute(self, recovery_email="testuser@example.com"):
        """
        Execute TC_LOGIN_003 test case
        
        Args:
            recovery_email (str): Email address for username recovery
            
        Returns:
            dict: Test execution results
        """
        print(f"\n{'='*60}")
        print(f"Executing Test Case: {self.test_case_id}")
        print(f"Test Case ID: {self.test_case_number}")
        print(f"{'='*60}\n")
        
        test_passed = True
        
        # Step 1: Navigate to the login screen
        print("Step 1: Navigate to the login screen")
        step1_result = self.login_page.navigate_to_login_screen(self.base_url)
        self.test_results.append({
            "step": 1,
            "description": "Navigate to the login screen",
            "expected": "Login screen is displayed",
            "status": "PASS" if step1_result else "FAIL"
        })
        test_passed = test_passed and step1_result
        time.sleep(1)
        
        # Step 2: Verify login screen is displayed
        print("\nStep 2: Verify login screen is displayed")
        step2_result = self.login_page.verify_login_screen_displayed()
        self.test_results.append({
            "step": 2,
            "description": "Verify login screen is displayed",
            "expected": "Login screen is displayed with all elements",
            "status": "PASS" if step2_result else "FAIL"
        })
        test_passed = test_passed and step2_result
        time.sleep(1)
        
        # Step 3: Click on 'Forgot Username' link
        print("\nStep 3: Click on 'Forgot Username' link")
        step3_result = self.login_page.click_forgot_username_link()
        self.test_results.append({
            "step": 3,
            "description": "Click on 'Forgot Username' link",
            "expected": "'Forgot Username' workflow is initiated",
            "status": "PASS" if step3_result else "FAIL"
        })
        test_passed = test_passed and step3_result
        time.sleep(1)
        
        # Step 4: Verify 'Forgot Username' workflow is initiated
        print("\nStep 4: Verify 'Forgot Username' workflow is initiated")
        step4_result = self.login_page.verify_forgot_username_workflow_initiated()
        self.test_results.append({
            "step": 4,
            "description": "Verify 'Forgot Username' workflow is initiated",
            "expected": "Recovery page is displayed with instructions",
            "status": "PASS" if step4_result else "FAIL"
        })
        test_passed = test_passed and step4_result
        time.sleep(1)
        
        # Step 5: Follow the instructions to recover username
        print("\nStep 5: Follow the instructions to recover username")
        step5_result = self.login_page.follow_username_recovery_instructions(recovery_email)
        self.test_results.append({
            "step": 5,
            "description": "Follow the instructions to recover username",
            "expected": "Username recovery instructions are followed",
            "status": "PASS" if step5_result else "FAIL"
        })
        test_passed = test_passed and step5_result
        time.sleep(2)
        
        # Step 6: Verify username is retrieved successfully
        print("\nStep 6: Verify username is retrieved successfully")
        step6_result, retrieved_username = self.login_page.verify_username_retrieved()
        self.test_results.append({
            "step": 6,
            "description": "Verify username is retrieved successfully",
            "expected": "Username is retrieved and displayed",
            "status": "PASS" if step6_result else "FAIL",
            "retrieved_username": retrieved_username
        })
        test_passed = test_passed and step6_result
        
        # Print test summary
        self.print_test_summary(test_passed)
        
        return {
            "test_case_id": self.test_case_id,
            "test_case_number": self.test_case_number,
            "overall_status": "PASS" if test_passed else "FAIL",
            "steps": self.test_results,
            "retrieved_username": retrieved_username if step6_result else None
        }
    
    def print_test_summary(self, test_passed):
        """Print test execution summary"""
        print(f"\n{'='*60}")
        print("Test Execution Summary")
        print(f"{'='*60}")
        print(f"Test Case: {self.test_case_id}")
        print(f"Test Case ID: {self.test_case_number}")
        print(f"Overall Status: {'PASS' if test_passed else 'FAIL'}")
        print(f"\nStep-by-Step Results:")
        for result in self.test_results:
            status_symbol = "✓" if result['status'] == "PASS" else "✗"
            print(f"  {status_symbol} Step {result['step']}: {result['description']} - {result['status']}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    # Example usage
    print("Test Scripts Module Loaded Successfully")
    print("Available Test Cases:")
    print("  - TC_LOGIN_002: Remember Me Checkbox Verification")
    print("  - TC_LOGIN_003: Forgot Username Recovery Workflow")
    print("\nTo execute test cases, import this module and use:")
    print("  driver = webdriver.Chrome()  # or your preferred driver")
    print("  test_002 = TC_LOGIN_002(driver, 'https://your-app-url.com/login')")
    print("  results_002 = test_002.execute()")
    print("  test_003 = TC_LOGIN_003(driver, 'https://your-app-url.com/login')")
    print("  results_003 = test_003.execute(recovery_email='user@example.com')")
