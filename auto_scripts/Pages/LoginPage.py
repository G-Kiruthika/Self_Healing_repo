# LoginPage.py
"""
Page Object for Login Page
Updated to include TC_LOGIN_004: Validation when username and password are empty.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page class for the Login Page.
    """
    LOGIN_URL = "https://app.example.com/login"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Locators loaded from Locators.json (assumed structure)
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "loginBtn")
        self.error_message = (By.XPATH, "//div[@class='error-message']")

    def open_login_page(self):
        """Navigate to the login page."""
        self.driver.get(self.LOGIN_URL)

    def login(self, username: str, password: str):
        """Perform standard login."""
        self.driver.find_element(*self.username_input).clear()
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self) -> str:
        """Return the error message text if present."""
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message)
            )
            return error.text
        except Exception:
            return ""

    def validate_empty_fields_error(self) -> bool:
        """
        TC_LOGIN_004: Validates error when both username and password are empty.
        Steps:
        1. Open login page.
        2. Leave username and password empty.
        3. Click Login.
        4. Verify error message 'Username and password are required'.
        Returns True if validation error is present and correct, else False.
        """
        self.open_login_page()
        # Ensure fields are empty
        self.driver.find_element(*self.username_input).clear()
        self.driver.find_element(*self.password_input).clear()
        # Click login
        self.driver.find_element(*self.login_button).click()
        # Validate error
        expected_error = "Username and password are required"
        actual_error = self.get_error_message()
        return actual_error.strip() == expected_error
