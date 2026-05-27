from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ShortcutsPage(BasePage):
    ADD_NEW_SHORTCUTS = (By.ID, "placeholder_add_new_shortcuts_id")

    def __init__(self, driver):
        super().__init__(driver)

    def click_add_new_shortcuts(self):
        self.click_element(self.ADD_NEW_SHORTCUTS)