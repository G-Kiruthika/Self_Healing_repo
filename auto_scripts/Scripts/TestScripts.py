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

def test_tc_login_002_remember_me_session_persistence(driver):
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
    Raises:
        AssertionError: If any validation fails.
    """
    try:
        login_page = LoginPage(driver)
        # Step 1: Navigate to login page
        login_page.go_to_login_page()
        assert login_page.is_on_login_page(), "Login page is not displayed."
        # Step 2: Enter valid credentials
        email = "testuser@example.com"
        password = "Test@1234"
        login_page.enter_email(email)
        login_page.enter_password(password)
        # Step 3: Select 'Remember Me' checkbox
        login_page.select_remember_me()
        # Step 4: Click Login and verify successful login
        login_page.click_login()
        assert login_page.verify_successful_login(), "Login failed or dashboard not displayed."
        # Step 5 & 6: Validate session persistence after browser reopen
        login_page.validate_remember_me_session_persistence(email, password)
        print("TC_LOGIN_002: Successfully validated login with 'Remember Me' and session persistence after browser reopen.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        assert False, f"Test TC_LOGIN_002 failed: {str(e)}"
