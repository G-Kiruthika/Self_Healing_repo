from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://example-ecommerce.com/login"
    EMAIL_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_login_page(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))

    def enter_email(self, email):
        email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password):
        password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def get_error_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
        except:
            return None

    def is_dashboard_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except:
            return False

    def is_user_profile_icon_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except:
            return False

    def get_validation_error(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR)).text
        except:
            return None

    # TC_LOGIN_07_02: login_with_short_email_and_password_and_validate_error
    def login_with_short_email_and_password_and_validate_error(self, email="a@", password="abc"):
        """
        1. Navigate to the login page.
        2. Enter an email shorter than minimum allowed (default: 'a@').
        3. Enter a password shorter than minimum allowed (default: 'abc').
        4. Click 'Login'.
        5. Assert error is shown.
        6. Assert login is not allowed.
        """
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

        # Wait for either error message or validation error
        error_text = None
        validation_text = None
        error_displayed = False
        validation_displayed = False

        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            error_text = error_elem.text
            error_displayed = True
        except:
            pass

        try:
            validation_elem = self.driver.find_element(*self.VALIDATION_ERROR)
            if validation_elem.is_displayed():
                validation_text = validation_elem.text
                validation_displayed = True
        except:
            pass

        assert error_displayed or validation_displayed, (
            "Expected error or validation message, but none was displayed."
        )
        assert not self.is_dashboard_displayed(), "Dashboard should not be displayed for invalid login."
        assert not self.is_user_profile_icon_displayed(), "User profile icon should not be displayed for invalid login."
        return {
            "error_message": error_text,
            "validation_error": validation_text,
            "error_displayed": error_displayed,
            "validation_displayed": validation_displayed
        }

    # TC_LOGIN_08_01: login_with_special_char_email_and_password_and_validate_success
    def login_with_special_char_email_and_password_and_validate_success(self, email="user.name+tag@example.com", password="P@ssw0rd!#"):
        """
        1. Navigate to the login page. [Acceptance Criteria: SCENARIO-8]
        2. Enter a valid email address containing allowed special characters (e.g., dot, underscore, plus).
        3. Enter a valid password containing special characters.
        4. Click the 'Login' button.
        5. Assert that the login page is displayed initially.
        6. Assert that email and password are accepted.
        7. Assert successful login (dashboard and user profile icon visible) if credentials are valid.
        """
        self.go_to_login_page()
        # Step 1: Ensure login page is displayed
        assert self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)), "Login page is not displayed."
        # Step 2: Enter special character email
        self.enter_email(email)
        # Step 3: Enter special character password
        self.enter_password(password)
        # Step 4: Click Login
        self.click_login()
        # Step 5: Validate acceptance
        # If login succeeds, dashboard and profile icon must be visible
        dashboard_displayed = self.is_dashboard_displayed()
        profile_icon_displayed = self.is_user_profile_icon_displayed()
        assert dashboard_displayed, "User is not successfully logged in (dashboard not visible)."
        assert profile_icon_displayed, "User profile icon not visible after login."
        return {
            "dashboard_displayed": dashboard_displayed,
            "profile_icon_displayed": profile_icon_displayed
        }
