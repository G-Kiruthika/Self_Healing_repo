from selenium.webdriver.common.by import By
from auto_scripts.Pages.BasePage import BasePage

class ShortcutsScreen(BasePage):
    ADD_NEW_SHORTCUTS_BTN = (By.XPATH, "//android.widget.Button[@content-desc='AddNewShortcuts']")

    def click_add_new_shortcuts(self):
        self.click(self.ADD_NEW_SHORTCUTS_BTN)

    def is_add_new_shortcuts_btn_visible(self):
        return self.is_visible(self.ADD_NEW_SHORTCUTS_BTN)
