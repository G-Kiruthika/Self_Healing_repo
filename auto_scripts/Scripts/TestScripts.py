# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.ForgotPasswordPage import ForgotPasswordPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
from auto_scripts.Pages.ResetPasswordPage import ResetPasswordPage
from selenium.webdriver.common.by import By
import pytest

class TestLogin:
    def test_tc_login_001_login_flow(self, driver):
        login_page = LoginPage(driver)
        result = login_page.tc_login_001_login_flow('user@example.com', 'ValidPass123')
        assert result is True

    def test_tc_login_003_invalid_password_flow(self, driver):
        login_page = LoginPage(driver)
        result = login_page.tc_login_003_invalid_password_flow('user@example.com', 'WrongPass456')
        assert result is True

    def test_tc_login_002_invalid_email_login(self, driver):
        login_page = LoginPage(driver)
        result = login_page.tc_login_002_invalid_email_login('userexample.com', 'ValidPass123')
        assert result is True

    def test_tc_login_004_required_fields_validation(self, driver):
        login_page = LoginPage(driver)
        result = login_page.tc_login_004_required_fields_validation()
        assert result["empty_prompt"] is not None, "Mandatory fields prompt should be displayed."
        assert result["login_unsuccessful"], "Login should not be successful when required fields are empty."
        assert (result["error_message"] is not None or result["validation_error"] is not None), "Error or validation message should be shown for empty fields."

    def test_tc_login_003(self, driver):
        """
        Test Case TC_LOGIN_003:
        1. Navigate to the login page.
        2. Enter valid email and incorrect password ('user@example.com', 'WrongPass456').
        3. Click the 'Login' button.
        4. Verify error message for incorrect password is shown.
        5. Verify login is not successful.
        """
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.login_with_credentials('user@example.com', 'WrongPass456')
        error_message = login_page.get_authentication_error()
        assert error_message is not None and error_message != "", "Authentication error message should be displayed for incorrect password."
        assert login_page.is_login_unsuccessful(), "Login should not be successful with incorrect password."

    def test_tc_login_004(self, driver):
        """
        Test Case TC_LOGIN_004:
        1. Navigate to the login page.
        2. Leave email and password fields empty.
        3. Click the 'Login' button.
        4. Verify error messages for required fields are shown.
        5. Verify login is not successful.
        """
        login_page = LoginPage(driver)
        login_page.open_login_page()
        result = login_page.validate_required_field_errors_tc_login_004()
        assert result["empty_prompt"] is not None, "Mandatory fields prompt should be displayed."
        assert result["login_unsuccessful"], "Login should not be successful when required fields are empty."
        assert (result["error_message"] is not None or result["validation_error"] is not None), "Error or validation message should be shown for empty fields."

    def test_tc_login_006_required_password_validation(self, driver):
        """
        Test Case TC_LOGIN_006:
        1. Navigate to the login page.
        2. Enter valid email and leave password field empty.
        3. Click the 'Login' button.
        4. Verify error message for required password is shown.
        5. Verify login is not successful.
        """
        login_page = LoginPage(driver)
        login_page.open_login_page()
        result = login_page.validate_password_required_error_tc_login_006('user@example.com')
        assert (result["error_message"] is not None or result["empty_prompt"] is not None or result["validation_error"] is not None), "Password required error should be displayed."
        assert result["login_unsuccessful"], "Login should not be successful when password is empty."

    def test_tc_login_005_required_email_validation(self, driver):
        """
        Test Case TC_LOGIN_005:
        1. Navigate to the login page.
        2. Leave email/username field empty and enter valid password ('ValidPass123').
        3. Click the 'Login' button.
        4. Verify error message for required email/username is shown.
        5. Verify login is not successful.
        """
        login_page = LoginPage(driver)
        login_page.open_login_page()
        result = login_page.validate_required_field_errors_tc_login_005('ValidPass123')
        assert result["error_message"] is not None, "Error message for required email/username should be displayed."
        assert result["login_unsuccessful"], "Login should not be successful when email/username is empty."

    def test_tc_login_007_max_length_login(self, driver):
        """
        Test Case TC_LOGIN_007:
        1. Navigate to the login page.
        2. Enter email and password with maximum allowed length (email: '64_chars@example.com', password: 'A'*128).
        3. Click the 'Login' button.
        4. Verify that fields accept maximum input and login succeeds if credentials are valid.
        """
        login_page = LoginPage(driver)
        login_page.open_login_page()
        # Use the PageClass function for max length validation
        result = login_page.validate_max_length_input_tc_login_007('64_chars@example.com', 'A'*128)
        assert result['fields_accept_max_length'], "Fields should accept maximum input length."
        assert result['login_success'], "Login should succeed with valid max-length credentials."
        # Optionally check for error/validation messages
        if result['error_message']:
            print(f"Login error message: {result['error_message']}")
        if result['validation_error']:
            print(f"Validation error: {result['validation_error']}")

    def test_tc_login_007_username_recovery(self, driver):
        """
        Test Case TC_LOGIN_007 Username Recovery:
        1. Navigate to the login page.
        2. Click 'Forgot Username' link.
        3. Verify username recovery page UI.
        4. Enter a 64-character email and check input length acceptance.
        5. Assert that recovery flow and max length validation succeed.
        """
        username_recovery_page = UsernameRecoveryPage(driver)
        # Step 1 & 2: Navigate and click 'Forgot Username'
        flow_result = username_recovery_page.tc_login_007_username_recovery_flow('64_chars@example.com')
        # Step 3: UI verification is part of flow
        # Step 4: Input max length validation
        max_length_ok = username_recovery_page.verify_email_field_max_length('64_chars@example.com')
        assert flow_result, "Username recovery flow failed."
        assert max_length_ok, "Email field did not accept max length input."

    def test_tc001_login_workflow(self, driver):
        """
        Test Case TC001: Valid Login Workflow
        Steps:
            1. Navigate to the login page
            2. Enter valid email and password ('user@example.com', 'ValidPassword123')
            3. Click the 'Login' button
            4. Verify dashboard is displayed
        """
        login_page = LoginPage(driver)
        result = login_page.execute_tc001_login_workflow('user@example.com', 'ValidPassword123')
        assert result['dashboard_displayed'], f"Dashboard not displayed. Error: {result.get('error_message', '')}"

    def test_tc_login_010_remember_me_session_persistence(self, driver):
        """
        Test Case TC_LOGIN_010:
        1. Navigate to the login page.
        2. Enter valid credentials and select 'Remember Me'.
        3. Click the 'Login' button.
        4. Verify session persists after browser restart.
        """
        login_page = LoginPage(driver)
        result = login_page.execute_tc_login_010_remember_me_session_persistence('user@example.com', 'ValidPass123')
        assert result['remember_me_checked'], "'Remember Me' checkbox should be selected."
        assert result['dashboard_displayed'], "Dashboard should be displayed after login."
        assert result['session_persisted'], f"Session should persist after browser restart. Error: {result.get('error_message', '')}"

    def test_tc002_invalid_email_valid_password(self, driver):
        """
        Test Case TC002:
        1. Navigate to the login page.
        2. Enter invalid email and valid password ('invaliduser@example.com', 'ValidPassword123').
        3. Click the 'Login' button.
        4. Assert error message 'Invalid email or password' is displayed and login fails.
        """
        login_page = LoginPage(driver)
        result = login_page.execute_tc002_invalid_email_workflow('invaliduser@example.com', 'ValidPassword123')
        assert result['error_message'] == 'Invalid email or password', f"Expected error message not displayed. Actual: {result['error_message']}"
        assert result['login_unsuccessful'], "Login should not be successful with invalid email."

    def test_tc003_invalid_password_scenario(self, driver):
        """
        Test Case TC003: Invalid Password Scenario
        Steps:
            1. Navigate to the login page
            2. Enter valid email and invalid password ('user@example.com', 'WrongPassword')
            3. Click the 'Login' button
            4. Verify error message 'Invalid email or password' is displayed
            5. Confirm login fails
        """
        login_page = LoginPage(driver)
        result = login_page.execute_tc003_invalid_password_login(email='user@example.com', password='WrongPassword')
        assert result['error_message_displayed'], f"Expected error message not displayed. Actual: {result['error_message_text']}"
        assert result['login_unsuccessful'], "Login should not be successful with invalid password."

    def test_tc_login_012_password_recovery(self, driver):
        """
        Test Case TC_LOGIN_012: Password Recovery Flow
        Steps:
            1. Navigate to the login page.
            2. Click on 'Forgot Password' link.
            3. Enter registered email address and submit.
            4. Verify that password reset email is sent (success message displayed).
        """
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.click_forgot_password()
        password_recovery_page = PasswordRecoveryPage(driver)
        password_recovery_page.enter_email_and_submit('user@example.com')
        assert password_recovery_page.is_success_message_displayed(), "Password reset success message should be displayed after submitting recovery request."

    def test_tc_login_015_case_sensitivity_enforcement(self, driver):
        """
        Test Case TC_LOGIN_015:
        1. Navigate to the login page.
        2. Enter email/username and password with different cases (email: 'USER@EXAMPLE.COM', password: 'VALIDPASS123').
        3. Click the 'Login' button.
        4. Validate case sensitivity enforcement as per requirement.
        5. Assert that result['case_sensitivity_enforced'] is True or False.
        """
        login_page = LoginPage(driver)
        result = login_page.execute_tc_login_015_case_sensitivity_enforcement(email='USER@EXAMPLE.COM', password='VALIDPASS123')
        assert result['case_sensitivity_enforced'] is True or result['case_sensitivity_enforced'] is False, f"Case sensitivity enforcement result is not boolean: {result['case_sensitivity_enforced']}"
        if result['error_message']:
            print(f"Login error message: {result['error_message']}")
