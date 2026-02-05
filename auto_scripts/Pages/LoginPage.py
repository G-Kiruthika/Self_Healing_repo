# Selenium Page Object for LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    LOGIN_URL = "https://app.example.com/login"
    EMAIL_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def navigate_to_login(self):
        """
        Step 1: Navigate to the login page.
        Acceptance Criteria: Login page is displayed with email and password fields.
        """
        self.driver.get(self.LOGIN_URL)
        return self.is_login_page_displayed()

    def is_login_page_displayed(self):
        """
        Checks if login page elements are visible.
        """
        try:
            email_visible = self.driver.find_element(*self.EMAIL_INPUT).is_displayed()
            password_visible = self.driver.find_element(*self.PASSWORD_INPUT).is_displayed()
            return email_visible and password_visible
        except NoSuchElementException:
            return False

    def enter_email(self, email: str):
        """
        Step 2: Enter valid registered email in the email field.
        Acceptance Criteria: Email is accepted and displayed in the field.
        """
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)
        return email_field.get_attribute("value") == email

    def enter_password(self, password: str):
        """
        Step 3: Enter correct password in the password field.
        Acceptance Criteria: Password is masked and accepted.
        """
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        # Selenium does not expose masking, but we can check input type
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login(self):
        """
        Step 4: Click on the Login button.
        Acceptance Criteria: User is successfully authenticated and redirected to dashboard.
        """
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        # Wait for dashboard header or user profile icon
        return self.is_dashboard_displayed()

    def is_dashboard_displayed(self):
        """
        Checks if dashboard page is displayed after login.
        """
        try:
            header_visible = self.driver.find_element(*self.DASHBOARD_HEADER).is_displayed()
            profile_visible = self.driver.find_element(*self.USER_PROFILE_ICON).is_displayed()
            return header_visible and profile_visible
        except NoSuchElementException:
            return False

    def verify_user_session(self):
        """
        Step 5: Verify user session is created.
        Acceptance Criteria: User session token is generated and stored, user profile is displayed.
        """
        # Session token verification is usually handled outside Selenium.
        # Here, we check for user profile display as a proxy.
        try:
            profile_icon = self.driver.find_element(*self.USER_PROFILE_ICON)
            return profile_icon.is_displayed()
        except NoSuchElementException:
            return False

    # --- End of TC_LOGIN_001 steps ---
