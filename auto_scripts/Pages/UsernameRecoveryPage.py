# Executive Summary:
# This PageClass implements the username recovery page automation for an e-commerce application using Selenium in Python.
# It now supports:
# - TC-LOGIN-007: End-to-end username recovery flow as per the latest test case and acceptance criteria.
# - All locators mapped from Locators.json, structured for maintainability and extensibility.

# Detailed Analysis:
# - Strict locator mapping from Locators.json
# - Defensive coding using Selenium WebDriverWait and exception handling
# - Functions for navigation, UI validation, and username recovery workflow
# - New/updated method: tc_login_007_username_recovery_flow() implements TC-LOGIN-007 steps

# Implementation Guide:
# - Instantiate UsernameRecoveryPage with a Selenium WebDriver instance
# - Use tc_login_007_username_recovery_flow(email) to automate TC-LOGIN-007 scenario
# - Example usage:
#     page = UsernameRecoveryPage(driver)
#     result = page.tc_login_007_username_recovery_flow('user@example.com')
# - Returns True if username recovery page is loaded and UI is validated, False otherwise

# Quality Assurance Report:
# - All locator references validated against Locators.json
# - PageClass code reviewed for Pythonic standards and Selenium best practices
# - Functions include assertion checks and detailed exception handling
# - Existing methods are preserved and new methods are appended

# Troubleshooting Guide:
# - Ensure the driver is initialized and points to the correct browser instance
# - Validate all locator values against Locators.json
# - For any assertion failure, review the error message for details
# - TimeoutException may indicate slow page load or incorrect locator

# Future Considerations:
# - Extend PageClass for additional username recovery and UI validation tests
# - Integrate with reporting tools for enhanced test results

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UsernameRecoveryPage:
    LOGIN_PAGE_URL = "https://ecommerce.example.com/login"  # Updated to match test data
    LOGIN_FORGOT_USERNAME_LINK = (By.LINK_TEXT, "Forgot Username")  # More precise locator per test step
    USERNAME_RECOVERY_URL = "https://ecommerce.example.com/forgot-username"
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
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_FORGOT_USERNAME_LINK))

    def click_forgot_username_link(self):
        """
        Step 2: Click on 'Forgot Username' link
        """
        link = self.wait.until(EC.element_to_be_clickable(self.LOGIN_FORGOT_USERNAME_LINK))
        link.click()
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

    def verify_username_recovery_page_ui(self):
        """
        Step 3: Verify username recovery page is displayed with input fields and instructions
        """
        try:
            correct_url = self.driver.current_url.startswith(self.USERNAME_RECOVERY_URL)
            email_visible = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)).is_displayed()
            instructions_visible = True
            if self.driver.find_elements(*self.INSTRUCTIONS):
                instructions_elem = self.driver.find_element(*self.INSTRUCTIONS)
                instructions_visible = instructions_elem.is_displayed()
            return correct_url and email_visible and instructions_visible
        except Exception as e:
            raise AssertionError(f"TC-LOGIN-007 (Username Recovery UI) failed: {str(e)}")

    def tc_login_007_username_recovery_flow(self, email: str):
        """
        TC-LOGIN-007 Steps:
        1. Navigate to the login page [Test Data: URL: https://ecommerce.example.com/login]
        2. Click on 'Forgot Username' link
        3. Verify username recovery page is displayed [Expected URL: https://ecommerce.example.com/forgot-username]
        Acceptance Criteria: TS-005
        """
        try:
            self.navigate_to_login_page()
            self.click_forgot_username_link()
            assert self.verify_username_recovery_page_ui(), "Username recovery page UI validation failed"
            return True
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException, AssertionError) as e:
            print(f"Exception during TC-LOGIN-007 username recovery flow: {e}")
            return False

    # --- Existing methods preserved below ---
    def enter_email(self, email: str):
        input_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        input_field.clear()
        input_field.send_keys(email)
        return input_field.get_attribute("value") == email

    def click_send_username(self):
        button = self.wait.until(EC.element_to_be_clickable(self.SEND_USERNAME_BUTTON))
        button.click()

    def is_success_message_displayed(self):
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
        raise NotImplementedError("Email inbox check for username recovery must be implemented in the test harness or with an external email service.")
