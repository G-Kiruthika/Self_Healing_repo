# RegistrationPage.py
# Selenium PageClass for User Registration
# Generated for Test Case TC-001
# Maintainer: G-Kiruthika

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegistrationPage:
    """
    Page Object Model for the Registration Page.
    Implements best practices for Selenium Python automation:
    - Explicit waits
    - DRY principle
    - Strict locator validation
    - Clear method naming
    """

    # Locators (update as per Locators.json/locators.json when available)
    REGISTRATION_URL = "https://example-ecommerce.com/register"
    EMAIL_INPUT = (By.ID, "register-email")
    PASSWORD_INPUT = (By.ID, "register-password")
    NAME_INPUT = (By.ID, "register-name")
    SUBMIT_BUTTON = (By.ID, "register-submit")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.alert-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_registration_page(self):
        """Navigate to the registration page."""
        self.driver.get(self.REGISTRATION_URL)
        assert self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)), "Registration page not displayed."

    def enter_registration_details(self, email, password, name):
        """Enter email, password, and name into registration fields."""
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        name_field = self.wait.until(EC.visibility_of_element_located(self.NAME_INPUT))

        email_field.clear()
        email_field.send_keys(email)
        password_field.clear()
        password_field.send_keys(password)
        name_field.clear()
        name_field.send_keys(name)

    def submit_registration(self):
        """Submit the registration form."""
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()

    def verify_registration_success(self):
        """Verify registration was successful."""
        # Check for success message and HTTP response code (if available via API or logs)
        success = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
        assert "account created" in success.text.lower() or "201 created" in success.text.lower(), "Registration failed or incorrect response."

    def verify_error_message(self):
        """Verify error message is displayed if registration fails."""
        error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return error.text

