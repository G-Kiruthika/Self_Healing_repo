# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
from auto_scripts.Pages.ProfilePage import ProfilePage
from auto_scripts.Pages.DashboardPage import DashboardPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.password_recovery_page = PasswordRecoveryPage(driver)
        self.username_recovery_page = UsernameRecoveryPage(driver)
        self.profile_page = ProfilePage(driver)
        self.dashboard_page = DashboardPage(driver)

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

    def test_TC_SCRUM_115_001(self):
        """Test Case TC-SCRUM-115-001: Valid login establishes user session"""
        try:
            # Step 1: Navigate to login page
            self.login_page.load()
            assert self.login_page.is_displayed(), "Login page not displayed."
            # Step 2: Enter valid username
            self.login_page.enter_email('validuser@example.com')
            # Step 3: Enter valid password
            self.login_page.enter_password('ValidPass123!')
            # Step 4: Click login
            self.login_page.click_login()
            # Step 5: Verify dashboard is displayed
            assert self.login_page.is_dashboard_displayed(), "Dashboard not displayed after login."
            # Step 6: Verify user profile icon is displayed
            assert self.login_page.is_user_profile_icon_displayed(), "User profile icon not displayed after login."
            # Step 7: Verify user profile name is displayed and session cookie exists
            assert self.profile_page.is_profile_name_displayed(), "Profile name not displayed."
            session_cookie = self.profile_page.get_session_cookie()
            assert session_cookie is not None, "Session cookie not found."
            print("TC-SCRUM-115-001 passed: User session established and verified.")
        except Exception as e:
            print(f"TC-SCRUM-115-001 failed: {e}")
            raise

    def test_TC_LOGIN_004(self):
        """Test Case TC_LOGIN_004: Validation when username and password are empty"""
        try:
            result = self.login_page.validate_empty_fields_error()
            assert result, "Validation error for empty username and password not displayed or incorrect."
            print("TC_LOGIN_004 passed: Correct error message displayed for empty username and password.")
        except Exception as e:
            print(f"TC_LOGIN_004 failed: {e}")
            raise

    def test_TC_LOGIN_005(self):
        """Test Case TC_LOGIN_005: Validation when username is empty and password is valid"""
        try:
            result = self.login_page.validate_empty_username_error(valid_password="ValidPass123!")
            assert result, "Validation error for empty username not displayed or incorrect."
            print("TC_LOGIN_005 passed: Correct error message displayed for empty username and valid password.")
        except Exception as e:
            print(f"TC_LOGIN_005 failed: {e}")
            raise
