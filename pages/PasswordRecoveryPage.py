import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class PasswordRecoveryPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators (replace with values from Locators.json if available)
        self.forgot_password_url = "https://your-app-url.com/forgot-password"  # Replace with actual URL
        self.email_field = (By.ID, "recoveryEmail")
        self.submit_button = (By.ID, "submitRecovery")
        self.success_message = (By.ID, "successMsg")

    def open_forgot_password_page(self):
        self.driver.get(self.forgot_password_url)

    def enter_email(self, email):
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.email_field)
        )
        email_input.clear()
        email_input.send_keys(email)

    def submit_recovery(self):
        submit_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.submit_button)
        )
        submit_btn.click()

    def get_success_message(self):
        try:
            success = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.success_message)
            )
            return success.text
        except TimeoutException:
            return None

    # TC008: Test forgot password flow
    def forgot_password_flow_tc008(self, email="user@example.com"):
        """
        Steps:
        1. Open forgot password page
        2. Enter registered email and submit
        3. Verify success message and password reset email sent
        Returns dict with results of each step.
        """
        results = {}
        self.open_forgot_password_page()
        results['page_opened'] = self.driver.current_url == self.forgot_password_url
        self.enter_email(email)
        self.submit_recovery()
        time.sleep(1)  # Wait for success message
        success_msg = self.get_success_message()
        results['success_message_displayed'] = success_msg is not None and 'password reset email sent' in success_msg.lower()
        results['success_message_text'] = success_msg
        # Downstream validation may check for email delivery in integration
        return results
