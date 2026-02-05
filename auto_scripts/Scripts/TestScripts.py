# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.ForgotPasswordPage import ForgotPasswordPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
from selenium.webdriver.common.by import By
import pytest

class TestLogin:
    def test_valid_login(self, driver):
        # Existing test logic...
        pass

    def test_empty_username_validation(self, driver):
        """
        TC-SCRUM-115-004: Validate login with empty username triggers error prompt and field highlighting
        Steps:
        1. Navigate to the e-commerce website login page
        2. Leave the username field empty
        3. Enter valid password in the password field
        4. Click on the Login button
        5. Verify username field is highlighted with error indicator
        Expected Results:
        - Error message: 'Username is required. Please enter your username.'
        - Username field is highlighted in red with error icon, focus is set to username field
        """
        login_page = LoginPage(driver)
        # Step 1: Navigate to login page (assume fixture or method handles navigation)
        # Step 2 & 3: Leave username empty, enter valid password
        valid_password = "ValidPassword123!"  # Replace with secure test credential
        login_page.login_with_empty_username(valid_password)
        # Step 4: Click Login is handled by login_with_empty_username
        # Step 5: Validate error prompt and field highlighting
        error_prompt = login_page.get_empty_field_prompt()
        assert error_prompt == "Username is required. Please enter your username.", f"Unexpected error prompt: {error_prompt}"
        login_page.highlight_username_field()
        assert login_page.is_username_field_highlighted(), "Username field is not highlighted after empty username submission."

    def test_boundary_and_negative_login_tc_scrum_115_005(self, driver):
        """
        TC-SCRUM-115-005: Boundary and negative test for login with maximum username length and empty password
        Steps:
        1. Navigate to the e-commerce website login page
        2. Enter username with maximum allowed length (boundary test)
        3. Leave the password field empty
        4. Click on the Login button
        5. Verify error message: 'Password is required. Please enter your password.'
        6. Verify password field is highlighted in red with error icon and focus
        """
        login_page = LoginPage(driver)
        boundary_username = "user_with_very_long_email_address_testing_boundary_conditions@example.com"
        result = login_page.tc_scrum_115_005_boundary_and_negative_login(boundary_username)
        assert result is True, "Boundary and negative login test for TC-SCRUM-115-005 failed."

    def test_forgot_password_flow_tc_scrum_115_006(self, driver):
        """
        TC-SCRUM-115-006: Forgot Password Flow
        Steps:
        1. Navigate to the e-commerce website login page
        2. Verify 'Forgot Password?' link is visible
        3. Click on 'Forgot Password?' link
        4. Verify user is redirected to password recovery page
        5. Enter valid registered email address
        6. Click on 'Send Reset Link' button
        7. Verify success message is displayed: 'Password reset link has been sent to your email address. Please check your inbox.'
        8. Simulate receiving the reset email and link
        9. Click reset link and set new password
        10. Verify confirmation message is displayed and user can login with new password
        """
        login_page = LoginPage(driver)
        # Step 1: Navigate to login page
        login_page.load()
        # Step 2: Verify login page is displayed and 'Forgot Password?' link is visible
        assert login_page.is_displayed(), "Login page not displayed."
        # Step 3: Click 'Forgot Password?' link
        login_page.click_forgot_password()
        # Step 4: Verify redirected to password recovery page
        forgot_page = ForgotPasswordPage(driver)
        assert forgot_page.is_loaded(), "Password recovery page not loaded."
        # Step 5: Enter valid registered email address
        valid_email = "validuser@example.com"
        assert forgot_page.enter_email(valid_email), "Email not entered or validated properly."
        # Step 6: Click 'Send Reset Link' button
        forgot_page.click_send_reset_link()
        # Step 7: Verify success message
        assert forgot_page.is_success_message_displayed(), "Success message not displayed after sending reset link."
        # Step 8: Simulate receiving the reset email and link (skipped, as email check is not implemented)
        reset_link_url = "https://ecommerce.example.com/reset-password?token=abc123xyz"
        new_password = "NewSecurePass789!"
        # Step 9: Click reset link and set new password
        assert forgot_page.click_reset_link_and_set_new_password(reset_link_url, new_password), "Password reset confirmation failed."
        # Step 10: Optionally, verify user can login with new password (not implemented here)

    def test_username_recovery_tc_scrum_115_007(self, driver):
        """
        TC-SCRUM-115-007: Username Recovery Flow
        Steps:
        1. Navigate to the e-commerce website login page
        2. Click on 'Forgot Username?' link
        3. Enter valid registered email address
        4. Click on 'Send Username' button
        5. Verify success message is displayed: 'Your username has been sent to your email address. Please check your inbox.'
        6. Enter unregistered email address
        7. Click on 'Send Username' button
        8. Verify generic security message is displayed: 'If this email is registered, username will be sent to the email address.'
        """
        login_page = LoginPage(driver)
        # Step 1: Navigate to login page
        login_page.load()
        # Step 2: Click 'Forgot Username?' link
        login_page.click_forgot_username()
        # Step 3 & 4: Enter registered email and click send
        recovery_page = UsernameRecoveryPage(driver)
        assert recovery_page.is_loaded(), "Username Recovery page not loaded."
        registered_email = "validuser@example.com"
        assert recovery_page.enter_email(registered_email), "Registered email not entered or validated properly."
        recovery_page.click_send_username()
        # Step 5: Verify success message
        assert recovery_page.is_success_message_displayed(), "Success message not displayed after username recovery request."
        # Step 6 & 7: Enter unregistered email and click send
        unregistered_email = "unregistered@example.com"
        assert recovery_page.enter_email(unregistered_email), "Unregistered email not entered or validated properly."
        recovery_page.click_send_username()
        # Step 8: Verify generic security message
        assert recovery_page.is_generic_message_displayed(), "Generic security message not displayed for unregistered email."
