"""Page Object for Printer Details Page."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PrinterDetailsPage(BasePage):
    """Page object for Printer Details Page."""
    
    BUTTON = (By.ID, 'placeholder_printer_details_button_locator')

    def __init__(self, driver):
        """Initialize PrinterDetailsPage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)

    def navigate_to_printer_details(self):
        """Navigate to printer details by clicking the button."""
        self.click_element(self.BUTTON)
