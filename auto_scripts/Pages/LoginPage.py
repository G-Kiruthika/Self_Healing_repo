from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://example-ecommerce.com/login"
    EMAIL_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ... existing methods ...

    def test_login_with_short_email_and_password(self, email="a@", password="abc"):
        """
        Test Case TC_LOGIN_07_02:
        1. Navigate to the login page.
        2. Enter an email address shorter than the minimum allowed length (e.g., 1 character).
        3. Enter a password shorter than the minimum allowed length (e.g., 3 characters).
        4. Click the 'Login' button.
        Expected: System displays an error or prevents login; appropriate error message is shown.
        """
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input = self.driver.find_element(*self.EMAIL_INPUT)
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)
        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()
        # Wait for either error message or validation error to appear
        error_displayed = False
        try:
            self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            error_displayed = True
        except:
            pass
        try:
            self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            error_displayed = True
        except:
            pass
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            error_displayed = True
        except:
            pass
        assert error_displayed, "Expected an error or validation message for short email/password, but none was displayed."
