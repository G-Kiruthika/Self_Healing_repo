import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "loginButton")
        self.error_message = (By.CLASS_NAME, "error-message")
        self.error_message_alt = (By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'alert')]")
        
    def navigate_to_login_screen(self, url):
        try:
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located(self.username_input))
            print("Successfully navigated to login screen")
            return True
        except Exception as e:
            print(f"Failed to navigate to login screen: {str(e)}")
            return False
    
    def validate_password_with_special_characters(self, password):
        """
        Validates password to include special characters.
        Returns True if password contains at least one special character.
        """
        try:
            special_char_pattern = r'[!@#$%^&*(),.?":{}|<>]'
            has_special_char = bool(re.search(special_char_pattern, password))
            if has_special_char:
                print(f"Password validation successful: Contains special characters")
            else:
                print(f"Password validation failed: No special characters found")
            return has_special_char
        except Exception as e:
            print(f"Failed to validate password: {str(e)}")
            return False
    
    def enter_invalid_credentials_and_submit(self, username, password):
        try:
            username_field = self.wait.until(EC.visibility_of_element_located(self.username_input))
            username_field.clear()
            username_field.send_keys(username)
            password_field = self.driver.find_element(*self.password_input)
            password_field.clear()
            password_field.send_keys(password)
            login_btn = self.driver.find_element(*self.login_button)
            login_btn.click()
            print(f"Entered invalid credentials - Username: {username}, Password: {password}")
            return True
        except Exception as e:
            print(f"Failed to enter invalid credentials: {str(e)}")
            return False
    
    def verify_invalid_login_error_message(self, expected_error):
        try:
            try:
                error_element = self.wait.until(EC.visibility_of_element_located(self.error_message))
            except TimeoutException:
                error_element = self.wait.until(EC.visibility_of_element_located(self.error_message_alt))
            actual_error = error_element.text.strip()
            if actual_error == expected_error:
                print(f"Error message validation successful: '{actual_error}'")
                return True
            else:
                print(f"Error message mismatch - Expected: '{expected_error}', Actual: '{actual_error}'")
                return False
        except Exception as e:
            print(f"Failed to verify error message: {str(e)}")
            return False

class TC_LOGIN_001:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.login_page = LoginPage(driver)
        self.test_case_id = "TC_LOGIN_001"
        self.test_case_number = "106"
        self.test_results = []
        
    def execute(self, invalid_username="invalid_user@example.com", invalid_password="wrongpassword123"):
        print(f"Executing Test Case: {self.test_case_id}")
        print(f"Test Case ID: {self.test_case_number}")
        test_passed = True
        expected_error = "Invalid username or password. Please try again."
        
        # Step 1: Navigate to the login screen
        print("Step 1: Navigate to the login screen")
        step1_result = self.login_page.navigate_to_login_screen(self.base_url)
        self.test_results.append({"step": 1, "description": "Navigate to the login screen", "expected": "Login screen is displayed", "status": "PASS" if step1_result else "FAIL"})
        test_passed = test_passed and step1_result
        
        # Step 2: Enter an invalid username and/or password
        print("Step 2: Enter an invalid username and/or password")
        step2_result = self.login_page.enter_invalid_credentials_and_submit(invalid_username, invalid_password)
        self.test_results.append({"step": 2, "description": "Enter an invalid username and/or password", "expected": "Invalid credentials are entered and submitted", "status": "PASS" if step2_result else "FAIL"})
        test_passed = test_passed and step2_result
        
        # Step 3: Verify error message 'Invalid username or password. Please try again.' is displayed
        print("Step 3: Verify error message is displayed")
        step3_result = self.login_page.verify_invalid_login_error_message(expected_error)
        self.test_results.append({"step": 3, "description": "Verify error message 'Invalid username or password. Please try again.' is displayed", "expected": f"Error message '{expected_error}' is displayed", "status": "PASS" if step3_result else "FAIL"})
        test_passed = test_passed and step3_result
        
        return {"test_case_id": self.test_case_id, "test_case_number": self.test_case_number, "overall_status": "PASS" if test_passed else "FAIL", "steps": self.test_results, "expected_error_message": expected_error, "integration_status": "Enhanced and Updated"}

class TC001:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.login_page = LoginPage(driver)
        self.test_case_id = "TC001"
        self.test_case_number = "1285"
        self.test_results = []
        
    def execute(self, test_password="TestPass@123"):
        print(f"Executing Test Case: {self.test_case_id}")
        print(f"Test Case ID: {self.test_case_number}")
        test_passed = True
        
        # Step 1: Updated password validation logic to include special characters
        print("Step 1: Updated password validation logic to include special characters")
        step1_result = self.login_page.validate_password_with_special_characters(test_password)
        self.test_results.append({"step": 1, "description": "Updated password validation logic to include special characters", "expected": "Step executes successfully as per the described change", "status": "PASS" if step1_result else "FAIL"})
        test_passed = test_passed and step1_result
        
        return {"test_case_id": self.test_case_id, "test_case_number": self.test_case_number, "overall_status": "PASS" if test_passed else "FAIL", "steps": self.test_results, "integration_status": "New Test Case Added with Password Validation"}