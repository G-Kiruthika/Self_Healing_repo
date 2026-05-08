"""Page Object for HPX App Launch Page."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HPXAppLaunchPage(BasePage):
    """Page object for HPX App Launch Page."""
    
    APP_ICON = (By.ID, 'placeholder_app_icon_locator')
    POPUP = (By.ID, 'placeholder_remove_popup_locator')

    def __init__(self, driver):
        """Initialize HPXAppLaunchPage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)

    def launch_app(self):
        """Launch the HPX application by clicking the app icon."""
        self.click_element(self.APP_ICON)

    def is_remove_popup_displayed(self) -> bool:
        """Check if the remove popup is displayed.
        
        Returns:
            bool: True if popup is visible, False otherwise
        """
        return self.is_element_visible(self.POPUP)
