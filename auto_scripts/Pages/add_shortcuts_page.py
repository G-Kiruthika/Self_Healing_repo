from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AddShortcutsPage(BasePage):
    ADD_SHORTCUTS_SECTION = (By.ID, "add_shortcuts_section_id")
    EMAIL_TOGGLE_BAR = (By.ID, "email_toggle_bar_id")
    CONTINUE_BUTTON = (By.ID, "continue_button_id")

    def navigate_to_add_shortcuts(self):
        self.click_element(self.ADD_SHORTCUTS_SECTION)

    def enable_email_destination(self):
        self.click_element(self.EMAIL_TOGGLE_BAR)

    def click_continue(self):
        self.click_element(self.CONTINUE_BUTTON)
