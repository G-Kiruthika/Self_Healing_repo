from auto_scripts.Pages.base_page import BasePage
from selenium.webdriver.common.by import By

class CreateShortcutScreen(BasePage):
    SHORTCUT_NAME_INPUT = (By.ID, "shortcut_name_input")
    SAVE_BUTTON = (By.ID, "save_btn")

    def enter_shortcut_name(self, name):
        self.enter_text(self.SHORTCUT_NAME_INPUT, name)

    def click_save_button(self):
        self.click_element(self.SAVE_BUTTON)

    def is_shortcut_name_input_visible(self):
        return self.is_element_visible(self.SHORTCUT_NAME_INPUT)
