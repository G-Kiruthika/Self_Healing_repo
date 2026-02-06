from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UsernameRecoveryPage:
    """
    Page Object for the Username Recovery workflow.
    Provides methods to interact with the username recovery process.
    Updated for TC_LOGIN_003 to support structured end-to-end automation.
    """
    URL = "https://example-ecommerce.com/forgot-username"
    INSTRUCTIONS_TEXT = (By.CSS_SELECTOR, "div.recovery-instructions")
    EMAIL_FIELD = (By.ID, "recovery-email")
    SUBMIT_BUTTON = (By.ID, "recovery-submit")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.recovery-success")
    USERNAME_RESULT = (By.CSS_SELECTOR, "span.recovered-username")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.recovery-error")

    def __init__(self, driver, timeout=10):
        """
        Initialize with Selenium WebDriver and optional timeout.
        Args:
            driver: Selenium WebDriver instance
            timeout (int): Wait timeout in seconds (default: 10)
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to_username_recovery_page(self):
        """
        Navigates directly to the Username Recovery page.
        """
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.INSTRUCTIONS_TEXT))

    def is_instructions_displayed(self):
        """
        TC_LOGIN_003 Step 4: Checks if the recovery instructions are displayed.
        Expected result: Username recovery instructions are visible.
        Returns:
            bool: True if instructions are displayed, False otherwise.
        """
        try:
            instructions_elem = self.wait.until(EC.visibility_of_element_located(self.INSTRUCTIONS_TEXT))
            return instructions_elem.is_displayed()
        except:
            return False

    def enter_recovery_email(self, email):
        """
        TC_LOGIN_003 Step 4: Enters the email address into the recovery field.
        Args:
            email (str): Email address for username recovery
        """
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def submit_recovery(self):
        """
        TC_LOGIN_003 Step 4: Clicks the submit button to start username recovery.
        """
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()

    def get_success_message(self):
        """
        TC_LOGIN_003 Step 4: Returns the success message shown after successful recovery.
        Expected result: Username recovery success message is displayed.
        Returns:
            str: Success message text, or None if not found.
        """
        try:
            success_elem = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return success_elem.text
        except:
            return None

    def get_recovered_username(self):
        """
        TC_LOGIN_003 Step 4: Returns the recovered username displayed on the page.
        Expected result: Username is retrieved and displayed.
        Returns:
            str: Recovered username text, or None if not found.
        """
        try:
            username_elem = self.wait.until(EC.visibility_of_element_located(self.USERNAME_RESULT))
            return username_elem.text
        except:
            return None

    def get_error_message(self):
        """
        Returns error message if recovery fails.
        Returns:
            str: Error message text, or None if not found.
        """
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None

    def perform_username_recovery(self, email):
        """
        TC_LOGIN_003 Step 4: Complete username recovery workflow.
        Follows the instructions to recover username using the provided email.
        Args:
            email (str): Email address for username recovery
        Returns:
            dict: Recovery result with success status, message, and recovered username (if any)
        """
        result = {
            "success": False,
            "message": "",
            "recovered_username": None,
            "instructions_displayed": False
        }
        
        try:
            # Check if instructions are displayed
            result["instructions_displayed"] = self.is_instructions_displayed()
            
            if not result["instructions_displayed"]:
                result["message"] = "Username recovery instructions not displayed"
                return result
            
            # Enter email and submit recovery
            self.enter_recovery_email(email)
            self.submit_recovery()
            
            # Check for success message
            success_msg = self.get_success_message()
            if success_msg:
                result["success"] = True
                result["message"] = success_msg
                
                # Try to get recovered username if displayed
                recovered_username = self.get_recovered_username()
                if recovered_username:
                    result["recovered_username"] = recovered_username
                
                return result
            
            # Check for error message
            error_msg = self.get_error_message()
            if error_msg:
                result["message"] = error_msg
                return result
            
            # No clear response
            result["message"] = "No response received from username recovery system"
            return result
            
        except Exception as e:
            result["message"] = f"Error during username recovery: {str(e)}"
            return result

    def run_tc_login_003_username_recovery(self, email):
        """
        TC_LOGIN_003 Step 4: Execute complete username recovery process.
        Args:
            email (str): Email address for username recovery
        Returns:
            dict: Complete test results for TC_LOGIN_003 Step 4
        """
        return self.perform_username_recovery(email)