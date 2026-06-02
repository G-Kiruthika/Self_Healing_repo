from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AddShortcutPage(BasePage):
    """Page Object for AddShortcutPage"""
    
    ADD_SHORTCUT_SCREEN = (By.ID, "add_shortcut_screen_id_placeholder")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def verify_add_shortcut_screen_displayed(self):
        """Verifies if the add shortcut screen is displayed"""
        return self.is_element_visible(self.ADD_SHORTCUT_SCREEN)
