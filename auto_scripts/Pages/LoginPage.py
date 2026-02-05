# Selenium Page Object for LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    LOGIN_URL = "https://ecommerce.example.com/login"
    EMAIL_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_login(self, url: str = None):
        target_url = url if url else self.LOGIN_URL
        self.driver.get(target_url)
        return self.is_login_page_displayed()

    def is_login_page_displayed(self):
        try:
            email_visible = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            password_visible = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
            forgot_password_visible = self.wait.until(EC.visibility_of_element_located(self.FORGOT_PASSWORD_LINK))
            return email_visible.is_displayed() and password_visible.is_displayed() and forgot_password_visible.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def click_forgot_password(self):
        try:
            forgot_link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
            forgot_link.click()
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    # ... [Other existing methods remain unchanged] ...
