from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RootViewPage(BasePage):
    PRINTER_ICON = (By.ID, "placeholder_printer_icon_id")

    def __init__(self, driver):
        super().__init__(driver)

    def click_printer_icon(self):
        self.click_element(self.PRINTER_ICON)