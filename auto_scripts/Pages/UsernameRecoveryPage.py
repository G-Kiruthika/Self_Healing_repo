from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UsernameRecoveryPage:
    """
    Page Object for the 'Forgot Username' workflow.
    Provides methods to interact with the username recovery process.
    Updated for TC_LOGIN_003 to support structured end-to-end automation.
    """
    URL = "https://example-ecommerce.com/forgot-username"
    EMAIL_FIELD = (By.ID, "recovery-email")
    SUBMIT_BUTTON = (By.ID, "recovery-submit")
    CONFIRMATION_MESSAGE = (By.CSS_SELECTOR, "div.recovery-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.recovery-error")
    INSTRUCTIONS_TEXT = (By.CSS_SELECTOR, "div.recovery-instructions")
    USERNAME_RESULT = (By.CSS_SELECTOR, "span.recovered-username")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to_username_recovery(self):
        """Navigate to the username recovery page and wait for the email field and instructions."""
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.INSTRUCTIONS_TEXT))

    def enter_email(self, email):
        """Enter the provided email into the recovery email field."""
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def submit_recovery(self):
        """Click the submit button to initiate username recovery."""
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()

    def get_confirmation_message(self):
        """Return the confirmation message after successful recovery, or None."""
        try:
            msg_elem = self.wait.until(EC.visibility_of_element_located(self.CONFIRMATION_MESSAGE))
            return msg_elem.text
        except:
            return None

    def get_error_message(self):
        """Return the error message if recovery fails, or None."""
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None

    def get_recovered_username(self):
        """Return the recovered username if displayed, or None."""
        try:
            username_elem = self.wait.until(EC.visibility_of_element_located(self.USERNAME_RESULT))
            return username_elem.text
        except:
            return None

    def recover_username(self, email):
        """End-to-end workflow: go to recovery page, enter email, submit, return confirmation or error."""
        self.go_to_username_recovery()
        self.enter_email(email)
        self.submit_recovery()
        confirmation = self.get_confirmation_message()
        if confirmation:
            return confirmation
        else:
            return self.get_error_message()

    def execute_tc_login_003(self, email):
        """Structured execution for TC_LOGIN_003 for downstream automation/reporting."""
        results = {}
        try:
            self.go_to_username_recovery()
            results["step_3_navigate_recovery"] = True
            self.enter_email(email)
            self.submit_recovery()
            confirmation = self.get_confirmation_message()
            error = self.get_error_message()
            recovered_username = self.get_recovered_username()
            if confirmation:
                results["step_4_recovery_success"] = True
                results["confirmation_message"] = confirmation
                results["recovered_username"] = recovered_username
            elif error:
                results["step_4_recovery_success"] = False
                results["error_message"] = error
            else:
                results["step_4_recovery_success"] = False
                results["error_message"] = "No response received"
        except Exception as e:
            results["step_3_navigate_recovery"] = False
            results["step_4_recovery_success"] = False
            results["error"] = str(e)
        results["overall_pass"] = results.get("step_3_navigate_recovery", False) and results.get("step_4_recovery_success", False)
        return results