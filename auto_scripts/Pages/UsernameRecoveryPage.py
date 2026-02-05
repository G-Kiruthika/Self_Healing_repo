# Selenium Page Object for UsernameRecoveryPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UsernameRecoveryPage:
    LOGIN_PAGE_URL = "https://app.example.com/login"  # For TC_LOGIN_009 navigation
    LOGIN_FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")  # Reused as no specific 'forgot username' locator provided
    USERNAME_RECOVERY_URL = "https://ecommerce.example.com/forgot-username"  # Existing
    EMAIL_INPUT = (By.ID, "username-recovery-email")
    SEND_USERNAME_BUTTON = (By.ID, "send-username")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.recovery-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.recovery-error")
    INSTRUCTIONS = (By.CSS_SELECTOR, "div.instructions")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_login_page(self):
        """
        Step 1: Navigate to the login page
        """
        self.driver.get(self.LOGIN_PAGE_URL)
        # Optionally wait for the page to load
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_FORGOT_USERNAME_LINK))

    def click_forgot_username_link(self):
        """
        Step 2: Click on 'Forgot Username' link
        """
        link = self.wait.until(EC.element_to_be_clickable(self.LOGIN_FORGOT_USERNAME_LINK))
        link.click()
        # Optionally wait for navigation to username recovery page
        self.wait.until(lambda d: self.USERNAME_RECOVERY_URL in d.current_url)

    def is_loaded(self):
        """Verify username recovery page is loaded by checking URL and main elements."""
        try:
            correct_url = self.driver.current_url.startswith(self.USERNAME_RECOVERY_URL)
            email_visible = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)).is_displayed()
            send_button_visible = self.wait.until(EC.visibility_of_element_located(self.SEND_USERNAME_BUTTON)).is_displayed()
            instructions_visible = self.driver.find_element(*self.INSTRUCTIONS).is_displayed() if self.driver.find_elements(*self.INSTRUCTIONS) else True
            return correct_url and email_visible and send_button_visible and instructions_visible
        except (NoSuchElementException, TimeoutException):
            return False

    def is_email_input_visible(self):
        try:
            input_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            return input_field.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def is_send_username_button_visible(self):
        try:
            button = self.wait.until(EC.visibility_of_element_located(self.SEND_USERNAME_BUTTON))
            return button.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def enter_email(self, email: str):
        """
        Step 3: Enter registered email address
        """
        input_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        input_field.clear()
        input_field.send_keys(email)
        return input_field.get_attribute("value") == email

    def click_send_username(self):
        """
        Step 4: Click on 'Submit' button
        """
        button = self.wait.until(EC.element_to_be_clickable(self.SEND_USERNAME_BUTTON))
        button.click()

    def is_success_message_displayed(self):
        """
        Step 5: Success message displayed: 'Username sent to your email'
        """
        try:
            success = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return success.is_displayed() and 'Username sent to your email' in success.text
        except (NoSuchElementException, TimeoutException):
            return False

    def is_error_message_displayed(self):
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.is_displayed()
        except (NoSuchElementException, TimeoutException):
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

    # --- Start of TC_LOGIN_009 steps ---
    def tc_login_009_forgot_username_flow(self, email: str):
        """
        TC_LOGIN_009 Steps:
        1. Navigate to the login page
        2. Click on 'Forgot Username' link
        3. Enter registered email address
        4. Click on Submit button
        5. Success message displayed and username reminder email sent
        """
        self.navigate_to_login_page()
        self.click_forgot_username_link()
        self.enter_email(email)
        self.click_send_username()
        return self.is_success_message_displayed()
    # --- End of TC_LOGIN_009 steps ---
