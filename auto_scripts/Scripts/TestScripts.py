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
    ...

def test_tc_login_005_empty_email_field(driver):
    """
    Test Case TC_LOGIN_005: Attempts login with empty email field, verifies validation error and login prevention.
    Test Steps:
        1. Navigate to the login page [URL: https://example-ecommerce.com/login]
        2. Leave email field empty
        3. Enter valid password [Password: Test@1234]
        4. Click Login button
        5. Validate error message 'Email is required' or field is highlighted
        6. Ensure login is prevented (user remains on login page)
    Expected Results:
        - Login page is displayed
        - Email field remains blank
        - Password is accepted
        - Validation error displayed: 'Email is required' or email field is highlighted
        - User cannot proceed with login and remains on login page
    Args:
        driver: Selenium WebDriver instance.
    Raises:
        AssertionError: If any validation fails.
    """
    login_page = LoginPage(driver)
    # Step 1: Open login page
    login_page.open_login_page()
    assert login_page.is_on_login_page(), "Login page not displayed"
    # Step 2: Leave email field empty (handled in method)
    # Step 3: Enter valid password
    # Step 4: Click Login button
    results = login_page.perform_empty_email_login_and_validate(password="Test@1234")
    # Step 5: Validate error message or field highlight
    assert results["validation_pass"], f"Validation failed: {results}"
    # Step 6: Ensure login is prevented
    assert results["login_prevented"], "Login was not prevented, user did not remain on login page"
    assert results["overall_pass"], "Overall TC_LOGIN_005 validation failed"
    print("TC_LOGIN_005: Successfully validated login with empty email field.")