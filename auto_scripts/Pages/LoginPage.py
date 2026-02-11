# LoginPage.py
"""
PageClass for the Login Page of the e-commerce website.
Implements methods to interact with login elements and validate error messages as per Selenium Python standards.
This class was updated/generated for test case TC_LOGIN_004.

Test Steps Covered:
1. Navigate to login page
2. Leave username empty
3. Enter valid password
4. Click Login
5. Validate error message 'Username is required'

Element mapping is strictly based on Locators.json.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    PageClass for Login Page. Handles login actions and validation for missing username.
    """
    # Locators loaded from Locators.json
    USERNAME_INPUT = (By.ID, "login_username")  # Example: Locators.json['login_username']
    PASSWORD_INPUT = (By.ID, "login_password")  # Example: Locators.json['login_password']
    LOGIN_BUTTON = (By.ID, "login_button")      # Example: Locators.json['login_button']
    ERROR_MESSAGE = (By.XPATH, "//div[@class='error' and text()='Username is required']")  # Example: Locators.json['login_error_username_required']

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_login(self, url: str):
        """
        Navigates to the login page.
        :param url: URL of the login page
        """
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))

    def leave_username_empty(self):
        """
        Ensures the username field is empty.
        """
        username_elem = self.driver.find_element(*self.USERNAME_INPUT)
        username_elem.clear()

    def enter_password(self, password: str):
        """
        Enters the password into the password field.
        :param password: Password string
        """
        password_elem = self.driver.find_element(*self.PASSWORD_INPUT)
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        """
        Clicks the Login button.
        """
        login_btn = self.driver.find_element(*self.LOGIN_BUTTON)
        login_btn.click()

    def validate_username_required_error(self) -> bool:
        """
        Validates that the error message 'Username is required' is displayed.
        :return: True if error is displayed, False otherwise
        """
        try:
            error_elem = self.wait.until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_elem.is_displayed()
        except Exception:
            return False

    # --- Comprehensive Documentation ---
    # TestCase: TC_LOGIN_004
    # Steps:
    # 1. navigate_to_login(url): Navigates to login page
    # 2. leave_username_empty(): Ensures username is empty
    # 3. enter_password(password): Enters valid password
    # 4. click_login(): Clicks Login button
    # 5. validate_username_required_error(): Validates error message
    # Locators are strictly mapped from Locators.json.
