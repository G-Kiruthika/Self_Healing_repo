from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UsernameRecoveryPage:
    INSTRUCTIONS_TEXT = (By.CSS_SELECTOR, "div.recovery-instructions")
    EMAIL_FIELD = (By.ID, "recovery-email")
    SUBMIT_BUTTON = (By.ID, "recovery-submit")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.recovery-success")
    USERNAME_RESULT = (By.CSS_SELECTOR, "span.recovered-username")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.recovery-error")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def is_instructions_displayed(self):
        """
        Checks if the recovery instructions are displayed.
        """
        return self.wait.until(EC.visibility_of_element_located(self.INSTRUCTIONS_TEXT)) is not None

    def enter_recovery_email(self, email):
        """
        Enters the email address into the recovery field.
        """
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def submit_recovery(self):
        """
        Clicks the submit button to start username recovery.
        """
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()

    def get_success_message(self):
        """
        Returns the success message shown after successful recovery.
        """
        try:
            success_elem = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return success_elem.text
        except:
            return None

    def get_recovered_username(self):
        """
        Returns the recovered username displayed on the page.
        """
        try:
            username_elem = self.wait.until(EC.visibility_of_element_located(self.USERNAME_RESULT))
            return username_elem.text
        except:
            return None

    def get_error_message(self):
        """
        Returns error message if recovery fails.
        """
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None
