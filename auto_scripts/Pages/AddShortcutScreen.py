from selenium.webdriver.common.by import By
from auto_scripts.Pages.BasePage import BasePage

class AddShortcutScreen(BasePage):
    CREATE_OWN_SHORTCUT_ARROW = (By.XPATH, "//android.widget.ImageView[@content-desc='CreateOwnShortcutArrow']")
    BACK_BUTTON = (By.XPATH, "//android.widget.Button[@content-desc='Back']")

    def click_create_own_shortcut_arrow(self):
        self.click(self.CREATE_OWN_SHORTCUT_ARROW)

    def click_back_button(self):
        self.click(self.BACK_BUTTON)

    def is_create_own_shortcut_arrow_visible(self):
        return self.is_visible(self.CREATE_OWN_SHORTCUT_ARROW)

    def is_back_button_visible(self):
        return self.is_visible(self.BACK_BUTTON)
