from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class CreateShortcutScreen(BasePage):
    # Locators
    create_own_shortcut_arrow = (By.ID, 'create_own_shortcut_arrow_id_placeholder')

    # Actions
    def click_create_own_shortcut_arrow(self):
        self.driver.find_element(*self.create_own_shortcut_arrow).click()
