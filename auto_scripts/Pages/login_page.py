from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "username_input")
    PASSWORD_FIELD = (By.ID, "password_input")
    LOGIN_BUTTON = (By.ID, "login_btn")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        """
        Performs login with username and password.
        Args:
            username (str): Username to enter
            password (str): Password to enter
        """
        self.enter_text(self.USERNAME_FIELD, username)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click_element(self.LOGIN_BUTTON)

    def logout(self):
        """
        Performs logout action.
        """
        # Implementation for logout
        pass

    def is_logged_in(self):
        """
        Validates if user is logged in.
        Returns:
            bool: True if logged in, False otherwise
        """
        # Check for dashboard or profile element
        return self.is_element_visible((By.ID, "dashboard-header"))
