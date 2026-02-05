import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Updated URL from Locators.json
        self.url = "https://example-ecommerce.com/login"
        # Updated locators from Locators.json
        self.email_input_locator = (By.ID, "login-email")
        self.password_input_locator = (By.ID, "login-password")
        self.login_button_locator = (By.ID, "login-submit")
        self.error_message_locator = (By.CSS_SELECTOR, "div.alert-danger")
        self.validation_error_locator = (By.CSS_SELECTOR, ".invalid-feedback")

    def open_login_page(self):
        """Navigate to the login page and wait for email field."""
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.email_input_locator)
        )

    def enter_email(self, email):
        """Enter email (supports 255+ chars) using correct locator."""
        email_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_input_locator)
        )
        email_input.clear()
        email_input.send_keys(email)
        # Optionally, validate input length if needed
        if len(email) > 255:
            # Check for validation error prompt
            try:
                error = self.get_validation_error()
                if error:
                    return error
            except Exception:
                pass
        return None

    def enter_password(self, password):
        """Enter password using correct locator."""
        password_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_input_locator)
        )
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        """Click the login button using correct locator."""
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button_locator)
        )
        login_button.click()

    def get_error_message(self):
        """Retrieve main error message after login attempt."""
        try:
            error_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message_locator)
            )
            return error_element.text
        except Exception:
            return None

    def get_validation_error(self):
        """Retrieve validation error messages (e.g., invalid email length, format)."""
        try:
            validation_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.validation_error_locator)
            )
            return validation_element.text
        except Exception:
            return None

    def get_all_errors(self):
        """Retrieve both error and validation error messages for comprehensive reporting."""
        errors = []
        error_msg = self.get_error_message()
        validation_msg = self.get_validation_error()
        if error_msg:
            errors.append(error_msg)
        if validation_msg:
            errors.append(validation_msg)
        return errors
