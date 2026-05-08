"""Page Object for Shortcuts Page."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ShortcutsPage(BasePage):
    """Page object for Shortcuts Page."""
    
    TAB = (By.ID, 'placeholder_shortcuts_tab_locator')
    LINK = (By.ID, 'placeholder_edit_link_locator')
    ICON = (By.ID, 'placeholder_edit_icon_print_locator')

    def __init__(self, driver):
        """Initialize ShortcutsPage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)

    def navigate_to_shortcuts(self):
        """Navigate to shortcuts by clicking the tab."""
        self.click_element(self.TAB)

    def click_edit_link(self):
        """Click the edit link."""
        self.click_element(self.LINK)

    def click_edit_icon_print_shortcut(self):
        """Click the edit icon for print shortcut."""
        self.click_element(self.ICON)
