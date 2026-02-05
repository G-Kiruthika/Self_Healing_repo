# LoginPage.py
"""
Page Object for Login Page using Selenium WebDriver
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_login(self):
        """Navigate to the login page."""
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

    def enter_email(self, email: str):
        """Enter email into the email field."""
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password: str):
        """Enter password into the password field."""
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def click_remember_me(self):
        """Click the 'Remember Me' checkbox."""
        checkbox = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
        checkbox.click()

    def click_login(self):
        """Click the login submit button."""
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        login_btn.click()

    def click_forgot_password(self):
        """Click the 'Forgot Password' link."""
        forgot_link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        forgot_link.click()

    def get_error_message(self) -> str:
        """Get the error message displayed after failed login."""
        error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return error_elem.text

    def get_validation_error(self) -> str:
        """Get the validation error message displayed for invalid input."""
        validation_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
        return validation_elem.text

    def is_empty_field_prompt_displayed(self) -> bool:
        """Check if the empty field prompt is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return True
        except:
            return False

    def is_dashboard_displayed(self) -> bool:
        """Check if dashboard header is displayed after login."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except:
            return False

    def is_user_profile_icon_displayed(self) -> bool:
        """Check if user profile icon is displayed after login."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except:
            return False

    # --- TC_LOGIN_005 ---
    def login_with_empty_username(self, password: str) -> str:
        """
        Execute TC_LOGIN_005:
        1. Navigate to login page
        2. Leave username field empty
        3. Enter valid password
        4. Click Login
        5. Return validation error message for empty username
        """
        self.navigate_to_login()
        # Leave email field empty (do not enter anything)
        self.enter_password(password)
        self.click_login()
        # Wait for validation error message specific to username
        try:
            validation_error = self.wait.until(
                EC.visibility_of_element_located(self.VALIDATION_ERROR)
            )
            return validation_error.text
        except:
            # Optionally, check for empty field prompt if standard validation error not found
            if self.is_empty_field_prompt_displayed():
                prompt_elem = self.driver.find_element(*self.EMPTY_FIELD_PROMPT)
                return prompt_elem.text
            return "Validation error not found"
