# Selenium Page Object for LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    LOGIN_URL = "https://example-ecommerce.com/login"
    EMAIL_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def navigate_to_login(self):
        """
        Step 1: Navigate to the e-commerce website login page.
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
        Step 2: Enter valid registered email address in the email field.
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
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login(self):
        """
        Step 4: Click on the Login button.
        Acceptance Criteria: User is successfully authenticated and redirected to the dashboard/home page.
        """
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self.is_dashboard_displayed()

    def is_dashboard_displayed(self):
        """
        Checks if dashboard/home page is displayed after login.
        """
        try:
            header_visible = self.driver.find_element(*self.DASHBOARD_HEADER).is_displayed()
            profile_visible = self.driver.find_element(*self.USER_PROFILE_ICON).is_displayed()
            return header_visible and profile_visible
        except NoSuchElementException:
            return False

    def verify_user_session(self):
        """
        Step 5: Verify user session is established.
        Acceptance Criteria: User name is displayed in the header and session cookie is set.
        """
        try:
            profile_icon = self.driver.find_element(*self.USER_PROFILE_ICON)
            session_cookie = None
            for cookie in self.driver.get_cookies():
                if cookie['name'] == 'session':
                    session_cookie = cookie['value']
                    break
            return profile_icon.is_displayed() and session_cookie is not None
        except NoSuchElementException:
            return False

    # --- End of TC-LOGIN-001 steps ---

    # Existing methods for other test cases remain unchanged below this line

    # --- Start of TC_LOGIN_002 steps ---
    def enter_incorrect_password(self, password: str):
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login_and_check_error(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self.is_error_message_displayed("Invalid email or password")

    def is_error_message_displayed(self, expected_message: str):
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
    # --- End of TC_LOGIN_002 steps ---

    # --- Start of TC_LOGIN_003 steps ---
    def leave_email_field_empty(self):
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        return email_field.get_attribute("value") == ""

    def enter_valid_password(self, password: str):
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login_button(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self.is_validation_error_displayed("Email is required")

    def is_validation_error_displayed(self, expected_message: str):
        try:
            validation_elem = self.driver.find_element(*self.VALIDATION_ERROR)
            return validation_elem.is_displayed() and expected_message in validation_elem.text
        except NoSuchElementException:
            return False

    def verify_login_prevented(self):
        current_url = self.driver.current_url
        on_login_page = current_url.startswith(self.LOGIN_URL)
        dashboard_visible = self.is_dashboard_displayed()
        return on_login_page and not dashboard_visible
    # --- End of TC_LOGIN_003 steps ---

    # --- Start of TC_SCRUM74_002 steps ---
    def enter_invalid_email_format(self, email: str):
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)
        return email_field.get_attribute("value") == email

    def get_email_format_error_message(self):
        try:
            validation_elem = self.driver.find_element(*self.VALIDATION_ERROR)
            if validation_elem.is_displayed():
                return validation_elem.text
            return None
        except NoSuchElementException:
            return None

    def enter_valid_password_for_invalid_email(self, password: str):
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login_for_invalid_email(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self.is_error_message_displayed("Invalid email or username")
    # --- End of TC_SCRUM74_002 steps ---

    # --- Start of TC_SCRUM74_003 steps ---
    def enter_nonexistent_email(self, email: str):
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)
        return email_field.get_attribute("value") == email

    def enter_any_password(self, password: str):
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login_and_verify_invalid_credentials(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self.is_error_message_displayed("Invalid credentials")
    # --- End of TC_SCRUM74_003 steps ---

    # --- Start of TC_LOGIN_004 steps ---
    def enter_valid_email_leave_password_empty(self, email: str):
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        return email_field.get_attribute("value") == email and password_field.get_attribute("value") == ""

    def click_login_and_verify_password_required(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self.is_validation_error_displayed("Password is required")

    def verify_login_prevented_password_empty(self):
        current_url = self.driver.current_url
        on_login_page = current_url.startswith(self.LOGIN_URL)
        dashboard_visible = self.is_dashboard_displayed()
        return on_login_page and not dashboard_visible
    # --- End of TC_LOGIN_004 steps ---
