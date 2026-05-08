# PrinterDetailsScreen: Printer details screen.
from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class PrinterDetailsScreen(BasePage):
    EDIT_LINK = By.XPATH, 'placeholder_locator'

    def click_edit_link(self):
        return self.click(self.EDIT_LINK)

    def is_edit_link_visible(self):
        return self.is_visible(self.EDIT_LINK)
