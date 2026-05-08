# AddShortcutScreen: Add Shortcut configuration screen.
from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class AddShortcutScreen(BasePage):
    SAVE_DESTINATION_TOGGLE = By.XPATH, 'placeholder_locator'
    CREATE_YOUR_OWN_SHORTCUT_ARROW = By.XPATH, 'placeholder_locator'

    def enable_save_destination_toggle(self):
        return self.click(self.SAVE_DESTINATION_TOGGLE)

    def click_create_your_own_shortcut_arrow(self):
        return self.click(self.CREATE_YOUR_OWN_SHORTCUT_ARROW)

    def is_save_destination_toggle_visible(self):
        return self.is_visible(self.SAVE_DESTINATION_TOGGLE)

    def is_create_your_own_shortcut_arrow_visible(self):
        return self.is_visible(self.CREATE_YOUR_OWN_SHORTCUT_ARROW)
