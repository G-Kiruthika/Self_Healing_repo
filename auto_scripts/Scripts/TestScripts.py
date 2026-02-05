# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.ForgotPasswordPage import ForgotPasswordPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
from auto_scripts.Pages.ResetPasswordPage import ResetPasswordPage
from selenium.webdriver.common.by import By
import pytest

class TestLogin:
    def test_valid_login(self, driver):
        # Existing test logic...
        pass

    def test_TC_LOGIN_007_forgot_password_flow(self, driver):
        # ...
        pass

    def test_TC_LOGIN_012_sql_injection_prevention(self, driver):
        # ...
        pass

    def test_TC_SCRUM_115_006_forgot_password_flow(self, driver):
        # ...
        pass

    def test_TC_SCRUM_115_003_account_lockout(self, driver):
        # ...
        pass

    def test_TC_LOGIN_008_forgot_password_unregistered_email_flow(self, driver):
        # ...
        pass

    def test_TC_LOGIN_013_sql_injection_prevention(self, driver):
        """
        Test Case TC-LOGIN-013: SQL Injection Prevention
        Steps:
        1. Navigate to the login page [Test Data: URL: https://ecommerce.example.com/login]
        2. Enter valid email address [Test Data: Email: testuser@example.com]
        3. Enter SQL injection payload in password field [Test Data: Password: ' OR '1'='1' --]
        4. Click on the Login button
        5. Verify no unauthorized access is granted
        Acceptance Criteria: TS-011
        """
        login_page = LoginPage(driver)
        result = login_page.tc_login_013_sql_injection_prevention(
            email="testuser@example.com",
            sql_injection_password="' OR '1'='1' --"
        )
        assert result, "SQL injection prevention test failed: Unauthorized access or improper error handling."

    def test_TC_LOGIN_009_forgot_username_flow(self, driver):
        """
        Test Case TC_LOGIN_009: Username Recovery
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Click on 'Forgot Username' link
        3. Enter registered email address [Test Data: Email: testuser@example.com]
        4. Click on Submit button
        5. Assert that the success message is displayed and username reminder email is sent
        """
        username_recovery_page = UsernameRecoveryPage(driver)
        result = username_recovery_page.tc_login_009_forgot_username_flow(email="testuser@example.com")
        assert result, "Username recovery test failed: Success message not displayed or email not sent."

    def test_TC_LOGIN_011_max_length_username(self, driver):
        """
        Test Case TC_LOGIN_011: Login with maximum allowed username length (255 characters)
        Steps:
        1. Navigate to the login page [Test Data: URL: https://ecommerce.example.com/login]
        2. Enter username with maximum allowed length (255 characters) [Test Data: Username: a_very_long_username_with_exactly_255_characters_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@example.com]
        3. Enter valid password [Test Data: Password: ValidPass123!]
        4. Click on the Login button
        5. Validate the login attempt is processed
        Acceptance Criteria: AC_006
        """
        login_page = LoginPage(driver)
        username = "a_very_long_username_with_exactly_255_characters_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@example.com"
        password = "ValidPass123!"
        result = login_page.tc_login_011_max_length_username(username, password)
        assert result, "Max username length login test failed: Login attempt not processed as expected."

    def test_TC_LOGIN_014_locked_account(self, driver):
        """
        Test Case TC-LOGIN-014: Locked Account Login Attempt
        Steps:
        1. Navigate to the login page [URL: https://ecommerce.example.com/login]
        2. Enter email of a locked account [Email: lockeduser@example.com]
        3. Enter correct password for the locked account [Password: CorrectPassword123!]
        4. Click the Login button.
        5. Verify error message: 'Your account has been locked. Please contact support.'
        6. Verify user is not authenticated and remains on login page.
        """
        login_page = LoginPage(driver)
        result = login_page.tc_login_014_locked_account_login(
            email="lockeduser@example.com",
            password="CorrectPassword123!"
        )
        assert result, "Locked account login test failed: Error message not shown or user was authenticated."

    def test_TC_LOGIN_010_max_length_username(self, driver):
        """
        Test Case TC_LOGIN_010: Login with maximum allowed username length (255 characters)
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter username with maximum allowed length (255 characters) [Test Data: Username: 'a'*243 + '@example.com']
        3. Enter valid password [Test Data: Password: ValidPass123!]
        4. Click on the Login button
        5. Verify system processes login attempt without field length errors
        Acceptance Criteria: AC_SCRUM-114_006
        """
        login_page = LoginPage(driver)
        username = "{}@example.com".format('a'*243)
        password = "ValidPass123!"
        result = login_page.tc_login_010_login_with_max_length_username(username, password)
        assert result, "Max username length login test failed: Login attempt not processed as expected."

    def test_TC_LOGIN_012_min_length_username(self, driver):
        """
        Test Case TC_LOGIN_012: Login with minimum allowed username length (3 characters)
        Steps:
        1. Navigate to the login page [Test Data: URL: https://ecommerce.example.com/login]
        2. Enter username with minimum allowed length (3 characters) [Test Data: Username: abc]
        3. Enter valid password [Test Data: Password: ValidPass123!]
        4. Click on the Login button
        5. Verify login is processed and dashboard/user icon is displayed
        Acceptance Criteria: AC_006
        """
        login_page = LoginPage(driver)
        result = login_page.tc_login_012_min_length_username_login()
        assert result, "Min username length login test failed: Login attempt not processed as expected."

    def test_TC_LOGIN_015_unverified_account(self, driver):
        """
        Test Case TC-LOGIN-015: Login Attempt with Unverified Account
        Steps:
            1. Navigate to the login page [Test Data: URL: https://ecommerce.example.com/login]
            2. Enter email of an unverified account [Test Data: Email: unverified@example.com]
            3. Enter correct password [Test Data: Password: ValidPass123!]
            4. Click on the Login button
            5. Verify error message: 'Please verify your email address before logging in.'
            6. Verify user remains on login page with option to resend verification email
        Acceptance Criteria: Error message shown, resend verification link present, user not authenticated.
        """
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.enter_email("unverified@example.com")
        login_page.enter_password("ValidPass123!")
        login_page.click_login()
        error_displayed = login_page.is_unverified_error_displayed()
        resend_option = login_page.click_resend_verification()
        assert error_displayed, "Unverified account error message not displayed."
        assert resend_option, "Resend verification option not available or not clickable."

    def test_TC_LOGIN_013_max_length_password(self, driver):
        """
        Test Case TC_LOGIN_013: Login with maximum allowed password length (128 characters)
        Steps:
        1. Navigate to the login page [Test Data: URL: https://ecommerce.example.com/login]
        2. Enter valid username [Test Data: Username: testuser@example.com]
        3. Enter password with maximum allowed length (128 characters) [Test Data: Password: Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!]
        4. Click on the Login button
        5. Verify login is processed and dashboard/user icon is displayed
        Acceptance Criteria: AC_006
        """
        login_page = LoginPage(driver)
        username = "testuser@example.com"
        max_length_password = "Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!"
        result = login_page.tc_login_013_max_length_password_login(username, max_length_password)
        assert result, "Max password length login test failed: Login attempt not processed as expected."

    def test_TC_LOGIN_014_special_char_username(self, driver):
        """
        Test Case TC_LOGIN_014: Login with Username Containing Special Characters
        Steps:
            1. Navigate to the login page [Test Data: URL: https://ecommerce.example.com/login]
            2. Enter username with special characters [Test Data: Username: test.user+tag@example.com]
            3. Enter valid password [Test Data: Password: ValidPass123!]
            4. Click on the Login button
            5. Validate system response: username is accepted and login is processed correctly (dashboard header and profile icon visible)
        Acceptance Criteria: AC_007
        """
        login_page = LoginPage(driver)
        result = login_page.tc_login_014_special_char_username_login()
        assert result, "Special character username login test failed: Username not accepted or login not processed correctly."
