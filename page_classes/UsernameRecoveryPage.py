from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class UsernameRecoveryPage:
    URL = 'https://example-ecommerce.com/forgot-username'
    INSTRUCTIONS_TEXT = (By.CSS_SELECTOR, 'div.recovery-instructions')
    EMAIL_FIELD = (By.ID, 'recovery-email')
    SUBMIT_BUTTON = (By.ID, 'recovery-submit')
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, 'div.recovery-success')
    USERNAME_RESULT = (By.CSS_SELECTOR, 'span.recovered-username')
    ERROR_MESSAGE = (By.CSS_SELECTOR, 'div.recovery-error')

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def load(self):
        self.driver.get(self.URL)

    def is_instructions_displayed(self):
        return self.driver.find_element(*self.INSTRUCTIONS_TEXT).is_displayed()

    def enter_email(self, email: str):
        email_elem = self.driver.find_element(*self.EMAIL_FIELD)
        email_elem.clear()
        email_elem.send_keys(email)

    def submit(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def get_success_message(self):
        return self.driver.find_element(*self.SUCCESS_MESSAGE).text

    def get_username_result(self):
        return self.driver.find_element(*self.USERNAME_RESULT).text

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def recover_username(self, email: str):
        self.enter_email(email)
        self.submit()
        if self.driver.find_elements(*self.SUCCESS_MESSAGE):
            return self.get_username_result()
        elif self.driver.find_elements(*self.ERROR_MESSAGE):
            return self.get_error_message()
        else:
            return None
