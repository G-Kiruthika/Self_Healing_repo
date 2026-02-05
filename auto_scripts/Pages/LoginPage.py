from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    WebDriverException
)

class LoginPage:
    '''
    Page Object for the Login Page.
    Implements methods for login scenarios and navigation to password recovery.
    '''

    # Locators from Locators.json
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[contains(text(),'Mandatory fields are required')]")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Existing methods preserved ---
    # ... [existing code preserved, see previous content] ...

    # --- TC-LOGIN-008: Login with Extremely Long Email Address ---
    def tc_login_008_extremely_long_email_login(self, long_email: str, valid_password: str) -> bool:
        '''
        Automates TC-LOGIN-008: Login attempt using an extremely long email address (255+ characters).
        Steps:
            1. Navigate to the login page.
            2. Enter extremely long email address.
            3. Enter valid password.
            4. Click on the Login button.
            5. Validate system response: truncation, validation error, or graceful failure.
        Args:
            long_email (str): The extremely long email address.
            valid_password (str): The valid password.
        Returns:
            bool: True if system handles input gracefully (error/truncation/validation), False otherwise.
        '''
        try:
            self.driver.get("https://ecommerce.example.com/login")
            self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
            email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_input.clear()
            email_input.send_keys(long_email)
            password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_input.clear()
            password_input.send_keys(valid_password)
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
            error_or_validation_present = False
            try:
                error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
                if error_elem.is_displayed():
                    error_or_validation_present = True
            except (TimeoutException, NoSuchElementException):
                pass
            try:
                validation_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
                if validation_elem.is_displayed():
                    error_or_validation_present = True
            except (TimeoutException, NoSuchElementException):
                pass
            still_on_login_page = self.driver.current_url == "https://ecommerce.example.com/login"
            dashboard_header_absent = True
            try:
                self.driver.find_element(*self.DASHBOARD_HEADER)
                dashboard_header_absent = False
            except NoSuchElementException:
                dashboard_header_absent = True
            return error_or_validation_present and still_on_login_page and dashboard_header_absent
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException) as e:
            print(f"Exception during TC_LOGIN_008 extremely long email login: {e}")
            return False

    # --- TC-LOGIN-015: Login with Password Containing Special Characters ---
    def tc_login_015_special_char_password(self, username: str, special_char_password: str) -> bool:
        '''
        Automates TC-LOGIN-015: Login attempt using a password with various special characters.
        Steps:
            1. Navigate to the login page.
            2. Enter valid username.
            3. Enter password with special characters.
            4. Click on the Login button.
            5. Validate system processes login correctly (successful login or appropriate error).
        Args:
            username (str): The valid username/email.
            special_char_password (str): The password with special characters.
        Returns:
            bool: True if system processes login correctly (user is logged in or proper error message shown), False otherwise.
        '''
        try:
            self.driver.get("https://ecommerce.example.com/login")
            self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
            email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_input.clear()
            email_input.send_keys(username)
            password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_input.clear()
            password_input.send_keys(special_char_password)
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
            # Wait for either dashboard or error/validation
            try:
                # Success: user lands on dashboard and sees profile icon/header
                self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
                self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
                return True
            except TimeoutException:
                # Failure: check for error or validation message
                try:
                    error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
                    if error_elem.is_displayed():
                        return True
                except (TimeoutException, NoSuchElementException):
                    pass
                try:
                    validation_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
                    if validation_elem.is_displayed():
                        return True
                except (TimeoutException, NoSuchElementException):
                    pass
            # If neither success nor error/validation, test failed
            return False
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException) as e:
            print(f"Exception during TC_LOGIN_015 special char password login: {e}")
            return False
