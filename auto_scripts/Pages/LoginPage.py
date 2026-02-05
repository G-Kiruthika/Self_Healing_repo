# Selenium Page Object for LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    # Locators loaded from Locators.json for maintainability
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

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_login(self, url: str = None):
        target_url = url if url else self.LOGIN_URL
        self.driver.get(target_url)
        return self.is_login_page_displayed()

    def is_login_page_displayed(self):
        try:
            email_visible = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            password_visible = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
            return email_visible.is_displayed() and password_visible.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def enter_email(self, email: str):
        try:
            email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            email_field.clear()
            email_field.send_keys(email)
            return email_field.get_attribute("value") == email
        except (NoSuchElementException, TimeoutException):
            return False

    def enter_password(self, password: str):
        try:
            password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
            password_field.clear()
            password_field.send_keys(password)
            is_masked = password_field.get_attribute("type") == "password"
            return is_masked and password_field.get_attribute("value") == password
        except (NoSuchElementException, TimeoutException):
            return False

    def click_login(self):
        try:
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
            login_btn.click()
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def is_error_message_displayed(self, expected_message: str = "Invalid email or password"):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.is_displayed() and expected_message in error_elem.text
        except (NoSuchElementException, TimeoutException):
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

    def tc_login_003_valid_email_wrong_password(self, url: str = "https://example-ecommerce.com/login", email: str = "testuser@example.com", password: str = "WrongPassword456", expected_error: str = "Invalid email or password"):
        login_page_displayed = self.navigate_to_login(url)
        if not login_page_displayed:
            print("Login page not displayed.")
            return False
        email_entered = self.enter_email(email)
        if not email_entered:
            print("Email not entered correctly.")
            return False
        password_entered = self.enter_password(password)
        if not password_entered:
            print("Password not entered or not masked.")
            return False
        login_clicked = self.click_login()
        if not login_clicked:
            print("Login button not clicked.")
            return False
        error_displayed = self.is_error_message_displayed(expected_error)
        if not error_displayed:
            print("Error message not displayed or incorrect.")
            return False
        user_stays = self.verify_user_stays_on_login_page()
        if not user_stays:
            print("User did not remain on login page.")
            return False
        return all([
            login_page_displayed,
            email_entered,
            password_entered,
            login_clicked,
            error_displayed,
            user_stays
        ])

    def is_validation_error_displayed(self, expected_message: str = None):
        """
        Checks for validation error message near the email field.
        """
        try:
            val_error_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            if expected_message:
                return val_error_elem.is_displayed() and expected_message in val_error_elem.text
            return val_error_elem.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def is_empty_field_prompt_displayed(self):
        """
        Checks for the specific empty field prompt message.
        """
        try:
            prompt_elem = self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return prompt_elem.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def tc_login_004_empty_email_valid_password(
        self,
        url: str = "https://example-ecommerce.com/login",
        password: str = "ValidPass123!",
        expected_validation_error: str = "Email is required",
        expected_empty_field_prompt: str = "Mandatory fields are required"
    ):
        """
        Test Case TC-LOGIN-004: Login attempt with empty email field.
        Steps:
        1. Navigate to login page
        2. Leave email field empty
        3. Enter valid password
        4. Click login
        5. Verify validation error for empty email
        6. Ensure user remains unauthenticated
        """
        login_page_displayed = self.navigate_to_login(url)
        if not login_page_displayed:
            print("Login page not displayed.")
            return False

        # Leave email field empty
        email_entered = self.enter_email("")
        if not email_entered:
            print("Email field was not cleared or is not blank.")
            return False
        try:
            email_field = self.driver.find_element(*self.EMAIL_INPUT)
            if email_field.get_attribute("value") != "":
                print("Email field is not empty after clear.")
                return False
        except NoSuchElementException:
            print("Email input not found after clearing.")
            return False

        # Enter valid password
        password_entered = self.enter_password(password)
        if not password_entered:
            print("Password not entered or not masked.")
            return False

        # Click login
        login_clicked = self.click_login()
        if not login_clicked:
            print("Login button not clicked.")
            return False

        # Verify validation error for empty email
        validation_error_displayed = self.is_validation_error_displayed(expected_validation_error)
        empty_field_prompt_displayed = self.is_empty_field_prompt_displayed()
        if not (validation_error_displayed or empty_field_prompt_displayed):
            print("Validation error for empty email not displayed.")
            return False

        # Ensure user remains unauthenticated
        user_stays = self.verify_user_stays_on_login_page()
        if not user_stays:
            print("User did not remain on login page (unauthenticated).")
            return False

        return all([
            login_page_displayed,
            email_entered,
            password_entered,
            login_clicked,
            (validation_error_displayed or empty_field_prompt_displayed),
            user_stays
        ])
