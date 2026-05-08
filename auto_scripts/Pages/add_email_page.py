from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AddEmailPage(BasePage):
    TO_SECTION = (By.ID, "to_section_id")
    ADD_TO_SHORTCUT_BUTTON = (By.ID, "add_to_shortcut_button_id")

    def enter_email_address(self, email):
        self.enter_text(self.TO_SECTION, email)

    def click_add_to_shortcut(self):
        self.click_element(self.ADD_TO_SHORTCUT_BUTTON)

    def verify_error_message(self):
        return self.is_element_visible(self.TO_SECTION)

    def verify_shortcut_saved(self):
        return self.is_element_visible(self.ADD_TO_SHORTCUT_BUTTON)
