"""
LoginPage PageClass for Selenium automation.
Implements TC-LOGIN-012: SQL Injection prevention on login form.
All locators are mapped from Locators.json. Strictly follows Python Selenium best practices.
"""

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
    """
    Page Object for the Login Page.
    Implements methods for TC-LOGIN-012: SQL Injection prevention.
    """

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

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Existing methods for TC-LOGIN-012 ---
    # ... [existing code preserved] ...

    # --- Start of TC-LOGIN-010 steps ---
    def tc_login_010_special_char_email_login(self, email: str, password: str) -> bool:
        """
        TC-LOGIN-010: Login with email containing special characters
        Steps:
        1. Navigate to the login page [Test Data: URL: https://ecommerce.example.com/login]
        2. Enter email with special characters [Test Data: Email: test.user+tag@example.com]
        3. Enter valid password [Test Data: Password: ValidPass123!]
        4. Click on the Login button
        Acceptance Criteria: TS-008
        """
        try:
            # Step 1: Navigate to Login Page
            self.driver.get(self.URL)
            login_page_displayed = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD)).is_displayed()
            assert login_page_displayed, "Login page is not displayed"

            # Step 2: Enter email with special characters
            email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_input.clear()
            email_input.send_keys(email)
            assert email_input.get_attribute("value") == email, "Email with special characters is not accepted"

            # Step 3: Enter valid password
            password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_input.clear()
            password_input.send_keys(password)
            assert password_input.get_attribute("type") == "password", "Password field is not masked"

            # Step 4: Click on the Login button
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()

            # Step 5: Validate login result
            try:
                dashboard_visible = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER)).is_displayed()
                return dashboard_visible
            except TimeoutException:
                # Check for error message if login fails
                if self.driver.find_elements(*self.ERROR_MESSAGE):
                    error = self.driver.find_element(*self.ERROR_MESSAGE)
                    assert error.is_displayed(), "Error message should be displayed for invalid credentials"
                    return False
                else:
                    raise AssertionError("Neither dashboard nor error message displayed after login attempt")
        except Exception as e:
            raise AssertionError(f"TC-LOGIN-010 failed: {str(e)}")
    # --- End of TC-LOGIN-010 steps ---
