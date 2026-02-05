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
        """
        Navigates to the login page.
        """
        target_url = url if url else self.LOGIN_URL
        self.driver.get(target_url)
        return self.is_login_page_displayed()

    def is_login_page_displayed(self):
        """
        Verifies that the login page is displayed by checking the visibility of email and password fields.
        """
        try:
            email_visible = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            password_visible = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
            return email_visible.is_displayed() and password_visible.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def enter_email(self, email: str):
        """
        Enters the email into the email input field.
        """
        try:
            email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            email_field.clear()
            email_field.send_keys(email)
            return email_field.get_attribute("value") == email
        except (NoSuchElementException, TimeoutException):
            return False

    def enter_password(self, password: str):
        """
        Enters the password into the password input field and verifies it is masked.
        """
        try:
            password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
            password_field.clear()
            password_field.send_keys(password)
            is_masked = password_field.get_attribute("type") == "password"
            return is_masked and password_field.get_attribute("value") == password
        except (NoSuchElementException, TimeoutException):
            return False

    def click_login(self):
        """
        Clicks the login button.
        """
        try:
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
            login_btn.click()
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def is_error_message_displayed(self, expected_message: str = "Invalid email or password"):
        """
        Checks if the error message is displayed and matches the expected text.
        """
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.is_displayed() and expected_message in error_elem.text
        except (NoSuchElementException, TimeoutException):
            return False

    def verify_user_stays_on_login_page(self):
        """
        Verifies that the user remains on the login page and is not authenticated.
        """
        current_url = self.driver.current_url
        on_login_page = current_url.startswith(self.LOGIN_URL)
        dashboard_visible = self.is_dashboard_displayed()
        return on_login_page and not dashboard_visible

    def is_dashboard_displayed(self):
        """
        Checks if the dashboard header and user profile icon are visible, indicating successful login.
        """
        try:
            header_visible = self.driver.find_element(*self.DASHBOARD_HEADER).is_displayed()
            profile_visible = self.driver.find_element(*self.USER_PROFILE_ICON).is_displayed()
            return header_visible and profile_visible
        except NoSuchElementException:
            return False

    def tc_login_003_valid_email_wrong_password(
        self,
        url: str = "https://example-ecommerce.com/login",
        email: str = "testuser@example.com",
        password: str = "WrongPassword456",
        expected_error: str = "Invalid email or password"
    ):
        """
        TC-LOGIN-003: Login attempt with valid registered email and incorrect password
        """
        # Step 1: Navigate to login page
        login_page_displayed = self.navigate_to_login(url)
        if not login_page_displayed:
            print("Login page not displayed.")
            return False
        # Step 2: Enter valid registered email
        email_entered = self.enter_email(email)
        if not email_entered:
            print("Email not entered correctly.")
            return False
        # Step 3: Enter incorrect password
        password_entered = self.enter_password(password)
        if not password_entered:
            print("Password not entered or not masked.")
            return False
        # Step 4: Click login button
        login_clicked = self.click_login()
        if not login_clicked:
            print("Login button not clicked.")
            return False
        # Step 5: Verify error message
        error_displayed = self.is_error_message_displayed(expected_error)
        if not error_displayed:
            print("Error message not displayed or incorrect.")
            return False
        # Step 6: Verify user remains on login page
        user_stays = self.verify_user_stays_on_login_page()
        if not user_stays:
            print("User did not remain on login page.")
            return False
        # Note: Session/cookie validation can be added here if required.
        return all([
            login_page_displayed,
            email_entered,
            password_entered,
            login_clicked,
            error_displayed,
            user_stays
        ])

    def tc_login_004_empty_email_valid_password(
        self,
        url: str = "https://ecommerce.example.com/login",
        password: str = "ValidPass123!",
        expected_validation: str = "Email is required"
    ):
        """
        TC-LOGIN-004: Attempt login with empty email and valid password
        Steps:
        1. Navigate to the login page [Test Data: URL]
        2. Leave the email field empty [Test Data: Email: (empty)]
        3. Enter valid password [Test Data: Password]
        4. Click on the Login button
        5. Verify validation error is displayed: 'Email is required' or 'Please fill in all required fields'
        6. Verify login is not processed; user remains on login page without authentication
        Acceptance Criteria: TS-003
        """
        # Step 1: Navigate to login page
        login_page_displayed = self.navigate_to_login(url)
        if not login_page_displayed:
            print("Login page not displayed.")
            return False
        # Step 2: Leave email field empty
        email_entered = self.enter_email("")
        if not email_entered:
            print("Email field did not remain blank.")
            return False
        # Step 3: Enter valid password
        password_entered = self.enter_password(password)
        if not password_entered:
            print("Password not entered or not masked.")
            return False
        # Step 4: Click login button
        login_clicked = self.click_login()
        if not login_clicked:
            print("Login button not clicked.")
            return False
        # Step 5: Verify validation error for empty email
        try:
            validation_error_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            error_text = validation_error_elem.text
            valid_error = expected_validation in error_text or "Please fill in all required fields" in error_text
        except (NoSuchElementException, TimeoutException):
            print("Validation error not found.")
            valid_error = False
        # Step 6: Verify user remains on login page
        user_stays = self.verify_user_stays_on_login_page()
        if not user_stays:
            print("User did not remain on login page.")
            return False
        return all([
            login_page_displayed,
            email_entered,
            password_entered,
            login_clicked,
            valid_error,
            user_stays
        ])
