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
