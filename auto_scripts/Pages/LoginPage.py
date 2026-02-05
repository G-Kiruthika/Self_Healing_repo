# Selenium Page Object for LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    LOGIN_URL = "https://example-ecommerce.com/login"
    EMAIL_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_login(self):
        self.driver.get(self.LOGIN_URL)
        return self.is_login_page_displayed()

    def is_login_page_displayed(self):
        try:
            email_visible = self.driver.find_element(*self.EMAIL_INPUT).is_displayed()
            password_visible = self.driver.find_element(*self.PASSWORD_INPUT).is_displayed()
            return email_visible and password_visible
        except NoSuchElementException:
            return False

    def enter_email(self, email: str):
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)
        return email_field.get_attribute("value") == email

    def enter_password(self, password: str):
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return True

    def is_error_message_displayed(self, expected_message: str = "Invalid email or password"):
        try:
            error_elem = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_elem.is_displayed() and expected_message in error_elem.text
        except NoSuchElementException:
            return False

    def verify_user_stays_on_login_page(self):
        current_url = self.driver.current_url
        on_login_page = current_url.startswith(self.LOGIN_URL)
        dashboard_visible = self.is_dashboard_displayed()
        return on_login_page and not dashboard_visible

    def is_dashboard_displayed(self):
        try:
            header_visible = self.driver.find_element(*self.DASHBOARD_HEADER).is_displayed()
            profile_visible = self.driver.find_element(*self.USER_PROFILE_ICON).is_displayed()
            return header_visible and profile_visible
        except NoSuchElementException:
            return False

    # --- TC-LOGIN-002 Test Steps Implementation ---
    def tc_login_002_invalid_login_flow(self, email: str, password: str):
        """
        1. Navigate to the login page
        2. Enter an unregistered or invalid email address
        3. Enter any password
        4. Click on the Login button
        5. Verify error message: 'Invalid email or password'
        6. Verify user remains on login page
        """
        self.navigate_to_login()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        error_displayed = self.is_error_message_displayed("Invalid email or password")
        user_stays = self.verify_user_stays_on_login_page()
        return error_displayed and user_stays

    # --- TC-LOGIN-008 Test Steps Implementation ---
    def tc_login_008_unregistered_email_login_flow(self, url: str, email: str, password: str, expected_error: str = "Invalid email or password"):
        """
        TC_LOGIN_008: Login attempt with unregistered email
        Steps:
        1. Navigate to the login page [Test Data: URL]
        2. Enter unregistered email address [Test Data: Email]
        3. Enter any password [Test Data: Password]
        4. Click on the Login button
        5. Verify error message displayed: 'Invalid email or password'
        6. Verify user remains on login page
        Acceptance Criteria: AC_008
        """
        self.driver.get(url)
        login_page_displayed = self.is_login_page_displayed()
        if not login_page_displayed:
            return False
        email_entered = self.enter_email(email)
        password_entered = self.enter_password(password)
        self.click_login()
        error_displayed = self.is_error_message_displayed(expected_error)
        user_stays = self.verify_user_stays_on_login_page()
        return all([login_page_displayed, email_entered, password_entered, error_displayed, user_stays])

    # --- TC-LOGIN-003 Test Steps Implementation ---
    def tc_login_003_valid_email_wrong_password(self, url: str = "https://ecommerce.example.com/login", email: str = "testuser@example.com", password: str = "WrongPassword456", expected_error: str = "Invalid email or password"):
        """
        TC-LOGIN-003: Login attempt with valid registered email and incorrect password
        Steps:
        1. Navigate to the login page [Test Data: URL]
        2. Enter valid registered email address [Test Data: Email]
        3. Enter incorrect password [Test Data: Password]
        4. Click on the Login button
        5. Verify error message displayed: 'Invalid email or password'
        6. Verify user remains on login page without authentication
        Acceptance Criteria: TS-002
        """
        self.driver.get(url)
        login_page_displayed = self.is_login_page_displayed()
        if not login_page_displayed:
            return False
        email_entered = self.enter_email(email)
        password_entered = self.enter_password(password)
        self.click_login()
        error_displayed = self.is_error_message_displayed(expected_error)
        user_stays = self.verify_user_stays_on_login_page()
        # Ensure no session is created (additional check can be added if session/cookie logic is implemented)
        return all([
            login_page_displayed,
            email_entered,
            password_entered,
            error_displayed,
            user_stays
        ])
