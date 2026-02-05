# Selenium Page Object for PasswordRecoveryPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PasswordRecoveryPage:
    PASSWORD_RECOVERY_URL = "https://ecommerce.example.com/forgot-password"
    EMAIL_INPUT = (By.ID, "recovery-email")
    SUBMIT_BUTTON = (By.ID, "recovery-submit")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.recovery-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.recovery-error")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def is_loaded(self):
        try:
            correct_url = self.driver.current_url.startswith(self.PASSWORD_RECOVERY_URL)
            email_visible = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)).is_displayed()
            instructions_visible = self.driver.find_element(By.CSS_SELECTOR, "div.instructions").is_displayed() if self.driver.find_elements(By.CSS_SELECTOR, "div.instructions") else True
            return correct_url and email_visible and instructions_visible
        except (NoSuchElementException, TimeoutException):
            return False

    def is_email_input_visible(self):
        try:
            input_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            return input_field.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    # ... [Other existing methods remain unchanged] ...
