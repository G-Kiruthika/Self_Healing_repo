# ShortcutsScreen: Shortcuts management screen.
from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class ShortcutsScreen(BasePage):
    EDIT_ICON_SAVE_SHORTCUT = By.XPATH, 'placeholder_locator'
    ADD_NEW_SHORTCUTS = By.XPATH, 'placeholder_locator'

    def click_edit_icon_save_shortcut(self):
        return self.click(self.EDIT_ICON_SAVE_SHORTCUT)

    def click_add_new_shortcuts(self):
        return self.click(self.ADD_NEW_SHORTCUTS)

    def is_edit_icon_save_shortcut_visible(self):
        return self.is_visible(self.EDIT_ICON_SAVE_SHORTCUT)

    def is_add_new_shortcuts_visible(self):
        return self.is_visible(self.ADD_NEW_SHORTCUTS)
