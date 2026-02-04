# Selenium Page Object for PasswordRecoveryPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class PasswordRecoveryPage:
    PASSWORD_RECOVERY_URL = "https://app.example.com/forgot-password"
    EMAIL_INPUT = (By.ID, "recovery-email")
    SUBMIT_BUTTON = (By.ID, "recovery-submit")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.recovery-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.recovery-error")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def is_loaded(self):
        """Verify password recovery page is loaded by checking URL and main elements."""
        return self.driver.current_url.startswith(self.PASSWORD_RECOVERY_URL) and \
            self.driver.find_element(*self.EMAIL_INPUT).is_displayed() and \
            self.driver.find_element(*self.SUBMIT_BUTTON).is_displayed()

    def is_email_input_visible(self):
        """Check if email input field is visible."""
        try:
            input_field = self.driver.find_element(*self.EMAIL_INPUT)
            return input_field.is_displayed()
        except NoSuchElementException:
            return False

    def is_submit_button_visible(self):
        """Check if submit button is visible."""
        try:
            button = self.driver.find_element(*self.SUBMIT_BUTTON)
            return button.is_displayed()
        except NoSuchElementException:
            return False

    def enter_email(self, email: str):
        """Enter email address for password recovery."""
        input_field = self.driver.find_element(*self.EMAIL_INPUT)
        input_field.clear()
        input_field.send_keys(email)
        return input_field.get_attribute("value") == email

    def submit_recovery(self):
        """Click on submit button to initiate password recovery."""
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def is_success_message_displayed(self):
        """Check if success message appears after submitting recovery."""
        try:
            success = self.driver.find_element(*self.SUCCESS_MESSAGE)
            return success.is_displayed()
        except NoSuchElementException:
            return False

    def is_error_message_displayed(self):
        """Check if error message appears after submitting recovery with invalid data."""
        try:
            error = self.driver.find_element(*self.ERROR_MESSAGE)
            return error.is_displayed()
        except NoSuchElementException:
            return False

    def verify_page_elements(self):
        """
        TC_LOGIN_009 - Step 3: Verify password recovery page elements (email input and submit button).
        Returns True if both are visible.
        """
        return self.is_email_input_visible() and self.is_submit_button_visible()

    # --- ADDED FOR TC_LOGIN_010 ---
    def check_password_reset_email_received(self, email: str):
        """
        TC_LOGIN_010: Step 4 - Check email inbox for password reset link.
        Note: This is a placeholder for integration with email checking service.
        Returns True if password reset email is received with valid reset link.
        """
        # In a real implementation, integrate with a test email inbox or use a mock service
        # For now, raise NotImplementedError to indicate this step is external
        raise NotImplementedError("Email inbox check for password reset link must be implemented in the test harness or with an external email service.")
