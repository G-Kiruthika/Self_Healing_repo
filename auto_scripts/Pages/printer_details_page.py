from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PrinterDetailsPage(BasePage):
    PRINTER_DETAILS_SECTION = (By.ID, "printer_details_section_id")

    def navigate_to_printer_details(self):
        self.click_element(self.PRINTER_DETAILS_SECTION)
