# Selenium Page Object for UsernameRecoveryPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class UsernameRecoveryPage:
    USERNAME_RECOVERY_URL = "https://app.example.com/forgot-username"
    EMAIL_INPUT = (By.ID, "username-recovery-email")
    SEND_USERNAME_BUTTON = (By.ID, "send-username")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.recovery-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.recovery-error")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def is_loaded(self):
        """Verify username recovery page is loaded by checking URL and main elements."""
        return self.driver.current_url.startswith(self.USERNAME_RECOVERY_URL) and \
            self.driver.find_element(*self.EMAIL_INPUT).is_displayed() and \
            self.driver.find_element(*self.SEND_USERNAME_BUTTON).is_displayed()

    def is_email_input_visible(self):
        try:
            input_field = self.driver.find_element(*self.EMAIL_INPUT)
            return input_field.is_displayed()
        except NoSuchElementException:
            return False

    def is_send_username_button_visible(self):
        try:
            button = self.driver.find_element(*self.SEND_USERNAME_BUTTON)
            return button.is_displayed()
        except NoSuchElementException:
            return False

    def enter_email(self, email: str):
        """
        Step 3: Enter registered email address
        """
        input_field = self.driver.find_element(*self.EMAIL_INPUT)
        input_field.clear()
        input_field.send_keys(email)
        return input_field.get_attribute("value") == email

    def click_send_username(self):
        """
        Step 4: Click on 'Send Username' button
        """
        self.driver.find_element(*self.SEND_USERNAME_BUTTON).click()

    def is_success_message_displayed(self):
        """
        Step 4: Success message displayed: 'Username sent to your email'
        """
        try:
            success = self.driver.find_element(*self.SUCCESS_MESSAGE)
            return success.is_displayed() and 'Username sent to your email' in success.text
        except NoSuchElementException:
            return False

    def is_error_message_displayed(self):
        try:
            error = self.driver.find_element(*self.ERROR_MESSAGE)
            return error.is_displayed()
        except NoSuchElementException:
            return False

    def verify_username_recovery_email_received(self, email: str):
        """
        Step 5: Verify username recovery email is received
        Note: This is a placeholder for integration with email checking service.
        Returns True if username recovery email is received with valid username info.
        """
        # In a real implementation, integrate with a test email inbox or use a mock service
        raise NotImplementedError("Email inbox check for username recovery must be implemented in the test harness or with an external email service.")

    # --- Start of TC_LOGIN_007 steps ---
    def tc_login_007_username_recovery_flow(self, email: str):
        """
        TC_LOGIN_007 Steps:
        3. Enter registered email address
        4. Click on 'Send Username' button
        5. Verify username recovery email is received
        """
        self.enter_email(email)
        self.click_send_username()
        return self.is_success_message_displayed()
    # --- End of TC_LOGIN_007 steps ---
