from selenium.webdriver.common.by import By
from auto_scripts.BasePage import BasePage

class ShortcutsScreen(BasePage):
    def click_add_new_shortcut(self):
        add_new_shortcut_button = self.driver.find_element(By.ACCESSIBILITY_ID, 'add_new_shortcut_button')
        add_new_shortcut_button.click()
