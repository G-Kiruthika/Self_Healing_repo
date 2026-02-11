from auto_scripts.PageClasses.ProfileAPIValidationPage import ProfileAPIValidationPage
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
from auto_scripts.Pages.LoginPage import LoginPage

def test_tc_login_001_invalid_credentials(driver):
    """
    Test Case TC_LOGIN_001: Test login functionality with invalid credentials.
    ...
    """
    try:
        # Initialize LoginPage
        login_page = LoginPage(driver)
        ...
    except Exception as e:
        ...

def test_tc_login_001_valid_login(driver):
    """
    Test Case TC_LOGIN_001: Test login functionality with valid credentials.
    ...
    """
    try:
        login_page = LoginPage(driver)
        ...
    except Exception as e:
        ...

def test_tc_login_002_remember_me_session_persistence(driver, driver_factory):
    """
    Test Case TC_LOGIN_002: Valid login, 'Remember Me' selection, and session persistence validation after browser reopen.
    Test Case ID: 4153
    Description: Test Case TC_LOGIN_002
    Test Steps:
        1. Navigate to the login page [Test Data: URL: https://example-ecommerce.com/login]
        2. Enter valid credentials [Test Data: Email: testuser@example.com, Password: Test@1234]
        3. Check the 'Remember Me' checkbox
        4. Click Login button and verify successful login
        5. Close browser and reopen, navigate to the website
        6. Verify user remains logged in without re-entering credentials
    Expected Results:
        - Login page is displayed
        - Credentials are accepted
        - Checkbox is selected
        - User is logged in successfully
        - User remains logged in after browser reopen
    Args:
        driver: Selenium WebDriver instance.
        driver_factory: Callable to instantiate a new WebDriver instance.
    Raises:
        AssertionError: If any validation fails.
    """
    try:
        login_page = LoginPage(driver)
        email = "testuser@example.com"
        password = "Test@1234"
        results = login_page.login_with_remember_me_and_validate_persistence(email, password, driver_factory)
        assert results['login_page_opened'], "Login page is not displayed."
        assert results['credentials_entered'], "Credentials were not entered properly."
        assert results['remember_me_checked'], "'Remember Me' checkbox was not checked."
        assert results['user_logged_in'], "User is not logged in after login attempt."
        assert results['user_still_logged_in_after_reopen'], "User is not logged in after browser reopen (session persistence failed)."
        print("TC_LOGIN_002: Successfully validated login with 'Remember Me' and session persistence after browser reopen.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        assert False, f"Test TC_LOGIN_002 failed: {str(e)}"

def test_tc_login_003_invalid_email_formats(driver):
    """
    Test Case TC_LOGIN_003: Negative login validation for invalid email formats.
    Test Case ID: 4154
    Description: Test Case TC_LOGIN_003
    Test Steps:
        1. Navigate to the login page [Test Data: URL: https://example-ecommerce.com/login]
        2. Enter invalid email format in email field [Test Data: Email: invalidemail@com, testuser.example.com, @example.com]
        3. Enter valid password [Test Data: Password: Test@1234]
        4. Click Login button
        5. Verify error message and session absence
    Expected Results:
        - Login page is displayed
        - Email field accepts the input
        - Password is accepted
        - Error message displayed: 'Please enter a valid email address'
        - User remains on login page, no session is created
    Args:
        driver: Selenium WebDriver instance.
    Raises:
        AssertionError: If any validation fails.
    """
    invalid_emails = ["invalidemail@com", "testuser.example.com", "@example.com"]
    password = "Test@1234"
    login_page = LoginPage(driver)
    for email in invalid_emails:
        try:
            login_page.validate_invalid_email(email, password)
            print(f"TC_LOGIN_003: Successfully validated negative login for invalid email format: {email}")
        except AssertionError as ae:
            import traceback
            traceback.print_exc()
            assert False, f"Test TC_LOGIN_003 failed for email '{email}': {str(ae)}"
        except Exception as e:
            import traceback
            traceback.print_exc()
            assert False, f"Unexpected error in TC_LOGIN_003 for email '{email}': {str(e)}"
