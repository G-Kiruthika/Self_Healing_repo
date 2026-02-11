import re
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    """
    Page Object Model for the Login Page of example-ecommerce.com
    Handles login functionality, including emails with special characters, and all acceptance criteria for TC_LOGIN_009.
    """
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[contains(text(), 'Mandatory fields are required')]")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def load(self) -> None:
        """Navigate to the login page URL."""
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

    def enter_email(self, email: str) -> None:
        """Enter the email address, supporting special characters as per TC_LOGIN_009."""
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password: str) -> None:
        """Enter the password into the password field."""
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self) -> None:
        """Click the Login button to submit credentials."""
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        login_btn.click()

    def is_login_successful(self) -> bool:
        """Check for successful login by verifying dashboard header or user profile icon."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except TimeoutException:
            return False

    def get_error_message(self) -> str:
        """Retrieve any login error message displayed."""
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.text.strip()
        except TimeoutException:
            return ""

    def get_validation_error(self) -> str:
        """Retrieve inline validation error (e.g., for email format)."""
        try:
            validation = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return validation.text.strip()
        except TimeoutException:
            return ""

    def is_empty_field_prompt_displayed(self) -> bool:
        """Check if the mandatory fields prompt is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return True
        except TimeoutException:
            return False

    @staticmethod
    def is_valid_email_format(email: str) -> bool:
        """Validate email format, allowing special characters as per RFC 5322."""
        # This regex supports most valid email formats including special characters.
        pattern = r"(^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)"
        return re.match(pattern, email) is not None
