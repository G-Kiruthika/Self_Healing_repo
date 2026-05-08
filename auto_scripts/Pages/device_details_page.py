from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class DeviceDetailsPage(BasePage):
    # Locators
    shortcuts_tile = (By.ID, 'shortcuts_tile_id_placeholder')

    # Actions
    def click_shortcuts_tile(self):
        self.driver.find_element(*self.shortcuts_tile).click()
