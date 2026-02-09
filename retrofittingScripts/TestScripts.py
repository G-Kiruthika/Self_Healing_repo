import time
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
        self.forgot_username_link = (By.LINK_TEXT, "Forgot Username")
        self.forgot_username_alt_link = (By.XPATH, "//a[contains(text(), 'Forgot Username')]")
        self.remember_me_checkbox = (By.ID, "rememberMe")
        self.remember_me_checkbox_alt = (By.XPATH, "//input[@type='checkbox' and contains(@name, 'remember')]")
        self.email_input = (By.ID, "recoveryEmail")
        self.recovery_submit_button = (By.ID, "submitRecovery")
        self.recovery_instructions = (By.CLASS_NAME, "recovery-instructions")
        self.username_display = (By.ID, "retrievedUsername")
        self.success_message = (By.CLASS_NAME, "success-message")

    def enter_username(self, username):
        """Enter username in the username field"""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.username_input))
            element.clear()
            element.send_keys(username)
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error entering username: {e}")
            return False

    def enter_password(self, password):
        """Enter password in the password field"""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.password_input))
            element.clear()
            element.send_keys(password)
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error entering password: {e}")
            return False

    def click_login_button(self):
        """Click the login button"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.login_button))
            element.click()
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error clicking login button: {e}")
            return False

    def get_error_message(self):
        """Get error message text"""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.error_message))
            return element.text
        except (TimeoutException, NoSuchElementException):
            try:
                element = self.wait.until(EC.presence_of_element_located(self.error_message_alt))
                return element.text
            except (TimeoutException, NoSuchElementException) as e:
                print(f"Error getting error message: {e}")
                return None

    def is_login_screen_displayed(self):
        """Check if login screen is displayed"""
        try:
            self.wait.until(EC.presence_of_element_located(self.username_input))
            self.wait.until(EC.presence_of_element_located(self.password_input))
            self.wait.until(EC.presence_of_element_located(self.login_button))
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Login screen not displayed: {e}")
            return False

    def click_forgot_username_link(self):
        """Click on Forgot Username link"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.forgot_username_link))
            element.click()
            return True
        except (TimeoutException, NoSuchElementException):
            try:
                element = self.wait.until(EC.element_to_be_clickable(self.forgot_username_alt_link))
                element.click()
                return True
            except (TimeoutException, NoSuchElementException) as e:
                print(f"Error clicking forgot username link: {e}")
                return False

    def is_forgot_username_workflow_initiated(self):
        """Check if forgot username workflow is initiated"""
        try:
            self.wait.until(EC.presence_of_element_located(self.email_input))
            self.wait.until(EC.presence_of_element_located(self.recovery_submit_button))
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Forgot username workflow not initiated: {e}")
            return False

    def enter_recovery_email(self, email):
        """Enter email in the recovery email field"""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.email_input))
            element.clear()
            element.send_keys(email)
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error entering recovery email: {e}")
            return False

    def click_recovery_submit_button(self):
        """Click the recovery submit button"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.recovery_submit_button))
            element.click()
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error clicking recovery submit button: {e}")
            return False

    def are_recovery_instructions_displayed(self):
        """Check if recovery instructions are displayed"""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.recovery_instructions))
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Recovery instructions not displayed: {e}")
            return False

    def is_username_retrieved(self):
        """Check if username is retrieved and displayed"""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.username_display))
            return element.is_displayed() and len(element.text) > 0
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Username not retrieved: {e}")
            return False

    def get_retrieved_username(self):
        """Get the retrieved username"""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.username_display))
            return element.text
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error getting retrieved username: {e}")
            return None

    def get_success_message(self):
        """Get success message text"""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.success_message))
            return element.text
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error getting success message: {e}")
            return None


class TC_LOGIN_001:
    """Test Case: TC_LOGIN_001 - Valid Login Test"""
    
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.test_case_id = "TC_LOGIN_001"
        self.test_result = "Not Executed"
        self.test_steps_results = []

    def execute(self, base_url, username, password):
        """Execute TC_LOGIN_001 test case"""
        print(f"\n{'='*60}")
        print(f"Executing Test Case: {self.test_case_id}")
        print(f"{'='*60}\n")
        
        try:
            # Step 1: Navigate to login page
            print("Step 1: Navigate to the login page")
            self.driver.get(base_url)
            time.sleep(2)
            
            if self.login_page.is_login_screen_displayed():
                print("✓ Login screen is displayed")
                self.test_steps_results.append({"step": 1, "status": "PASS"})
            else:
                print("✗ Login screen is not displayed")
                self.test_steps_results.append({"step": 1, "status": "FAIL"})
                self.test_result = "FAIL"
                return self.test_result

            # Step 2: Enter valid username
            print(f"\nStep 2: Enter username: {username}")
            if self.login_page.enter_username(username):
                print("✓ Username entered successfully")
                self.test_steps_results.append({"step": 2, "status": "PASS"})
            else:
                print("✗ Failed to enter username")
                self.test_steps_results.append({"step": 2, "status": "FAIL"})
                self.test_result = "FAIL"
                return self.test_result

            # Step 3: Enter valid password
            print(f"\nStep 3: Enter password")
            if self.login_page.enter_password(password):
                print("✓ Password entered successfully")
                self.test_steps_results.append({"step": 3, "status": "PASS"})
            else:
                print("✗ Failed to enter password")
                self.test_steps_results.append({"step": 3, "status": "FAIL"})
                self.test_result = "FAIL"
                return self.test_result

            # Step 4: Click login button
            print(f"\nStep 4: Click login button")
            if self.login_page.click_login_button():
                print("✓ Login button clicked successfully")
                time.sleep(3)
                self.test_steps_results.append({"step": 4, "status": "PASS"})
            else:
                print("✗ Failed to click login button")
                self.test_steps_results.append({"step": 4, "status": "FAIL"})
                self.test_result = "FAIL"
                return self.test_result

            # Step 5: Verify successful login
            print(f"\nStep 5: Verify successful login")
            current_url = self.driver.current_url
            if "dashboard" in current_url.lower() or "home" in current_url.lower():
                print(f"✓ Login successful - Redirected to: {current_url}")
                self.test_steps_results.append({"step": 5, "status": "PASS"})
                self.test_result = "PASS"
            else:
                print(f"✗ Login failed - Current URL: {current_url}")
                self.test_steps_results.append({"step": 5, "status": "FAIL"})
                self.test_result = "FAIL"

        except Exception as e:
            print(f"\n✗ Test execution failed with error: {e}")
            self.test_result = "ERROR"
            self.test_steps_results.append({"step": "Exception", "status": "ERROR", "error": str(e)})

        finally:
            print(f"\n{'='*60}")
            print(f"Test Case: {self.test_case_id} - Result: {self.test_result}")
            print(f"{'='*60}\n")
            return self.test_result

    def get_test_results(self):
        """Return test results summary"""
        return {
            "test_case_id": self.test_case_id,
            "test_result": self.test_result,
            "test_steps_results": self.test_steps_results
        }


class TC_LOGIN_003:
    """Test Case: TC_LOGIN_003 - Forgot Username Workflow Test"""
    
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.test_case_id = "TC_LOGIN_003"
        self.test_case_description = "Test Case TC_LOGIN_003 - Forgot Username Workflow"
        self.test_result = "Not Executed"
        self.test_steps_results = []

    def execute(self, base_url, recovery_email):
        """Execute TC_LOGIN_003 test case"""
        print(f"\n{'='*60}")
        print(f"Executing Test Case: {self.test_case_id}")
        print(f"Description: {self.test_case_description}")
        print(f"{'='*60}\n")
        
        try:
            # Step 1: Navigate to the login screen
            print("Step 1: Navigate to the login screen")
            self.driver.get(base_url)
            time.sleep(2)
            
            if self.login_page.is_login_screen_displayed():
                print("✓ Login screen is displayed")
                self.test_steps_results.append({
                    "step_id": 1,
                    "step_desc": "Navigate to the login screen",
                    "expected": "Login screen is displayed",
                    "status": "PASS"
                })
            else:
                print("✗ Login screen is not displayed")
                self.test_steps_results.append({
                    "step_id": 1,
                    "step_desc": "Navigate to the login screen",
                    "expected": "Login screen is displayed",
                    "status": "FAIL"
                })
                self.test_result = "FAIL"
                return self.test_result

            # Step 2: Click on 'Forgot Username' link
            print("\nStep 2: Click on 'Forgot Username' link")
            if self.login_page.click_forgot_username_link():
                print("✓ 'Forgot Username' link clicked successfully")
                time.sleep(2)
                self.test_steps_results.append({
                    "step_id": 2,
                    "step_desc": "Click on 'Forgot Username' link",
                    "expected": "'Forgot Username' workflow is initiated",
                    "status": "PASS"
                })
            else:
                print("✗ Failed to click 'Forgot Username' link")
                self.test_steps_results.append({
                    "step_id": 2,
                    "step_desc": "Click on 'Forgot Username' link",
                    "expected": "'Forgot Username' workflow is initiated",
                    "status": "FAIL"
                })
                self.test_result = "FAIL"
                return self.test_result

            # Step 3: Verify 'Forgot Username' workflow is initiated
            print("\nStep 3: Verify 'Forgot Username' workflow is initiated")
            if self.login_page.is_forgot_username_workflow_initiated():
                print("✓ 'Forgot Username' workflow is initiated - Recovery form is displayed")
                self.test_steps_results.append({
                    "step_id": 3,
                    "step_desc": "Verify forgot username workflow initiated",
                    "expected": "Recovery form with email input is displayed",
                    "status": "PASS"
                })
            else:
                print("✗ 'Forgot Username' workflow was not initiated properly")
                self.test_steps_results.append({
                    "step_id": 3,
                    "step_desc": "Verify forgot username workflow initiated",
                    "expected": "Recovery form with email input is displayed",
                    "status": "FAIL"
                })
                self.test_result = "FAIL"
                return self.test_result

            # Step 4: Follow the instructions to recover username
            print(f"\nStep 4: Follow the instructions to recover username")
            print(f"  - Entering recovery email: {recovery_email}")
            
            if self.login_page.enter_recovery_email(recovery_email):
                print("  ✓ Recovery email entered successfully")
            else:
                print("  ✗ Failed to enter recovery email")
                self.test_steps_results.append({
                    "step_id": 4,
                    "step_desc": "Follow the instructions to recover username",
                    "expected": "Username recovery instructions are followed and username is retrieved",
                    "status": "FAIL"
                })
                self.test_result = "FAIL"
                return self.test_result

            print("  - Clicking recovery submit button")
            if self.login_page.click_recovery_submit_button():
                print("  ✓ Recovery submit button clicked successfully")
                time.sleep(3)
            else:
                print("  ✗ Failed to click recovery submit button")
                self.test_steps_results.append({
                    "step_id": 4,
                    "step_desc": "Follow the instructions to recover username",
                    "expected": "Username recovery instructions are followed and username is retrieved",
                    "status": "FAIL"
                })
                self.test_result = "FAIL"
                return self.test_result

            # Step 5: Verify username is retrieved
            print("\nStep 5: Verify username recovery instructions are followed and username is retrieved")
            
            # Check if recovery instructions are displayed
            if self.login_page.are_recovery_instructions_displayed():
                print("  ✓ Recovery instructions are displayed")
            
            # Check if username is retrieved
            if self.login_page.is_username_retrieved():
                retrieved_username = self.login_page.get_retrieved_username()
                print(f"  ✓ Username is retrieved successfully: {retrieved_username}")
                self.test_steps_results.append({
                    "step_id": 5,
                    "step_desc": "Follow the instructions to recover username",
                    "expected": "Username recovery instructions are followed and username is retrieved",
                    "status": "PASS",
                    "retrieved_username": retrieved_username
                })
                self.test_result = "PASS"
            else:
                print("  ✗ Username was not retrieved")
                self.test_steps_results.append({
                    "step_id": 5,
                    "step_desc": "Follow the instructions to recover username",
                    "expected": "Username recovery instructions are followed and username is retrieved",
                    "status": "FAIL"
                })
                self.test_result = "FAIL"

        except Exception as e:
            print(f"\n✗ Test execution failed with error: {e}")
            self.test_result = "ERROR"
            self.test_steps_results.append({
                "step_id": "Exception",
                "step_desc": "Test execution",
                "expected": "Test completes without errors",
                "status": "ERROR",
                "error": str(e)
            })

        finally:
            print(f"\n{'='*60}")
            print(f"Test Case: {self.test_case_id} - Result: {self.test_result}")
            print(f"{'='*60}\n")
            return self.test_result

    def get_test_results(self):
        """Return test results summary"""
        return {
            "test_case_id": self.test_case_id,
            "test_case_description": self.test_case_description,
            "test_result": self.test_result,
            "test_steps_results": self.test_steps_results
        }


# Main execution block for testing
if __name__ == "__main__":
    # Example usage
    driver = webdriver.Chrome()
    
    try:
        # Execute TC_LOGIN_001
        print("\n" + "="*80)
        print("EXECUTING TEST SUITE")
        print("="*80)
        
        tc_001 = TC_LOGIN_001(driver)
        result_001 = tc_001.execute(
            base_url="https://example.com/login",
            username="testuser",
            password="testpassword"
        )
        print(f"\nTC_LOGIN_001 Results: {tc_001.get_test_results()}")
        
        # Execute TC_LOGIN_003
        driver.get("https://example.com/login")  # Reset to login page
        time.sleep(2)
        
        tc_003 = TC_LOGIN_003(driver)
        result_003 = tc_003.execute(
            base_url="https://example.com/login",
            recovery_email="testuser@example.com"
        )
        print(f"\nTC_LOGIN_003 Results: {tc_003.get_test_results()}")
        
        print("\n" + "="*80)
        print("TEST SUITE EXECUTION COMPLETED")
        print("="*80)
        
    finally:
        driver.quit()
