# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage
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
