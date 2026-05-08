# RootViewScreen: Root view screen of the HPX app.
from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class RootViewScreen(BasePage):
    PRINTER_ICON = By.XPATH, 'placeholder_locator'
    SHORTCUTS_TILE = By.XPATH, 'placeholder_locator'

    def click_printer_icon(self):
        return self.click(self.PRINTER_ICON)

    def click_shortcuts_tile(self):
        return self.click(self.SHORTCUTS_TILE)

    def is_printer_icon_visible(self):
        return self.is_visible(self.PRINTER_ICON)

    def is_shortcuts_tile_visible(self):
        return self.is_visible(self.SHORTCUTS_TILE)
