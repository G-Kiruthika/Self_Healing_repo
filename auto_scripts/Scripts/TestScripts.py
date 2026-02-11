from auto_scripts.PageClasses.ProfileAPIValidationPage import ProfileAPIValidationPage
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
from auto_scripts.Pages.LoginPage import LoginPage

# TC_LOGIN_007 PageClass import
from auto_scripts.Pages.TC_LOGIN_007_TestPage import TC_LOGIN_007_TestPage

# TC_LOGIN_008 PageClass import
from auto_scripts.Pages.LoginPasswordVisibilityTestPage import LoginPasswordVisibilityTestPage

# TC_LOGIN_010 PageClass import
from auto_scripts.Pages.LoginPage_TC_LOGIN_010 import LoginPage_TC_LOGIN_010

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
    assert results['step_1_navigate'], f"Step 1 failed: Did not navigate to login page"
    # Step 2: Enter valid email and incorrect password
    assert results['step_2_enter_credentials'], f"Step 2 failed: Credentials not entered"
    # Step 3: Click Login button 5 times, validate error messages
    assert len(results['step_3_all_errors']) == 5, f"Step 3 failed: Error messages not captured for all 5 attempts"
    for idx, msg in enumerate(results['step_3_all_errors']):
        assert msg is not None and 'Invalid' in msg, f"Step 3 failed at attempt {idx+1}: Expected invalid credentials error, got: {msg}"
    # Step 4: Attempt login 6th time, validate lockout message
    assert results['step_4_lockout_detected'], f"Step 4 failed: Lockout message not detected"
    assert 'Account temporarily locked' in results['step_4_lockout_message'], f"Step 4 failed: Unexpected lockout message: {results['step_4_lockout_message']}"
    # Step 5: Attempt login with correct password, validate lockout persists
    assert results['step_5_lockout_persists'], f"Step 5 failed: Lockout does not persist after correct password"
    assert 'Account temporarily locked' in results['step_5_correct_password_lockout_message'], f"Step 5 failed: Lockout message missing after correct password: {results['step_5_correct_password_lockout_message']}"
    assert results['overall_pass'], f"Overall test failed: Lockout not enforced as expected"
    print('TC_LOGIN_007: Account Lockout after multiple failed login attempts - Successfully validated.', results)


def test_tc_login_008_password_visibility_toggle(driver):
    """
    Test Case TC_LOGIN_008: Password Visibility Toggle
    Steps:
        1. Navigate to login page
        2. Enter password in password field
        3. Click on 'Show Password' icon/toggle
        4. Click on 'Hide Password' icon/toggle
        5. Verify toggle works multiple times
    """
    login_page = LoginPasswordVisibilityTestPage(driver)
    password = 'Test@1234'
    results = login_page.run_tc_login_008(password)
    # Step 1: Navigate to login page
    assert results['step_1']['ui_state'] == 'Login page displayed with password field', f"Step 1 failed: {results['step_1']}"
    # Step 2: Enter password in password field, verify masked
    assert results['step_2']['password_masked'], f"Step 2 failed: Password not masked. {results['step_2']}"
    # Step 3: Click 'Show Password', verify visible
    assert results['step_3']['toggle_clicked'], f"Step 3 failed: Show toggle not clicked. {results['step_3']}"
    assert results['step_3']['password_visible'], f"Step 3 failed: Password not visible after toggle. {results['step_3']}"
    # Step 4: Click 'Hide Password', verify masked again
    assert results['step_4']['toggle_clicked'], f"Step 4 failed: Hide toggle not clicked. {results['step_4']}"
    assert results['step_4']['password_masked'], f"Step 4 failed: Password not masked after hide toggle. {results['step_4']}"
    # Step 5: Repeat toggle, validate results
    toggle_results = results['step_5']['toggle_results']
    for idx, res in enumerate(toggle_results):
        assert res['visible'], f"Step 5 failed at iteration {idx+1}: Password not visible after show toggle."
        assert res['masked'], f"Step 5 failed at iteration {idx+1}: Password not masked after hide toggle."
    print('TC_LOGIN_008: Password Visibility Toggle - Successfully validated.', results)


def test_tc_login_009_special_character_email(driver):
    """
    Test Case TC_LOGIN_009: Login with email containing special characters and strict validation (AC_009)
    Steps:
        1. Navigate to login page
        2. Enter email with special characters (test.user+tag@example.com)
        3. Enter valid password (Test@1234)
        4. Click Login button
        5. Verify successful login or valid error message
    """
    login_page = LoginPage(driver)
    email = "test.user+tag@example.com"
    password = "Test@1234"
    results = login_page.login_with_special_character_email(email=email, password=password)
    # Step 1: Navigate to login page
    assert results['step_1']['ui_state'] == 'Login page displayed', f"Step 1 failed: {results['step_1']}"
    # Step 2: Enter email with special characters
    assert results['step_2']['input_email'] == email, f"Step 2 failed: Email input mismatch. {results['step_2']}"
    # Step 3: Enter valid password
    assert results['step_3']['input_password'] == password, f"Step 3 failed: Password input mismatch. {results['step_3']}"
    # Step 4: Click Login button, check dashboard or error message
    step4 = results['step_4']
    if step4['dashboard_visible'] and step4['profile_icon_visible']:
        assert step4['dashboard_visible'], f"Step 4 failed: Dashboard not visible. {step4}"
        assert step4['profile_icon_visible'], f"Step 4 failed: Profile icon not visible. {step4}"
    else:
        assert step4['error_message'] is not None, f"Step 4 failed: No error message present. {step4}"
    # Step 5: Verify login outcome
    step5 = results['step_5']
    if step5['login_successful']:
        print('TC_LOGIN_009: Login successful with special character email.', results)
    else:
        assert step5['error_message'] is not None, f"Step 5 failed: No error message present. {step5}"
        print('TC_LOGIN_009: Valid error message received for special character email.', results)


def test_tc_login_010_network_recovery(driver):
    """
    Test Case TC_LOGIN_010: Network Disconnection and Recovery (AC_010)
    Steps:
        1. Navigate to login page
        2. Enter valid credentials
        3. Simulate network offline/throttling
        4. Click Login button, verify loading indicator and error message
        5. Restore network, retry login, validate dashboard and profile icon
    """
    login_page = LoginPage_TC_LOGIN_010(driver)
    email = "testuser@example.com"
    password = "Test@1234"
    # Run test with network offline
    results_offline = login_page.perform_login_with_network_issue_and_retry(email, password)
    # Stepwise assertions
    assert results_offline['step_1_page_loaded'], "Step 1 failed: Login page not loaded"
    assert results_offline['step_2_credentials_entered'], "Step 2 failed: Credentials not entered"
    assert results_offline['step_3_network_disconnected'], "Step 3 failed: Network not disconnected"
    assert results_offline['step_4_loading_indicator'], "Step 4 failed: Loading indicator not shown"
    assert results_offline['step_4_expected_error'], "Step 4 failed: Expected network error message not shown"
    assert results_offline['step_5_network_restored'], "Step 5 failed: Network not restored"
    assert results_offline['step_6_login_successful'], "Step 6 failed: Login not successful after network restoration"
    assert results_offline['overall_pass'], "Overall test failed: Not all steps passed"
    print('TC_LOGIN_010: Successfully validated login with network disconnection and recovery (offline scenario).', results_offline)