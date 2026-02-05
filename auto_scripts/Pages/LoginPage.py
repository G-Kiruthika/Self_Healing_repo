# LoginPage.py
"""
Page Object Model for the Login Page.
Auto-generated/updated for TC_LOGIN_017.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for the Login Page at https://example-ecommerce.com/login
    """
    URL = "https://example-ecommerce.com/login"

    # Locators (from Locators.json)
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

    def go_to(self):
        """
        Navigates to the login page URL.
        """
        self.driver.get(self.URL)
        assert self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD)), "Login page did not load properly."

    def enter_password(self, password: str):
        """
        Enters the password into the password field.
        Args:
            password (str): The password to input.
        """
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)
        # Verify password is masked
        input_type = password_input.get_attribute("type")
        assert input_type == "password", "Password field is not masked!"

    # Existing methods (if any) should be restored here.