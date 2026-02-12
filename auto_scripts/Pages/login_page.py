from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
 USERNAME_INPUT = (By.ID, "username_input_locator")
 PASSWORD_INPUT = (By.ID, "password_input_locator")
 LOGIN_BUTTON = (By.ID, "login_button_locator")
 ERROR_MESSAGE = (By.ID, "error_message_locator")

 def navigate_to_login_page(self):
 # Example navigation logic, customize as needed
 self.driver.get("https://your-app-url/login")

 def enter_username(self, username):
 self.enter_text(self.USERNAME_INPUT, username)

 def enter_password(self, password):
 self.enter_text(self.PASSWORD_INPUT, password)

 def click_login_button(self):
 self.click_element(self.LOGIN_BUTTON)

 def is_not_logged_in(self):
 # Returns True if login button is visible, indicating not logged in
 return self.is_element_visible(self.LOGIN_BUTTON)

 def is_error_message_displayed(self):
 return self.is_element_visible(self.ERROR_MESSAGE)