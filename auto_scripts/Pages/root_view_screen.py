from auto_scripts.Pages.base_page import BasePage
from selenium.webdriver.common.by import By

class RootViewScreen(BasePage):
    ROOT_CONTAINER = (By.ID, "root_container")
    TITLE_TEXT = (By.XPATH, "//h1[@class='title']")
    SETTINGS_BUTTON = (By.ID, "settings_btn")

    def click_settings_button(self):
        self.click_element(self.SETTINGS_BUTTON)

    def is_title_visible(self):
        return self.is_element_visible(self.TITLE_TEXT)
