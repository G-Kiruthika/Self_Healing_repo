# LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def login_with_email_and_password(self, email, password, remember_me=False):
        self.driver.get(self.URL)
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_field.clear()
        email_field.send_keys(email)
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(password)
        if remember_me:
            remember_checkbox = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
            if not remember_checkbox.is_selected():
                remember_checkbox.click()
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_button.click()

    def is_dashboard_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except Exception:
            return False

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return None

    def verify_invalid_login_shows_error(self, invalid_email, invalid_password):
        """
        Automates TC_LOGIN_001: Attempts login with invalid credentials and asserts the correct error message is shown.

        Steps:
            1. Navigates to the login screen.
            2. Enters invalid username and password.
            3. Clicks the login button.
            4. Asserts the error message is displayed with the text:
               'Invalid username or password. Please try again.'

        Args:
            invalid_email (str): The invalid email/username to use.
            invalid_password (str): The invalid password to use.

        Raises:
            AssertionError: If the error message is not displayed or does not match the expected text.
        """
        # Step 1: Navigate to login page
        self.driver.get(self.URL)

        # Step 2: Enter invalid credentials
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_field.clear()
        email_field.send_keys(invalid_email)

        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(invalid_password)

        # Step 3: Click the login button
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_button.click()

        # Step 4: Assert error message is shown with correct text
        expected_error = "Invalid username or password. Please try again."
        error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        actual_error = error_elem.text.strip()
        assert actual_error == expected_error, (
            f"Expected error message '{expected_error}', but got '{actual_error}'"
        )

    def verify_remember_me_checkbox_absence(self):
        """
        Automates TC_LOGIN_002: Verifies that the 'Remember Me' checkbox is NOT present on the login screen.

        Steps:
            1. Navigates to the login screen.
            2. Checks for the absence of the 'Remember Me' checkbox.

        Returns:
            bool: True if the checkbox is NOT present, False otherwise.
        """
        self.driver.get(self.URL)
        try:
            # Short explicit wait for absence
            self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
            # If found, it's present
            return False
        except Exception:
            # If NoSuchElementException or any exception, treat as absent
            return True
