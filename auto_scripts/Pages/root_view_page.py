from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RootViewPage(BasePage):
    """Page Object for RootViewPage"""
    
    PRINTER_ICON = (By.ID, "printer_icon_id_placeholder")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_printer_icon(self):
        """Clicks the printer icon"""
        self.click_element(self.PRINTER_ICON)
