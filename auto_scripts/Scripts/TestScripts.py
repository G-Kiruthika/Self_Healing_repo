# Existing imports
import pytest
from auto_scripts.Pages.TC_LOGIN_006_TestPage import TC_LOGIN_006_TestPage
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.LoginPage_PasswordVisibilityToggle import LoginPagePasswordVisibilityToggle

# ... (existing test methods) ...

def test_tc_login_006_remember_me_persistence():
    """
    TC_LOGIN_006: Validating 'Remember Me' session persistence on login.
    Steps:
    1. Navigate to login page
    2. Enter valid credentials
    3. Check 'Remember Me'
    4. Click Login
    5. Close and reopen browser, revisit site, and validate session persistence
    """
    # Instantiate the page class
    test_page = TC_LOGIN_006_TestPage()
    # Run the test case workflow
    result = test_page.run_tc_login_006('validuser@example.com', 'ValidPass123!')
    # Assert that the test case passed overall
    assert result['overall_pass'] is True, f"TC_LOGIN_006 failed: {result}"


def test_tc_login_007_account_lock_after_failed_attempts(driver):
    """
    TC_LOGIN_007: Validate account lock after repeated invalid login attempts.
    Steps:
    1. Navigate to login page
    2. Enter valid username and invalid password, repeat 5 times
    3. Validate error message for each failed login
    4. Attempt login with valid credentials after 5 failures
    5. Validate account lock message
    """
    # Test data
    email = 'validuser@example.com'
    invalid_passwords = ['WrongPass1!', 'WrongPass2!', 'WrongPass3!', 'WrongPass4!', 'WrongPass5!']
    valid_password = 'ValidPass123!'

    # Instantiate LoginPage
    login_page = LoginPage(driver)
    # Run TC_LOGIN_007
    result = login_page.run_tc_login_007(email, invalid_passwords, valid_password)
    # Assert overall pass
    assert result['overall_pass'] is True, f"TC_LOGIN_007 failed: {result}"


def test_tc_login_008_password_visibility_toggle(driver):
    """
    TC_LOGIN_008: Password visibility toggle (eye icon) on the login page.
    Steps:
    1. Navigate to the e-commerce website login page
    2. Enter password in the password field
    3. Click on the eye icon to show password
    4. Click on the eye icon again to hide password
    Validates password masking/unmasking as per AC_008.
    """
    # Navigate to login page (assuming driver.get is available)
    driver.get('https://ecommerce.example.com/login')

    # Instantiate the page object
    login_page_toggle = LoginPagePasswordVisibilityToggle(driver)

    # Validate all required fields are present
    login_page_toggle.validate_all_fields()

    # Enter password
    login_page_toggle.enter_password('ValidPass123!')

    # Initially, password should be masked
    password_field = login_page_toggle._get_element('password_field')
    assert password_field.get_attribute('type') == 'password', 'Password should be masked initially.'

    # Click eye icon to show password
    login_page_toggle.toggle_password_visibility()
    assert login_page_toggle.is_password_visible(), 'Password should be visible after toggling.'

    # Click eye icon again to hide password
    login_page_toggle.toggle_password_visibility()
    assert not login_page_toggle.is_password_visible(), 'Password should be masked again after toggling back.'

    # Log success
    login_page_toggle.log_step('Password visibility toggle test completed successfully.')
