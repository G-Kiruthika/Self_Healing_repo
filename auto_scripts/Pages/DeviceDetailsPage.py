from selenium.webdriver.common.by import By
from auto_scripts.BasePage import BasePage

class DeviceDetailsPage(BasePage):
    def click_shortcuts_tile(self):
        shortcuts_tile = self.driver.find_element(By.ACCESSIBILITY_ID, 'shortcuts_tile')
        shortcuts_tile.click()
