from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    LOGIN_URL = "https://example-ecommerce.com/login"
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

    def navigate_to_login_screen(self):
        self.driver.get(self.LOGIN_URL)
        # Wait for email field to be present
        self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
        self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))
        self.wait.until(EC.presence_of_element_located(self.LOGIN_SUBMIT))
        return self.is_login_screen_displayed()

    def is_login_screen_displayed(self) -> bool:
        try:
            email_present = self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
            password_present = self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))
            submit_present = self.wait.until(EC.presence_of_element_located(self.LOGIN_SUBMIT))
            return email_present is not None and password_present is not None and submit_present is not None
        except Exception:
            return False

    def enter_credentials(self, username: str, password: str):
        email_elem = self.driver.find_element(*self.EMAIL_FIELD)
        password_elem = self.driver.find_element(*self.PASSWORD_FIELD)
        email_elem.clear()
        email_elem.send_keys(username)
        password_elem.clear()
        password_elem.send_keys(password)

    def submit_login(self):
        submit_btn = self.driver.find_element(*self.LOGIN_SUBMIT)
        submit_btn.click()

    def login_with_invalid_credentials(self, username: str, password: str):
        self.enter_credentials(username, password)
        self.submit_login()

    def get_error_message(self) -> str:
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text.strip()
        except Exception:
            return ""

    def verify_invalid_login_error(self, expected_message: str) -> bool:
        actual_message = self.get_error_message()
        return actual_message == expected_message
