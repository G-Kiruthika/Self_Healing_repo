from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PasswordRecoveryPage:
    """
    Page Object for the 'Forgot Password' workflow.
    Provides methods to interact with the password recovery process.
    """
    URL = "https://example-ecommerce.com/forgot-password"
    EMAIL_FIELD = (By.ID, "recovery-email")
    SUBMIT_BUTTON = (By.ID, "recovery-submit")
    CONFIRMATION_MESSAGE = (By.CSS_SELECTOR, "div.recovery-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.recovery-error")
    INSTRUCTIONS_TEXT = (By.CSS_SELECTOR, "div.recovery-instructions")

    def __init__(self, driver, timeout=10):
        """
        Initialize with Selenium WebDriver and optional timeout.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to_password_recovery(self):
        """
        Navigates to the Password Recovery page.
        """
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.INSTRUCTIONS_TEXT))

    def enter_email(self, email):
        """
        Enters the email address for password recovery.
        """
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def submit_recovery(self):
        """
        Submits the password recovery request.
        """
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()

    def get_confirmation_message(self):
        """
        Retrieves the confirmation message after successful recovery.
        """
        try:
            msg_elem = self.wait.until(EC.visibility_of_element_located(self.CONFIRMATION_MESSAGE))
            return msg_elem.text
        except:
            return None

    def get_error_message(self):
        """
        Retrieves any error message displayed during recovery.
        """
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None

    def recover_password(self, email):
        """
        Complete workflow: enter email, submit, return confirmation or error.
        """
        self.go_to_password_recovery()
        self.enter_email(email)
        self.submit_recovery()
        confirmation = self.get_confirmation_message()
        if confirmation:
            return confirmation
        else:
            return self.get_error_message()
