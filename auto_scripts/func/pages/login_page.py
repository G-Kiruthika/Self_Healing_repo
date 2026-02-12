from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LoginPage(BasePage):
 """Page Object for Login Page functionality."""
 
 USERNAME_INPUT = (By.ID, "username_input_locator")
 PASSWORD_INPUT = (By.ID, "password_input_locator")
 LOGIN_BUTTON = (By.ID, "login_button_locator")
 ERROR_MESSAGE = (By.ID, "error_message_locator")

 def navigate_to_login_page(self):
 """Navigate to the login page."""
 # Example: self.driver.get("https://example.com/login")
 pass

 def enter_username(self, username):
 """Enter username into the username input field.
 
 Args:
 username (str): The username to enter
 """
 username_element = self.find_element(self.USERNAME_INPUT)
 username_element.clear()
 username_element.send_keys(username)

 def enter_password(self, password):
 """Enter password into the password input field.
 
 Args:
 password (str): The password to enter
 """
 password_element = self.find_element(self.PASSWORD_INPUT)
 password_element.clear()
 password_element.send_keys(password)

 def click_login_button(self):
 """Click the login button."""
 login_btn = self.find_element(self.LOGIN_BUTTON)
 login_btn.click()

 def is_not_logged_in(self):
 """Check if user is not logged in.
 
 Returns:
 bool: True if login button is visible (user not logged in), False otherwise
 """
 return self.is_element_visible(self.LOGIN_BUTTON)

 def is_error_message_displayed(self):
 """Check if error message is displayed.
 
 Returns:
 bool: True if error message is visible, False otherwise
 """
 return self.is_element_visible(self.ERROR_MESSAGE)
