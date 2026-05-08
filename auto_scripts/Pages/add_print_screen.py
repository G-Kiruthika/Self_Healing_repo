from auto_scripts.Pages.base_page import BasePage
from selenium.webdriver.common.by import By

class AddPrintScreen(BasePage):
    PRINT_NAME_INPUT = (By.ID, "print_name_input")
    ADD_PRINT_BUTTON = (By.ID, "add_print_btn")

    def enter_print_name(self, name):
        self.enter_text(self.PRINT_NAME_INPUT, name)

    def click_add_print_button(self):
        self.click_element(self.ADD_PRINT_BUTTON)

    def is_print_name_input_visible(self):
        return self.is_element_visible(self.PRINT_NAME_INPUT)
