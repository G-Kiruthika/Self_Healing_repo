# LoginPage.py
"""
Page Object for Login Page
Updated to include TC-SCRUM-115-002: Validation for invalid username and error message handling.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class LoginPage:
    """
    Page class for the Login Page.
    """
    LOGIN_URL = "https://ecommerce.example.com/login"
    USERNAME_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open_login_page(self):
        """Navigate to the login page."""
        self.driver.get(self.LOGIN_URL)

    def enter_username(self, username: str):
        """Enter username in the username field."""
        username_field = self.driver.find_element(*self.USERNAME_INPUT)
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password: str):
        """Enter password in the password field."""
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        """Click the login button."""
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self) -> str:
        """Return the error message text if present."""
        try:
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error.text
        except (NoSuchElementException, TimeoutException):
            return ""

    def login_with_invalid_username_and_validate_error(self, username: str, password: str, expected_error: str) -> bool:
        """
        TC-SCRUM-115-002: Test invalid/non-existent username login scenario.
        Steps:
        1. Navigate to the login page.
        2. Enter invalid/non-existent username.
        3. Enter valid password.
        4. Click Login.
        5. Verify error message and that user remains on the login page.
        Returns True if error message matches and user is not authenticated.
        """
        self.open_login_page()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        error_msg = self.get_error_message()
        current_url = self.driver.current_url
        fields_preserved = self.driver.find_element(*self.USERNAME_INPUT).get_attribute("value") == username and self.driver.find_element(*self.PASSWORD_INPUT).get_attribute("value") == ""
        error_match = error_msg.strip() == expected_error.strip()
        on_login_page = current_url.endswith("/login")
        return error_match and on_login_page
