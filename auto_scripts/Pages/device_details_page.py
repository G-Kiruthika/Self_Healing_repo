from auto_scripts.Pages.base_page import BasePage
from selenium.webdriver.common.by import By

class DeviceDetailsPage(BasePage):
    DEVICE_NAME = (By.ID, "device_name")
    DEVICE_STATUS = (By.XPATH, "//span[@class='status']")
    EDIT_BUTTON = (By.ID, "edit_btn")

    def click_edit_button(self):
        self.click_element(self.EDIT_BUTTON)

    def is_device_status_visible(self):
        return self.is_element_visible(self.DEVICE_STATUS)
