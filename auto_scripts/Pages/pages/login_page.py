from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
 USERNAME_INPUT = ("placeholder", "username_input_locator")
 PASSWORD_INPUT = ("placeholder", "password_input_locator")
 LOGIN_BUTTON = ("placeholder", "login_button_locator")
 ERROR_MESSAGE = ("placeholder", "error_message_locator")

 def navigate_to_login_page(self):
 # Replace with actual navigation logic, e.g., self.driver.get(url)
 self.go_to("/login")

 def enter_username(self, username):
 self.enter_text(self.USERNAME_INPUT, username)

 def enter_password(self, password):
 self.enter_text(self.PASSWORD_INPUT, password)

 def click_login_button(self):
 self.click(self.LOGIN_BUTTON)

 def is_not_logged_in(self):
 return self.is_visible(self.USERNAME_INPUT) and self.is_visible(self.PASSWORD_INPUT)

 def is_error_message_displayed(self):
 return self.is_visible(self.ERROR_MESSAGE)
