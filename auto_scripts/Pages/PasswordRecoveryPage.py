# Selenium Page Object for PasswordRecoveryPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PasswordRecoveryPage:
    PASSWORD_RECOVERY_URL = "https://ecommerce.example.com/forgot-password"
    EMAIL_INPUT = (By.ID, "recovery-email")
    SUBMIT_BUTTON = (By.ID, "recovery-submit")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.recovery-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.recovery-error")
    GENERIC_MESSAGE = (By.CSS_SELECTOR, "div.recovery-success")  # Assuming generic message is shown in success div

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def is_loaded(self):
        try:
            correct_url = self.driver.current_url.startswith(self.PASSWORD_RECOVERY_URL)
            email_visible = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)).is_displayed()
            instructions_visible = self.driver.find_element(By.CSS_SELECTOR, "div.instructions").is_displayed() if self.driver.find_elements(By.CSS_SELECTOR, "div.instructions") else True
            return correct_url and email_visible and instructions_visible
        except (NoSuchElementException, TimeoutException):
            return False

    def is_email_input_visible(self):
        try:
            input_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            return input_field.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    # --- Start of TC_LOGIN_006 steps ---
    def tc_login_006_forgot_password_flow(self, email: str) -> bool:
        """
        TC_LOGIN_006: Forgot Password Flow
        1. Verify Password Recovery Page is loaded
        2. Enter registered email address [Test Data: Email: testuser@example.com]
        3. Click on 'Send Reset Link' button
        4. Verify success message: 'Password reset link sent to your email'
        5. Verify password reset email is received (external integration required)
        """
        assert self.is_loaded(), "Password Recovery page is not loaded"
        input_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        input_field.clear()
        input_field.send_keys(email)
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()
        try:
            success = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            assert success.is_displayed(), "Success message not displayed after reset link sent"
            assert "Password reset link sent to your email" in success.text, f"Unexpected success message: {success.text}"
        except Exception as e:
            raise AssertionError(f"Success message validation failed: {e}")
        # Step 5: Email verification (to be implemented in external test harness)
        # Example placeholder:
        # assert self.verify_password_reset_email_received(email), "Password reset email not received"
        return True
    # --- End of TC_LOGIN_006 steps ---

    def verify_password_reset_email_received(self, email: str) -> bool:
        """
        Step 5: Verify password reset email is received
        Note: This is a placeholder for integration with email checking service.
        Returns True if password reset email is received with valid reset link.
        """
        # In a real implementation, integrate with a test email inbox or use a mock service
        raise NotImplementedError("Email inbox check for password reset must be implemented in the test harness or with an external email service.")

    # --- Start of TC_LOGIN_008 steps ---
    def tc_login_008_forgot_password_unregistered_email(self, email: str) -> bool:
        """
        TC_LOGIN_008: Forgot Password with Unregistered Email

        Steps:
        1. Verify Password Recovery Page is loaded
        2. Enter unregistered email address [Test Data: Email: unregistered@example.com]
        3. Click on Submit button
        4. Verify generic message: 'If email exists, reset link will be sent'

        Returns:
            bool: True if the generic message is displayed as expected, raises AssertionError otherwise.
        """
        assert self.is_loaded(), "Password Recovery page is not loaded"
        input_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        input_field.clear()
        input_field.send_keys(email)
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()
        try:
            generic_message = self.wait.until(EC.visibility_of_element_located(self.GENERIC_MESSAGE))
            assert generic_message.is_displayed(), "Generic message not displayed after submitting unregistered email"
            assert "If email exists, reset link will be sent" in generic_message.text, f"Unexpected generic message: {generic_message.text}"
        except Exception as e:
            raise AssertionError(f"Generic message validation failed: {e}")
        return True
    # --- End of TC_LOGIN_008 steps ---
