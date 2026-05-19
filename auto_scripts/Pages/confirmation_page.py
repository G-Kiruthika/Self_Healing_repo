from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ConfirmationPage(BasePage):
    CONFIRMATION_MESSAGE = (By.XPATH, "//div[contains(text(),'Product added to cart')]")

    def __init__(self, driver):
        super().__init__(driver)

    def is_confirmation_message_displayed(self):
        return self.is_element_visible(self.CONFIRMATION_MESSAGE)
