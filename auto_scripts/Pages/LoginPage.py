import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://ecommerce.example.com/login"
        self.email_input_locator = (By.ID, "email")
        self.password_input_locator = (By.ID, "password")
        self.login_button_locator = (By.ID, "loginBtn")
        self.error_message_locator = (By.CSS_SELECTOR, ".error-message")

    def navigate(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.email_input_locator)
        )

    def enter_email(self, email):
        email_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_input_locator)
        )
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        password_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_input_locator)
        )
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button_locator)
        )
        login_button.click()

    def get_error_message(self):
        try:
            error_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message_locator)
            )
            return error_element.text
        except Exception:
            return None
