from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DeviceDetailsPage(BasePage):
    """Page Object for DeviceDetailsPage"""
    
    SHORTCUTS_TILE = (By.ID, "shortcuts_tile_id_placeholder")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_shortcuts_tile(self):
        """Clicks the shortcuts tile"""
        self.click_element(self.SHORTCUTS_TILE)
