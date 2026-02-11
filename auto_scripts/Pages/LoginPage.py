# LoginPage.py
# Selenium PageClass for TC_LOGIN_003: Invalid Email Format Login

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    """
    PageClass for LoginPage supporting TC_LOGIN_003 (Invalid Email Format Login)
    Implements navigation, data entry, login action, error validation, and session status verification.
    """
    # Locators (must be validated against Locators.json if available)
    EMAIL_INPUT_LOCATOR = (By.ID, "email_input")
    PASSWORD_INPUT_LOCATOR = (By.ID, "password_input")
    LOGIN_BUTTON_LOCATOR = (By.ID, "login_button")
    ERROR_MESSAGE_LOCATOR = (By.ID, "login_error_message")
    LOGIN_SCREEN_LOCATOR = (By.ID, "login_screen")

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_login_page(self, url):
        """
        Step 1: Navigate to the login page
        Args:
            url (str): The login page URL
        Returns:
            bool: True if login page is displayed, False otherwise
        """
        self.driver.get(url)
        try:
            return self.driver.find_element(*self.LOGIN_SCREEN_LOCATOR).is_displayed()
        except NoSuchElementException:
            return False

    def enter_email(self, email):
        """
        Step 2: Enter email (invalid format supported)
        Args:
            email (str): Email input value
        Returns:
            bool: True if email field accepts input, False otherwise
        """
        try:
            email_field = self.driver.find_element(*self.EMAIL_INPUT_LOCATOR)
            email_field.clear()
            email_field.send_keys(email)
            return email_field.get_attribute("value") == email
        except NoSuchElementException:
            return False

    def enter_password(self, password):
        """
        Step 3: Enter valid password
        Args:
            password (str): Password input value
        Returns:
            bool: True if password field accepts input, False otherwise
        """
        try:
            password_field = self.driver.find_element(*self.PASSWORD_INPUT_LOCATOR)
            password_field.clear()
            password_field.send_keys(password)
            return password_field.get_attribute("value") == password
        except NoSuchElementException:
            return False

    def click_login_button(self):
        """
        Step 4: Click Login button
        Returns:
            bool: True if click action is successful, False otherwise
        """
        try:
            login_button = self.driver.find_element(*self.LOGIN_BUTTON_LOCATOR)
            login_button.click()
            return True
        except NoSuchElementException:
            return False

    def get_error_message(self):
        """
        Step 4: Retrieve error message after login attempt
        Returns:
            str: Error message text if present, else None
        """
        try:
            error_elem = self.driver.find_element(*self.ERROR_MESSAGE_LOCATOR)
            if error_elem.is_displayed():
                return error_elem.text
            return None
        except NoSuchElementException:
            return None

    def is_user_logged_in(self):
        """
        Step 5: Verify user is not logged in
        Returns:
            bool: False if user remains on login page, True if session is created (should be False for invalid email)
        """
        try:
            # If login screen is still displayed, user is not logged in
            return not self.driver.find_element(*self.LOGIN_SCREEN_LOCATOR).is_displayed()
        except NoSuchElementException:
            # If login screen is not found, user may be redirected
            return True

    # Composite test method for TC_LOGIN_003
    def execute_tc_login_003(self, url, email, password):
        """
        Execute TC_LOGIN_003 end-to-end
        Args:
            url (str): Login page URL
            email (str): Invalid email format
            password (str): Valid password
        Returns:
            dict: Results of each step and overall validation
        """
        results = {}
        results["navigate"] = self.navigate_to_login_page(url)
        results["enter_email"] = self.enter_email(email)
        results["enter_password"] = self.enter_password(password)
        results["click_login"] = self.click_login_button()
        error_message = self.get_error_message()
        results["error_message"] = error_message == "Please enter a valid email address"
        results["user_logged_in"] = not self.is_user_logged_in()  # Should be True if user NOT logged in
        results["overall"] = all([
            results["navigate"],
            results["enter_email"],
            results["enter_password"],
            results["click_login"],
            results["error_message"],
            results["user_logged_in"]
        ])
        return results

# Example usage:
# from selenium import webdriver
# driver = webdriver.Chrome()
# login_page = LoginPage(driver)
# result = login_page.execute_tc_login_003(
#     url="https://example-ecommerce.com/login",
#     email="invalidemail@com",
#     password="Test@1234"
# )
# print(result)
