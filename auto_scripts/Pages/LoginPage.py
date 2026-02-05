# Selenium Page Object for LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    LOGIN_URL = "https://app.example.com/login"
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
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login(self):
        """
        Step 4: Click on the Login button.
        Acceptance Criteria: User is successfully authenticated and redirected to dashboard.
        """
        self.driver.find_element(*self.LOGIN_BUTTON).click()
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
        try:
            profile_icon = self.driver.find_element(*self.USER_PROFILE_ICON)
            return profile_icon.is_displayed()
        except NoSuchElementException:
            return False

    # --- End of TC_LOGIN_001 steps ---

    # --- Start of TC_LOGIN_002 steps ---
    def enter_incorrect_password(self, password: str):
        """
        Step 3: Enter incorrect password in the password field.
        Acceptance Criteria: Password is masked and accepted for submission.
        """
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login_and_check_error(self):
        """
        Step 4: Click on the Login button and verify error message.
        Acceptance Criteria: Error message 'Invalid email or password' is displayed.
        """
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self.is_error_message_displayed("Invalid email or password")

    def is_error_message_displayed(self, expected_message: str):
        """
        Checks if the error message is displayed and matches expected text.
        """
        try:
            error_elem = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_elem.is_displayed() and expected_message in error_elem.text
        except NoSuchElementException:
            return False

    def verify_user_stays_on_login_page(self):
        """
        Step 5: Verify user remains on login page after failed login.
        Acceptance Criteria: User is not authenticated and stays on login page.
        """
        current_url = self.driver.current_url
        on_login_page = current_url.startswith(self.LOGIN_URL)
        dashboard_visible = self.is_dashboard_displayed()
        return on_login_page and not dashboard_visible
    # --- End of TC_LOGIN_002 steps ---

    # --- Start of TC_LOGIN_003 steps ---
    def leave_email_field_empty(self):
        """
        Step 2: Leave email field empty.
        Acceptance Criteria: Email field remains empty.
        """
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        return email_field.get_attribute("value") == ""

    def enter_valid_password(self, password: str):
        """
        Step 3: Enter valid password.
        Acceptance Criteria: Password is masked and accepted.
        """
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login_button(self):
        """
        Step 4: Click on the Login button when email field is empty.
        Acceptance Criteria: Validation error displayed: 'Email is required'.
        """
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self.is_validation_error_displayed("Email is required")

    def is_validation_error_displayed(self, expected_message: str):
        """
        Checks if the validation error message for empty email is displayed.
        """
        try:
            validation_elem = self.driver.find_element(*self.VALIDATION_ERROR)
            return validation_elem.is_displayed() and expected_message in validation_elem.text
        except NoSuchElementException:
            return False

    def verify_login_prevented(self):
        """
        Step 5: Verify login is prevented and user remains on login page.
        Acceptance Criteria: User cannot proceed, remains on login page.
        """
        current_url = self.driver.current_url
        on_login_page = current_url.startswith(self.LOGIN_URL)
        dashboard_visible = self.is_dashboard_displayed()
        return on_login_page and not dashboard_visible
    # --- End of TC_LOGIN_003 steps ---

    # --- Start of TC_SCRUM74_002 steps ---
    def enter_invalid_email_format(self, email: str):
        """
        Step 2: Enter invalid email format in the email/username field.
        Acceptance Criteria: Invalid email format error message is displayed.
        """
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)
        return email_field.get_attribute("value") == email

    def get_email_format_error_message(self):
        """
        Step 2: Retrieve invalid email format error message.
        Acceptance Criteria: Invalid email format error message is displayed.
        """
        try:
            validation_elem = self.driver.find_element(*self.VALIDATION_ERROR)
            if validation_elem.is_displayed():
                return validation_elem.text
            return None
        except NoSuchElementException:
            return None

    def enter_valid_password_for_invalid_email(self, password: str):
        """
        Step 3: Enter valid password (for invalid email scenario).
        Acceptance Criteria: Password is accepted.
        """
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login_for_invalid_email(self):
        """
        Step 4: Click on the Login button (invalid email scenario).
        Acceptance Criteria: Login fails with error message 'Invalid email or username'.
        """
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self.is_error_message_displayed("Invalid email or username")
    # --- End of TC_SCRUM74_002 steps ---

    # --- Start of TC_SCRUM74_003 steps ---
    def enter_nonexistent_email(self, email: str):
        """
        Step 2: Enter non-existent email in the email field.
        Acceptance Criteria: Email is accepted in the field.
        """
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)
        return email_field.get_attribute("value") == email

    def enter_any_password(self, password: str):
        """
        Step 3: Enter any password in the password field.
        Acceptance Criteria: Password is masked.
        """
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        is_masked = password_field.get_attribute("type") == "password"
        return is_masked and password_field.get_attribute("value") == password

    def click_login_and_verify_invalid_credentials(self):
        """
        Step 4: Click on the Login button and verify error message for non-existent email.
        Acceptance Criteria: Login fails with error message 'Invalid credentials'.
        """
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self.is_error_message_displayed("Invalid credentials")
    # --- End of TC_SCRUM74_003 steps ---

    # --- Start of TC_LOGIN_004 steps ---
    def enter_valid_email_leave_password_empty(self, email: str):
        """
        TC_LOGIN_004 - Step 2 & 3: Enter valid registered email and leave password field empty.
        Acceptance Criteria: Email is accepted, password field remains empty.
        """
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        return email_field.get_attribute("value") == email and password_field.get_attribute("value") == ""

    def click_login_and_verify_password_required(self):
        """
        TC_LOGIN_004 - Step 4: Click on the Login button and verify validation error for empty password.
        Acceptance Criteria: Validation error displayed: 'Password is required'.
        """
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self.is_validation_error_displayed("Password is required")

    def verify_login_prevented_password_empty(self):
        """
        TC_LOGIN_004 - Step 5: Verify login is prevented and user remains on login page when password is empty.
        Acceptance Criteria: User cannot proceed with login, remains on login page.
        """
        current_url = self.driver.current_url
        on_login_page = current_url.startswith(self.LOGIN_URL)
        dashboard_visible = self.is_dashboard_displayed()
        return on_login_page and not dashboard_visible
    # --- End of TC_LOGIN_004 steps ---
