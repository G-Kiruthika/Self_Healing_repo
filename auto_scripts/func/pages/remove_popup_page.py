"""Page Object for Remove Popup Page."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RemovePopupPage(BasePage):
    """Page object for Remove Popup Page."""
    
    BUTTON = (By.ID, 'placeholder_remove_button_locator')
    SHORTCUT = (By.ID, 'placeholder_print_shortcut_locator')
    POPUP = (By.ID, 'placeholder_remove_popup_locator')

    def __init__(self, driver):
        """Initialize RemovePopupPage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)

    def click_remove_button(self):
        """Click the remove button."""
        self.click_element(self.BUTTON)

    def is_print_shortcut_removed(self) -> bool:
        """Check if the print shortcut has been removed.
        
        Returns:
            bool: True if shortcut is not visible, False otherwise
        """
        return not self.is_element_visible(self.SHORTCUT)
    
    def is_remove_popup_displayed(self) -> bool:
        """Check if the remove popup is displayed.
        
        Returns:
            bool: True if popup is visible, False otherwise
        """
        return self.is_element_visible(self.POPUP)
