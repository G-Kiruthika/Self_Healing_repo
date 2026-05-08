from auto_scripts.Pages.base_page import BasePage
from selenium.webdriver.common.by import By

class AddShortcutScreen(BasePage):
    SHORTCUT_TYPE_DROPDOWN = (By.ID, "shortcut_type_dropdown")
    CONFIRM_BUTTON = (By.ID, "confirm_btn")

    def select_shortcut_type(self, shortcut_type):
        self.select_dropdown_option(self.SHORTCUT_TYPE_DROPDOWN, shortcut_type)

    def click_confirm_button(self):
        self.click_element(self.CONFIRM_BUTTON)

    def is_shortcut_type_dropdown_visible(self):
        return self.is_element_visible(self.SHORTCUT_TYPE_DROPDOWN)
