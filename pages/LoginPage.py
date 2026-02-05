import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators loaded from Locators.json
        self.login_url = "https://your-app-url.com/login"  # Replace with actual URL if dynamic
        self.email_field = (By.ID, "email")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "loginBtn")
        self.error_message = (By.ID, "errorMsg")

    def open_login_page(self):
        self.driver.get(self.login_url)

    def enter_email(self, email):
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.email_field)
        )
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.password_field)
        )
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        )
        login_btn.click()

    def get_error_message(self):
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message)
            )
            return error.text
        except TimeoutException:
            return None

    def get_password_field_value(self):
        try:
            password_input = self.driver.find_element(*self.password_field)
            return password_input.get_attribute("value")
        except NoSuchElementException:
            return None

    # TC006: Test login with valid email, empty password, check error message and login failure
    def login_with_valid_email_and_empty_password_tc006(self, email="user@example.com"):
        """
        Steps:
        1. Open login page
        2. Enter valid email ('user@example.com'), leave password empty
        3. Click login
        4. Verify password field remains empty
        5. Check for error message 'Password required'
        6. Confirm login fails
        Returns dict with results of each step.
        """
        results = {}
        self.open_login_page()
        results['page_opened'] = self.driver.current_url == self.login_url

        self.enter_email(email)
        # Leave password field empty (do not call enter_password)
        password_value = self.get_password_field_value()
        results['password_empty'] = (password_value == "" or password_value is None)

        self.click_login()
        time.sleep(1)  # Short wait for error message to appear

        error_msg = self.get_error_message()
        results['error_message_displayed'] = (error_msg == "Password required")
        results['login_failed'] = results['error_message_displayed']

        # Return details for validation
        return results
