# LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    """
    Page Object for Login Page.
    Supports navigation, login actions, and validation of field constraints and error messages.
    """
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to(self):
        """Navigate to the login page URL."""
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

    def enter_email(self, email):
        """Enter email in the email field."""
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_overlong_email(self, base_email="user", domain="@example.com", total_length=256):
        """Enter an email exceeding the maximum allowed length (default 256 chars)."""
        max_local = total_length - len(domain)
        overlong_email = (base_email * ((max_local // len(base_email)) + 1))[:max_local] + domain
        self.enter_email(overlong_email)
        return overlong_email

    def enter_password(self, password):
        """Enter password in the password field."""
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        """Click the login button."""
        btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        btn.click()

    def is_error_message_displayed(self):
        """Check if a general error message is displayed."""
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).is_displayed()
        except TimeoutException:
            return False

    def is_email_length_error_displayed(self):
        """
        Check if an email length validation error is displayed.
        Returns True if validation error or specific error message for overlong email is shown.
        """
        try:
            validation_error = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            if validation_error.is_displayed() and ("email" in validation_error.text.lower() or "length" in validation_error.text.lower()):
                return True
        except TimeoutException:
            pass
        # Check for general error message as fallback
        try:
            error_msg = self.driver.find_element(*self.ERROR_MESSAGE)
            if error_msg.is_displayed() and ("email" in error_msg.text.lower() or "length" in error_msg.text.lower()):
                return True
        except Exception:
            pass
        return False

    def login_with_overlong_email(self, password):
        """
        Combined method for TC_LOGIN_06_02:
        1. Enter overlong email
        2. Enter password
        3. Click login
        4. Return error detection result
        """
        self.go_to()
        overlong_email = self.enter_overlong_email()
        self.enter_password(password)
        self.click_login()
        return self.is_email_length_error_displayed()

    # Existing methods below (if any)...
