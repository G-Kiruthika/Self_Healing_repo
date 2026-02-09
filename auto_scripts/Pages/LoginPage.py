from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional

class LoginPage:
    """
    Page Object for Login Page functionality.
    Implements locators and actions for login workflows including invalid login validation.
    """
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to_login_page(self):
        """Navigate to the login page and wait for email field."""
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

    def enter_email(self, email: str):
        """Enter email into email field."""
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password: str):
        """Enter password into password field."""
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        """Click the login submit button."""
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_btn.click()

    def click_forgot_username(self):
        """Click the 'Forgot Username' link."""
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK))
        link.click()

    def get_error_message(self) -> Optional[str]:
        """Return error message text if present."""
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return None

    def is_on_login_page(self) -> bool:
        """Verify if user is on login page."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            return True
        except Exception:
            return False

    def login_with_credentials(self, email: str, password: str):
        """Perform login with provided credentials."""
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def perform_invalid_login_and_validate(self, email: str, invalid_password: str):
        """
        TC_LOGIN_001: Performs invalid login and validates error message.
        Steps:
            1. Navigate to the login screen.
            2. Enter invalid username and/or password.
            3. Click Login button.
            4. Validate error message 'Invalid username or password. Please try again.' is displayed.
            5. Assert user remains on login page after failed login.
        Args:
            email (str): Invalid email/username.
            invalid_password (str): Invalid password.
        Raises:
            AssertionError: If error message is not as expected or user is not on login page.
        """
        expected_error = "Invalid username or password. Please try again."
        self.login_with_credentials(email, invalid_password)
        error_msg = self.get_error_message()
        assert error_msg is not None, "Error message not found after invalid login."
        assert error_msg.strip() == expected_error, f"Expected error '{expected_error}', got '{error_msg.strip()}'"
        assert self.is_on_login_page(), "User is not on the login page after failed login."