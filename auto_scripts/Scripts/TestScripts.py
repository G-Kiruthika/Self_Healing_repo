from auto_scripts.PageClasses.ProfileAPIValidationPage import ProfileAPIValidationPage
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
from auto_scripts.Pages.LoginPage import LoginPage

def test_tc_login_001_invalid_credentials(driver):
    ...
def test_tc_login_001_valid_login(driver):
    ...
def test_tc_login_002_remember_me_session_persistence(driver, driver_factory):
    ...

def test_tc_login_003_invalid_email_formats(driver):
    ...

def test_tc_login_004_invalid_password(driver):
    """
    Test Case TC_LOGIN_004: Attempts login with valid email and incorrect password, verifies error message and user remains on login page.
    Test Steps:
        1. Navigate to the login page [URL: https://example-ecommerce.com/login]
        2. Enter valid email address [Email: testuser@example.com]
        3. Enter incorrect password [Password: WrongPass@123]
        4. Click Login button
        5. Verify error message 'Invalid email or password'
        6. Verify user remains on login page and is not authenticated
    Expected Results:
        - Login page is displayed
        - Error message is shown: 'Invalid email or password'
        - User remains on login page, not authenticated
    Args:
        driver: Selenium WebDriver instance.
    Raises:
        AssertionError: If any validation fails.
    """
    login_page = LoginPage(driver)
    # Step 1: Open login page
    login_page.navigate_to_login("https://example-ecommerce.com/login")
    assert login_page.is_on_login_page(), "Login page not displayed"
    # Step 2: Enter valid email address
    login_page.enter_email("testuser@example.com")
    # Step 3: Enter incorrect password
    login_page.enter_password("WrongPass@123")
    # Step 4: Click Login button
    login_page.click_login()
    # Step 5: Verify error message
    error_msg = login_page.get_error_message()
    expected_error = "Invalid email or password"
    assert error_msg is not None and expected_error in error_msg, f"Expected error message not found. Got: '{error_msg}'"
    # Step 6: Verify user remains on login page and is not authenticated
    assert login_page.is_on_login_page(), "User did not remain on login page after invalid login"
    print("TC_LOGIN_004: Successfully validated login with invalid password.")

def test_tc_login_006_empty_fields(driver):
    """
    Test Case TC_LOGIN_006: Attempts login with both email and password fields empty, verifies error messages and field highlights, ensures login is prevented.
    Test Steps:
        1. Navigate to the login page [URL: https://example-ecommerce.com/login]
        2. Leave both email and password fields empty
        3. Click Login button
        4. Validate error messages 'Email is required' and 'Password is required'
        5. Check both fields are highlighted as required
        6. Ensure login is prevented and user remains on login page
    Expected Results:
        - Login page is displayed
        - Both fields remain blank
        - Validation errors displayed for both fields: 'Email is required' and 'Password is required'
        - Both email and password fields show validation error styling
        - User cannot proceed and remains on login page
    Args:
        driver: Selenium WebDriver instance.
    Raises:
        AssertionError: If any validation fails.
    """
    login_page = LoginPage(driver)
    results = login_page.run_tc_login_006()
    # Step 1: Navigate to login page
    assert results['step_1']['ui_state'] == 'Login page displayed', f"Step 1 failed: {results['step_1']}"
    # Step 2: Leave both fields empty
    assert results['step_2']['ui_state'] == 'Both fields blank', f"Step 2 failed: {results['step_2']}"
    # Step 3: Click Login button and validate error messages
    step3 = results['step_3']
    assert step3['email_error_message'] is not None and 'email' in step3['email_error_message'].lower(), f"Step 3 failed: Email error message not found. {step3}"
    assert step3['password_error_message'] is not None and 'password' in step3['password_error_message'].lower(), f"Step 3 failed: Password error message not found. {step3}"
    # Step 4: Check both fields are highlighted as required
    assert step3['email_field_highlighted'], f"Step 4 failed: Email field not highlighted. {step3}"
    assert step3['password_field_highlighted'], f"Step 4 failed: Password field not highlighted. {step3}"
    # Step 5: Verify login is prevented (user remains on login page)
    step4 = results['step_4']
    assert step4['login_prevented'], f"Step 5 failed: Login was not prevented. {step4}"
    assert step4['current_url'] == login_page.URL, f"Step 5 failed: User not on login page. {step4}"
    print('TC_LOGIN_006: Successfully validated login with empty fields.', results)
