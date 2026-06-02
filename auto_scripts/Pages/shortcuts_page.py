from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ShortcutsPage(BasePage):
    """Page Object for ShortcutsPage"""
    
    ADD_NEW_SHORTCUTS_BUTTON = (By.ID, "add_new_shortcuts_btn_id_placeholder")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_add_new_shortcuts(self):
        """Clicks the add new shortcuts button"""
        self.click_element(self.ADD_NEW_SHORTCUTS_BUTTON)
