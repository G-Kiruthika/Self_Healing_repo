from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.LoginPage import LoginPage

class TC_LOGIN_001_TestPage(LoginPage):
    """
    Test Page for TC_LOGIN_001.
    Orchestrates invalid login test and validates error message.
    Inherits from LoginPage.
    """
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def execute_tc_login_001(self, invalid_email="invalid@test.com", invalid_password="wrongpassword"):
        """
        Executes TC_LOGIN_001: Invalid login and error message validation.
        Args:
            invalid_email (str): Email/username to use for invalid login.
            invalid_password (str): Password to use for invalid login.
        Returns:
            str: Success message if test passes.
        Raises:
            AssertionError: If error message or login page validation fails.
        """
        self.perform_invalid_login_and_validate(invalid_email, invalid_password)
        return "TC_LOGIN_001 executed successfully"