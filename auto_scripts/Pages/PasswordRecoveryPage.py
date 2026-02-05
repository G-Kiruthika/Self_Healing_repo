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
        """Step 3: Enter registered email address"""
        input_field = self.driver.find_element(*self.EMAIL_INPUT)
        input_field.clear()
        input_field.send_keys(email)
        return input_field.get_attribute("value") == email

    def click_send_reset_link(self):
        """Step 4: Click on 'Send Reset Link' button"""
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def is_success_message_displayed(self):
        """Step 4: Success message displayed: 'Password reset link sent to your email'"""
        try:
            success = self.driver.find_element(*self.SUCCESS_MESSAGE)
            return success.is_displayed() and 'Password reset link sent to your email' in success.text
        except NoSuchElementException:
            return False

    def is_error_message_displayed(self):
        """Check if error message appears after submitting recovery with invalid data."""
        try:
            error = self.driver.find_element(*self.ERROR_MESSAGE)
            return error.is_displayed()
        except NoSuchElementException:
            return False

    def verify_password_reset_email_received(self, email: str):
        """
        Step 5: Verify password reset email is received
        Note: This is a placeholder for integration with email checking service.
        Returns True if password reset email is received with valid reset link.
        """
        # In a real implementation, integrate with a test email inbox or use a mock service
        raise NotImplementedError("Email inbox check for password reset link must be implemented in the test harness or with an external email service.")

    # --- Start of TC_LOGIN_006 steps ---
    def tc_login_006_password_recovery_flow(self, email: str):
        """
        TC_LOGIN_006 Steps:
        3. Enter registered email address
        4. Click on 'Send Reset Link' button
        5. Verify password reset email is received
        """
        self.enter_email(email)
        self.click_send_reset_link()
        return self.is_success_message_displayed()
    # --- End of TC_LOGIN_006 steps ---
