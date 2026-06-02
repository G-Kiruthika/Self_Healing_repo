from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AddNewShortcutsPage(BasePage):
    """Page Object for AddNewShortcutsPage"""
    
    CREATE_YOUR_OWN_SHORTCUT_ARROW = (By.ID, "create_your_own_shortcut_arrow_id_placeholder")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_create_your_own_shortcut_arrow(self):
        """Clicks the create your own shortcut arrow"""
        self.click_element(self.CREATE_YOUR_OWN_SHORTCUT_ARROW)
