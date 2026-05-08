from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class AddShortcutScreen(BasePage):
    # Locators
    email_toggle = (By.ID, 'email_toggle_id_placeholder')
    continue_button = (By.ID, 'continue_button_id_placeholder')

    # Actions
    def enable_email_toggle(self):
        toggle = self.driver.find_element(*self.email_toggle)
        if not toggle.is_selected():
            toggle.click()

    def disable_email_toggle(self):
        toggle = self.driver.find_element(*self.email_toggle)
        if toggle.is_selected():
            toggle.click()

    # Validations
    def is_continue_button_enabled(self):
        button = self.driver.find_element(*self.continue_button)
        return button.is_enabled()

    def is_continue_button_disabled(self):
        button = self.driver.find_element(*self.continue_button)
        return not button.is_enabled()
