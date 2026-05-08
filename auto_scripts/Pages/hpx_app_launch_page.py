from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HpxAppLaunchPage(BasePage):
    LAUNCH_BUTTON = (By.ID, "launch_button_id")

    def launch_app(self):
        self.click_element(self.LAUNCH_BUTTON)
