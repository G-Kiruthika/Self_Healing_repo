from selenium.webdriver.common.by import By
from auto_scripts.Pages.BasePage import BasePage

class PopUpScreen(BasePage):
    GO_BACK_BUTTON = (By.XPATH, "//android.widget.Button[@content-desc='GoBack']")
    YES_CANCEL_BUTTON = (By.XPATH, "//android.widget.Button[@content-desc='YesCancel']")

    def click_go_back_button(self):
        self.click(self.GO_BACK_BUTTON)

    def click_yes_cancel_button(self):
        self.click(self.YES_CANCEL_BUTTON)

    def is_go_back_button_visible(self):
        return self.is_visible(self.GO_BACK_BUTTON)

    def is_yes_cancel_button_visible(self):
        return self.is_visible(self.YES_CANCEL_BUTTON)
