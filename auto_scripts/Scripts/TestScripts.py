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

    def test_TC_LOGIN_002(self):
        """Test Case TC_LOGIN_002: Invalid login shows error message"""
        try:
            error_message = self.login_page.tc_login_002_invalid_login(
                invalid_email='invaliduser@example.com',
                valid_password='ValidPass123!'
            )
            assert error_message is not None, "No error message displayed for invalid login."
            assert 'Invalid username or password' in error_message, f"Unexpected error message: {error_message}"
            print("TC_LOGIN_002 passed: Error message displayed for invalid login.")
        except Exception as e:
            print(f"TC_LOGIN_002 failed: {e}")
            raise

    def test_TC_LOGIN_003(self):
        """Test Case TC_LOGIN_003: Invalid password shows error message"""
        try:
            result = self.login_page.tc_login_003(username="testuser@example.com", password="WrongPassword123")
            assert result, "Error message for invalid password not displayed or incorrect."
            print("TC_LOGIN_003 passed: Error message displayed for invalid password.")
        except Exception as e:
            print(f"TC_LOGIN_003 failed: {e}")
            raise
