from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.LoginPage import LoginPage

class TC_LOGIN_001_TestPage(LoginPage):
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def execute_tc_login_001(self, invalid_email="invalid@test.com", invalid_password="wrongpassword"):
        self.perform_invalid_login_and_validate(invalid_email, invalid_password)
        return "TC_LOGIN_001 executed successfully"