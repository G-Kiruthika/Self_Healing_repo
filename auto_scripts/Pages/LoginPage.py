# LoginPage.py
"""
Page Object for Login Page using Selenium WebDriver
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
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
    ACCOUNT_LOCKED_MESSAGE = (By.XPATH, "//*[contains(text(), 'Account locked due to multiple failed login attempts')]")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get(self.URL)

    def is_displayed(self):
        try:
            email_displayed = self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
            password_displayed = self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))
            return email_displayed and password_displayed
        except TimeoutException:
            return False

    def enter_email(self, email):
        email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password):
        password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        login_btn.click()

    def get_error_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
        except TimeoutException:
            return None

    def get_validation_error(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR)).text
        except TimeoutException:
            return None

    def get_empty_field_prompt(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT)).text
        except TimeoutException:
            return None

    def is_dashboard_displayed(self):
        try:
            return self.wait.until(EC.presence_of_element_located(self.DASHBOARD_HEADER))
        except TimeoutException:
            return False

    def is_user_profile_icon_displayed(self):
        try:
            return self.wait.until(EC.presence_of_element_located(self.USER_PROFILE_ICON))
        except TimeoutException:
            return False

    def is_account_locked(self):
        """
        Returns True if the account lockout message is displayed after multiple failed login attempts.
        """
        try:
            lockout_message = self.wait.until(
                EC.visibility_of_element_located(self.ACCOUNT_LOCKED_MESSAGE)
            )
            return lockout_message is not None
        except TimeoutException:
            return False

    def get_account_locked_message(self):
        """
        Returns the account lockout message text if present.
        """
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.ACCOUNT_LOCKED_MESSAGE)
            ).text
        except TimeoutException:
            return None

    def attempt_login(self, email, password, attempts=1):
        """
        Attempts to login multiple times and checks for account lockout after failed attempts.
        Returns a tuple (locked: bool, last_error: str)
        """
        last_error = None
        for attempt in range(attempts):
            self.enter_email(email)
            self.enter_password(password)
            self.click_login()
            # Wait for error message or lockout
            error = self.get_error_message()
            if self.is_account_locked():
                return True, self.get_account_locked_message()
            last_error = error
        return False, last_error
