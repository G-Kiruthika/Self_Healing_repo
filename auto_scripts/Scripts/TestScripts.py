from auto_scripts.PageClasses.ProfileAPIValidationPage import ProfileAPIValidationPage
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
from auto_scripts.Pages.LoginPage import LoginPage

# TC_LOGIN_007 PageClass import
from auto_scripts.Pages.TC_LOGIN_007_TestPage import TC_LOGIN_007_TestPage

def test_tc_login_001_invalid_credentials(driver):
    ...
def test_tc_login_001_valid_login(driver):
    ...
def test_tc_login_002_remember_me_session_persistence(driver, driver_factory):
    ...

def test_tc_login_003_invalid_email_formats(driver):
    ...

def test_tc_login_004_invalid_password(driver):
    ...

def test_tc_login_006_empty_fields(driver):
    ...

def test_tc_login_006_strict_validation(driver):
    """
    Test Case TC_LOGIN_006 (Strict Validation): Attempts login with both email and password fields empty, verifies error messages and field highlights, ensures login is prevented.
    Steps:
        1. Navigate to login page
        2. Leave both fields empty
        3. Click Login button
        4. Validate error messages ('Email is required', 'Password is required')
        5. Check highlights for both fields
        6. Ensure login is prevented and user remains on login page
    """
    login_page = LoginPage(driver)
    results = login_page.run_tc_login_006()
    # Step 1: Navigate to login page
    assert results['step_1']['ui_state'] == 'Login page displayed', f"Step 1 failed: {results['step_1']}"
    # Step 2: Leave both fields empty
    assert results['step_2']['ui_state'] == 'Both fields blank', f"Step 2 failed: {results['step_2']}"
    # Step 3: Click Login button and validate error messages
    step3 = results['step_3']
    assert step3['email_error_found'], f"Step 3 failed: Email error message not found. {step3}"
    assert step3['password_error_found'], f"Step 3 failed: Password error message not found. {step3}"
    # Step 4: Check both fields are highlighted as required
    step4 = results['step_4']
    assert step4['email_field_highlighted'], f"Step 4 failed: Email field not highlighted. {step4}"
    assert step4['password_field_highlighted'], f"Step 4 failed: Password field not highlighted. {step4}"
    # Step 5: Verify login is prevented (user remains on login page)
    step5 = results['step_5']
    assert step5['login_prevented'], f"Step 5 failed: Login was not prevented. {step5}"
    assert step5['current_url'] == login_page.URL, f"Step 5 failed: User not on login page. {step5}"
    print('TC_LOGIN_006 (Strict Validation): Successfully validated login with empty fields.', results)


def test_tc_login_007_account_lockout(driver):
    """
    Test Case TC_LOGIN_007: Account Lockout after multiple failed login attempts
    Steps:
        1. Navigate to login page
        2. Enter valid email and incorrect password
        3. Click Login button and repeat 5 times
        4. Attempt login 6th time, verify lockout message
        5. Verify login is blocked even with correct password
    """
    login_page = TC_LOGIN_007_TestPage(driver)
    email = 'testuser@example.com'
    incorrect_password = 'WrongPass@1'
    correct_password = 'Test@1234'
    results = login_page.run_tc_login_007(email, incorrect_password, correct_password)
    # Step 1: Navigate to login page
    assert results['step_1_navigate_login'], f"Step 1 failed: Did not navigate to login page"
    # Step 2: Enter valid email and incorrect password
    assert results['step_2_credentials_entered'], f"Step 2 failed: Credentials not entered"
    # Step 3: Click Login button 5 times, validate error messages
    assert results['step_3_all_errors_valid'], f"Step 3 failed: Error messages not valid"
    # Step 4: Attempt login 6th time, validate lockout message
    assert results['step_4_lockout_valid'], f"Step 4 failed: Lockout message not valid"
    # Step 5: Verify login is blocked even with correct password
    assert results['step_5_lockout_persists'], f"Step 5 failed: Lockout does not persist"
    assert results['step_5_login_prevented'], f"Step 5 failed: Login not prevented"
    print('TC_LOGIN_007: Account Lockout after multiple failed login attempts - Successfully validated.', results)
