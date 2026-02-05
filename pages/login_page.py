# login_page.py
"""
LoginPage class for handling user authentication.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'loginBtn')
    SIGNOUT_BUTTON = (By.ID, 'signoutBtn')

    def login(self, username, password):
        """
        Logs in the user with the provided credentials.
        """
        self.enter_text(*self.USERNAME_INPUT, text=username)
        self.enter_text(*self.PASSWORD_INPUT, text=password)
        self.click(*self.LOGIN_BUTTON)

    def sign_out(self):
        """
        Signs out the current user.
        """
        self.click(*self.SIGNOUT_BUTTON)
