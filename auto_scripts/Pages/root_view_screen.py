from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class RootViewScreen(BasePage):
    # Locators
    printer_icon = (By.ID, 'printer_icon_id_placeholder')

    # Actions
    def click_printer_icon(self):
        self.driver.find_element(*self.printer_icon).click()
