# RemoveDestinationPopup: Popup dialog for removing a destination.
from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class RemoveDestinationPopup(BasePage):
    POPUP_CONTAINER = By.XPATH, 'placeholder_locator'

    def verify_popup_displayed(self):
        return self.is_visible(self.POPUP_CONTAINER)
