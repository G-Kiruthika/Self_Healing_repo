# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.password_recovery_page = PasswordRecoveryPage(driver)
        self.username_recovery_page = UsernameRecoveryPage(driver)

    def test_TC_LOGIN_001(self):
        """Test Case TC_LOGIN_001: Valid login redirects to dashboard"""
        try:
            self.login_page.go_to()
            self.login_page.enter_username('testuser@example.com')
            self.login_page.enter_password('ValidPass123!')
            self.login_page.click_login()
            assert self.login_page.is_dashboard_displayed(), "Dashboard was not displayed after login."
            print("TC_LOGIN_001 passed: Dashboard displayed after valid login.")
        except Exception as e:
            print(f"TC_LOGIN_001 failed: {e}")
            raise
