from selenium.webdriver.common.by import By
from auto_scripts.Pages.BasePage import BasePage

class DeviceDetailsPage(BasePage):
    SHORTCUTS_TILE = (By.XPATH, "//android.widget.FrameLayout[@content-desc='ShortcutsTile']")

    def click_shortcuts_tile(self):
        self.click(self.SHORTCUTS_TILE)

    def is_shortcuts_tile_visible(self):
        return self.is_visible(self.SHORTCUTS_TILE)
