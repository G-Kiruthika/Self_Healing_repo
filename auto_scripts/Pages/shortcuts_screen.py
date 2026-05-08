from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class ShortcutsScreen(BasePage):
    # Locators
    add_new_shortcut = (By.ID, 'add_new_shortcut_id_placeholder')

    # Actions
    def click_add_new_shortcut(self):
        self.driver.find_element(*self.add_new_shortcut).click()
