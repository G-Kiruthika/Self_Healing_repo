from selenium.webdriver.common.by import By
from auto_scripts.BasePage import BasePage

class CreateShortcutScreen(BasePage):
    def click_create_your_own_arrow(self):
        create_your_own_arrow_button = self.driver.find_element(By.ACCESSIBILITY_ID, 'create_your_own_arrow_button')
        create_your_own_arrow_button.click()
