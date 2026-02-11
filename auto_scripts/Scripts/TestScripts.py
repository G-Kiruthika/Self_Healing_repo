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
    """
    Test Case TC_LOGIN_003: Test login functionality with invalid email formats.
    Test Case ID: 4154
    Description: Test invalid email formats on login page.
    Test Steps:
        1. Navigate to the login page [Test Data: URL: https://example-ecommerce.com/login]
        2. Enter invalid email formats [Test Data: Email: invalidemail@com, testuser.example.com, @example.com]
        3. Enter valid password [Test Data: Password: Test@1234]
        4. Click Login button
        5. Validate error message 'Please enter a valid email address'
        6. Verify user is not logged in
    Expected Results:
        - Login page is displayed
        - Error message is shown for each invalid email
        - User remains on login page, no session is created
    Args:
        driver: Selenium WebDriver instance.
    Raises:
        AssertionError: If any validation fails.
    """
    try:
        login_page = LoginPage(driver)
        invalid_emails = ["invalidemail@com", "testuser.example.com", "@example.com"]
        valid_password = "Test@1234"
        results = login_page.login_with_invalid_email_and_validate(invalid_emails, valid_password)
        for email, result in results.items():
            assert result["pass_criteria"], (
                f"Failed for email '{email}': "
                f"Error Message: {result['error_message']}, "
                f"Validation Error: {result['validation_error_message']}, "
                f"On Login Page: {result['on_login_page']}, "
                f"User Logged In: {result['user_logged_in']}"
            )
        print("TC_LOGIN_003: Successfully validated login with invalid email formats.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        assert False, f"Test TC_LOGIN_003 failed: {str(e)}"
