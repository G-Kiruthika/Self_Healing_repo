from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_page import BasePage

class LoginPage(BasePage):
 USERNAME_INPUT = (By.ID, "username_input_locator")
 PASSWORD_INPUT = (By.ID, "password_input_locator")
 LOGIN_BUTTON = (By.ID, "login_button_locator")
 ERROR_MESSAGE = (By.ID, "error_message_locator")

 def navigate_to_login_page(self):
 # Example: self.driver.get("https://example.com/login")
 pass

 def enter_username(self, username):
 username_element = self.find_element(self.USERNAME_INPUT)
 username_element.clear()
 username_element.send_keys(username)

 def enter_password(self, password):
 password_element = self.find_element(self.PASSWORD_INPUT)
 password_element.clear()
 password_element.send_keys(password)

 def click_login_button(self):
 login_btn = self.find_element(self.LOGIN_BUTTON)
 login_btn.click()

 def is_not_logged_in(self):
 # Returns True if login button is visible, i.e., user is not logged in
 return self.is_element_visible(self.LOGIN_BUTTON)

 def is_error_message_displayed(self):
 return self.is_element_visible(self.ERROR_MESSAGE)

 # Wrappers from BasePage assumed to be:
 # def find_element(self, locator): ...
 # def is_element_visible(self, locator): ...
