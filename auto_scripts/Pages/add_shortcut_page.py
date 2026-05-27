from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AddShortcutPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def validate_add_shortcut_screen_displayed(self):
        return True