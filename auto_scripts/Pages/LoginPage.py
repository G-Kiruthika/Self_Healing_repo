from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to_login_page(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

    def enter_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_btn.click()

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None

    def is_on_login_page(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            return True
        except:
            return False

    def login_with_credentials(self, email, password):
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def perform_invalid_login_and_validate(self, email, invalid_password, expected_error):
        self.login_with_credentials(email, invalid_password)
        error_msg = self.get_error_message()
        assert error_msg == expected_error, f"Expected error '{expected_error}', got '{error_msg}'"
        assert self.is_on_login_page(), "User is not on the login page after failed login."

    def click_forgot_username(self):
        forgot_username_link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK))
        forgot_username_link.click()

    def login_with_minimum_allowed_credentials_and_verify_success(self):
        """
        TC_LOGIN_07_01:
        1. Navigate to the login page.
        2. Enter an email address with the minimum allowed length (a@b.co).
        3. Enter a password with the minimum allowed length (Abc12345).
        4. Click the 'Login' button.
        5. Verify that the user is successfully logged in if credentials are valid.
        """
        self.go_to_login_page()
        self.enter_email("a@b.co")
        self.enter_password("Abc12345")
        self.click_login()
        # Verification: Wait for dashboard or user profile icon to be visible as sign of successful login
        try:
            dashboard_header = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            user_profile_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            assert dashboard_header.is_displayed() or user_profile_icon.is_displayed(), \
                "Login did not succeed: Dashboard or User Profile not visible."
        except Exception as e:
            raise AssertionError(f"Login with minimum allowed credentials failed: {e}")