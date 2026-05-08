from selenium.webdriver.common.by import By
from auto_scripts.BasePage import BasePage

class AddShortcutScreen(BasePage):
    def enable_email_destination_toggle(self):
        email_destination_toggle = self.driver.find_element(By.ACCESSIBILITY_ID, 'email_destination_toggle')
        email_destination_toggle.click()

    def click_continue(self):
        continue_button = self.driver.find_element(By.ACCESSIBILITY_ID, 'continue_button')
        continue_button.click()

    def verify_screen(self):
        add_email_screen = self.driver.find_element(By.ACCESSIBILITY_ID, 'add_email_screen')
        assert add_email_screen is not None, "User should be navigated to the 'Add Email' screen."
