from selenium.webdriver.common.by import By
from auto_scripts.BasePage import BasePage

class RootViewScreen(BasePage):
    def click_printer_icon(self):
        printer_icon = self.driver.find_element(By.ACCESSIBILITY_ID, 'printer_icon')
        printer_icon.click()
