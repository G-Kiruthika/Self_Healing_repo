from selenium.webdriver.common.by import By
from auto_scripts.Pages.BasePage import BasePage

class RootViewScreen(BasePage):
    PRINTER_ICON = (By.XPATH, "//android.widget.ImageView[@content-desc='Printer']")

    def click_printer_icon(self):
        self.click(self.PRINTER_ICON)

    def is_printer_icon_visible(self):
        return self.is_visible(self.PRINTER_ICON)
