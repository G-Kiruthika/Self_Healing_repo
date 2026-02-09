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
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.INSTRUCTIONS_TEXT))

    def is_instructions_displayed(self):
        try:
            instructions_elem = self.wait.until(EC.visibility_of_element_located(self.INSTRUCTIONS_TEXT))
            return instructions_elem.is_displayed()
        except:
            return False

    def enter_recovery_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def submit_recovery(self):
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()

    def get_success_message(self):
        try:
            success_elem = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return success_elem.text
        except:
            return None

    def get_recovered_username(self):
        try:
            username_elem = self.wait.until(EC.visibility_of_element_located(self.USERNAME_RESULT))
            return username_elem.text
        except:
            return None

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None

    def perform_username_recovery(self, email):
        result = {
            "success": False,
            "message": "",
            "recovered_username": None,
            "instructions_displayed": False
        }
        try:
            result["instructions_displayed"] = self.is_instructions_displayed()
            if not result["instructions_displayed"]:
                result["message"] = "Username recovery instructions not displayed"
                return result
            self.enter_recovery_email(email)
            self.submit_recovery()
            success_msg = self.get_success_message()
            if success_msg:
                result["success"] = True
                result["message"] = success_msg
                recovered_username = self.get_recovered_username()
                if recovered_username:
                    result["recovered_username"] = recovered_username
                return result
            error_msg = self.get_error_message()
            if error_msg:
                result["message"] = error_msg
                return result
            result["message"] = "No response received from username recovery system"
            return result
        except Exception as e:
            result["message"] = f"Error during username recovery: {str(e)}"
            return result

    def run_tc_login_003_username_recovery(self, email):
        return self.perform_username_recovery(email)
