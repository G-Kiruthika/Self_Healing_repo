# Selenium Page Object for LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    LOGIN_URL = "https://example-ecommerce.com/login"  # Updated per Locators.json
    EMAIL_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def go_to_login_page(self):
        self.driver.get(self.LOGIN_URL)
        assert self.is_loaded(), "Login page did not load successfully"

    def is_loaded(self):
        try:
            correct_url = self.driver.current_url.startswith(self.LOGIN_URL)
            email_visible = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)).is_displayed()
            password_visible = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT)).is_displayed()
            login_btn_visible = self.wait.until(EC.visibility_of_element_located(self.LOGIN_BUTTON)).is_displayed()
            return correct_url and email_visible and password_visible and login_btn_visible
        except (NoSuchElementException, TimeoutException):
            return False

    def enter_email(self, email: str):
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_field.clear()
        email_field.send_keys(email)
        return email_field.get_attribute("value") == email

    def enter_password(self, password: str):
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_field.clear()
        password_field.send_keys(password)
        return password_field.get_attribute("value") == password

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def is_error_message_displayed(self):
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def is_validation_error_displayed(self):
        try:
            validation_error = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return validation_error.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    # --- Start of TC_LOGIN_008 steps ---
    def tc_login_008_extremely_long_email(self, email: str, password: str) -> bool:
        """
        TC-LOGIN-008: Login with extremely long email address (255+ characters)
        1. Navigate to the login page
        2. Enter an extremely long email address
        3. Enter valid password
        4. Click on the Login button
        5. Verify system truncates input or shows validation error, or login fails gracefully
        """
        self.go_to_login_page()
        assert self.is_loaded(), "Login page is not loaded"
        assert self.enter_email(email), "Email input failed"
        assert self.enter_password(password), "Password input failed"
        self.click_login()
        # Acceptance: Either validation error or error message is displayed, or login fails gracefully
        validation = self.is_validation_error_displayed()
        error = self.is_error_message_displayed()
        # Optionally, check for URL not changing (login fails gracefully)
        login_failed = self.driver.current_url.startswith(self.LOGIN_URL)
        assert validation or error or login_failed, (
            "Expected validation error, error message, or failed login, but none detected"
        )
        return validation or error or login_failed
    # --- End of TC_LOGIN_008 steps ---

    # --- Start of TC_LOGIN_003 steps ---
    def tc_login_003_invalid_password(self, email: str, invalid_password: str) -> bool:
        """
        TC-LOGIN-003: Attempt login with valid username and invalid password
        Steps:
        1. Navigate to the login page
        2. Enter valid username
        3. Enter invalid password
        4. Click on the Login button
        5. Verify error message 'Invalid username or password' is displayed and user remains on login page
        Returns True if the expected error message is displayed and URL remains on login page, else False.
        """
        self.go_to_login_page()
        assert self.is_loaded(), "Login page is not loaded"
        assert self.enter_email(email), "Email input failed"
        assert self.enter_password(invalid_password), "Password input failed"
        self.click_login()
        error_displayed = self.is_error_message_displayed()
        still_on_login = self.driver.current_url.startswith(self.LOGIN_URL)
        # Optionally, verify the actual error message text if needed
        if error_displayed:
            error_element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            error_text = error_element.text.strip()
            assert "Invalid username or password" in error_text, (
                f"Unexpected error message: {error_text}"
            )
        assert error_displayed and still_on_login, (
            "Expected error message and to remain on login page, but criteria not met"
        )
        return error_displayed and still_on_login
    # --- End of TC_LOGIN_003 steps ---
