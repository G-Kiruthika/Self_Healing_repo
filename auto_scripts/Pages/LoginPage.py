from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    WebDriverException
)

class LoginPage:
    '''
    Page Object for the Login Page.
    Implements methods for login scenarios and navigation to password recovery.
    '''

    # Locators from Locators.json
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[contains(text(),'Mandatory fields are required')]")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login_with_credentials(self, email, password):
        '''
        Logs in using provided credentials.
        '''
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD)).clear()
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD)).clear()
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
        self.driver.find_element(*self.LOGIN_SUBMIT_BUTTON).click()

    def click_forgot_password(self):
        '''
        Clicks the forgot password link.
        '''
        self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK)).click()

    def is_error_message_displayed(self):
        '''
        Checks if the error message is displayed.
        '''
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.is_displayed()
        except TimeoutException:
            return False

    def is_validation_error_displayed(self):
        '''
        Checks if the validation error message is displayed.
        '''
        try:
            validation_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return validation_elem.is_displayed()
        except TimeoutException:
            return False

    def login_with_invalid_email_format(self, invalid_email, valid_password):
        '''
        TC_LOGIN_002: Attempts login with invalid email format and valid password, expects validation error message.
        Args:
            invalid_email (str): Invalid email format (e.g., 'userexample.com')
            valid_password (str): Valid password (e.g., 'ValidPass123')
        Returns:
            bool: True if validation error for invalid email is displayed, False otherwise.
        '''
        self.driver.get(self.URL)
        try:
            # Enter invalid email
            email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_input.clear()
            email_input.send_keys(invalid_email)
            # Enter valid password
            password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_input.clear()
            password_input.send_keys(valid_password)
            # Click Login
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
            # Wait for validation error
            validation_error = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return validation_error.is_displayed()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException):
            return False
