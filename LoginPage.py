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

    def load(self):
        self.driver.get(self.URL)

    def is_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD)) and \
               self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))

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
        except:
            return None

    def get_validation_error(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR)).text
        except:
            return None

    def get_empty_field_prompt(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT)).text
        except:
            return None

    def is_dashboard_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.DASHBOARD_HEADER))

    def is_user_profile_icon_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.USER_PROFILE_ICON))
