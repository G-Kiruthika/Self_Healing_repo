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
    login_page.open()
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
    assert not login_page.is_authenticated(), "User is unexpectedly authenticated after invalid login"
    print("TC_LOGIN_004: Successfully validated login with invalid password.")
