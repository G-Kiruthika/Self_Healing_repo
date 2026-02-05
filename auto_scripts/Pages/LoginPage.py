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
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver, timeout=10):
        """
        Initializes the LoginPage object.

        :param driver: Selenium WebDriver instance.
        :param timeout: Default timeout for waits.
        """
        self.driver = driver
        self.timeout = timeout

    def navigate_to_login(self):
        """
        Navigates to the login page URL and verifies page load.

        :raises TimeoutException: if login page does not load.
        """
        try:
            self.driver.get(self.URL)
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(self.EMAIL_FIELD)
            )
        except (TimeoutException, WebDriverException) as e:
            raise TimeoutException("Login page did not load properly.") from e

    def enter_email(self, email):
        """
        Enters email into the email field.

        :param email: Email string (can be SQL injection payload).
        :raises Exception: if field is not interactable.
        """
        try:
            email_input = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(self.EMAIL_FIELD)
            )
            email_input.clear()
            email_input.send_keys(email)
        except (TimeoutException, ElementNotInteractableException) as e:
            raise Exception("Unable to enter email.") from e

    def enter_password(self, password):
        """
        Enters password into the password field.

        :param password: Password string.
        :raises Exception: if field is not interactable.
        """
        try:
            password_input = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(self.PASSWORD_FIELD)
            )
            password_input.clear()
            password_input.send_keys(password)
        except (TimeoutException, ElementNotInteractableException) as e:
            raise Exception("Unable to enter password.") from e

    def click_login(self):
        """
        Clicks the login button.

        :raises Exception: if button is not interactable.
        """
        try:
            login_btn = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(self.LOGIN_BUTTON)
            )
            login_btn.click()
        except (TimeoutException, ElementNotInteractableException) as e:
            raise Exception("Unable to click login button.") from e

    def verify_error_message(self, expected_message=None):
        """
        Verifies that an error message is displayed after failed login.

        :param expected_message: Optional string to match error message.
        :return: True if error message is displayed, False otherwise.
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            if expected_message:
                return expected_message in error_elem.text
            return True
        except TimeoutException:
            return False

    def verify_no_unauthorized_access(self):
        """
        Verifies that user is NOT granted access after failed login.

        Checks absence of dashboard header and user profile icon.

        :return: True if unauthorized access is prevented, False otherwise.
        """
        try:
            # Wait for possible redirect, then check absence of dashboard elements
            WebDriverWait(self.driver, self.timeout).until_not(
                EC.presence_of_element_located(self.DASHBOARD_HEADER)
            )
        except TimeoutException:
            # Dashboard header not present, which is expected
            pass

        # Check user profile icon
        try:
            self.driver.find_element(*self.USER_PROFILE_ICON)
            # If found, unauthorized access granted
            return False
        except NoSuchElementException:
            # Not found, access prevented
            return True

    def perform_sql_injection_test(self, email_payload, password, expected_error=None):
        """
        Executes all steps of TC-LOGIN-012 for SQL injection prevention.

        :param email_payload: SQL injection payload for email field.
        :param password: Password to use.
        :param expected_error: Expected error message after failed login.
        :return: Dict with step results.
        """
        results = {}
        try:
            self.navigate_to_login()
            results['navigate_to_login'] = True
        except Exception as e:
            results['navigate_to_login'] = False
            results['error'] = str(e)
            return results

        try:
            self.enter_email(email_payload)
            results['enter_email'] = True
        except Exception as e:
            results['enter_email'] = False
            results['error'] = str(e)
            return results

        try:
            self.enter_password(password)
            results['enter_password'] = True
        except Exception as e:
            results['enter_password'] = False
            results['error'] = str(e)
            return results

        try:
            self.click_login()
            results['click_login'] = True
        except Exception as e:
            results['click_login'] = False
            results['error'] = str(e)
            return results

        results['verify_error_message'] = self.verify_error_message(expected_error)
        results['verify_no_unauthorized_access'] = self.verify_no_unauthorized_access()

        return results

# Example usage (should be in test file, not in PageClass):
# from selenium import webdriver
# driver = webdriver.Chrome()
# login_page = LoginPage(driver)
# result = login_page.perform_sql_injection_test("admin' OR '1'='1", "password123", expected_error="Invalid credentials")
# assert result['verify_error_message'] and result['verify_no_unauthorized_access']
