from auto_scripts.Pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ShortcutsScreen(BasePage):
    SHORTCUT_LIST = (By.ID, "shortcut_list")
    ADD_SHORTCUT_BUTTON = (By.XPATH, "//button[@id='add_shortcut']")

    def click_add_shortcut_button(self):
        self.click_element(self.ADD_SHORTCUT_BUTTON)

    def is_shortcut_list_visible(self):
        return self.is_element_visible(self.SHORTCUT_LIST)
