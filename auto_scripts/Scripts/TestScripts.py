# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.ForgotPasswordPage import ForgotPasswordPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
from selenium.webdriver.common.by import By
import pytest

class TestLogin:
    def test_valid_login(self, driver):
        # Existing test logic...
        pass

    def test_TC_LOGIN_007_forgot_password_flow(self, driver):
        """
        Test Case TC_LOGIN_007: Forgot Password flow
        Steps:
        1. Navigate to the login page
        2. Click the 'Forgot Password' link
        3. Enter registered email address
        4. Click Submit
        5. Verify success message displayed and password reset email sent
        """
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        assert login_page.is_login_page_displayed(), "Login page is not displayed."

        login_page.click_forgot_password()
        recovery_page = PasswordRecoveryPage(driver)
        assert recovery_page.is_forgot_password_page_displayed(), "Forgot password page is not displayed."

        recovery_page.enter_email("testuser@example.com")
        recovery_page.click_submit()
        assert recovery_page.verify_success_message(), "Success message not displayed or password reset email not sent."

    def test_TC_LOGIN_012_sql_injection_prevention(self, driver):
        """
        Test Case TC-LOGIN-012: SQL Injection Prevention
        Steps:
        1. Instantiate LoginPage with driver
        2. Call perform_sql_injection_test with email_payload="admin' OR '1'='1", password="password123", expected_error="Invalid credentials"
        3. Assert error message is shown and unauthorized access is prevented
        """
        login_page = LoginPage(driver)
        result = login_page.perform_sql_injection_test(
            email_payload="admin' OR '1'='1",
            password="password123",
            expected_error="Invalid credentials"
        )
        assert result['verify_error_message'], "Error message for SQL injection not displayed."
        assert result['verify_no_unauthorized_access'], "Unauthorized access was not prevented during SQL injection test."
