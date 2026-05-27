from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AddNewShortcutsPage(BasePage):
    CREATE_YOUR_OWN_SHORTCUT_ARROW = (By.ID, "placeholder_create_shortcut_arrow_id")

    def __init__(self, driver):
        super().__init__(driver)

    def click_create_your_own_shortcut_arrow(self):
        self.click_element(self.CREATE_YOUR_OWN_SHORTCUT_ARROW)