from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DeviceDetailsPage(BasePage):
    SHORTCUTS_TILE = (By.ID, "placeholder_shortcuts_tile_id")

    def __init__(self, driver):
        super().__init__(driver)

    def click_shortcuts_tile(self):
        self.click_element(self.SHORTCUTS_TILE)