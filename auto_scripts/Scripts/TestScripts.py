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
    login_page = LoginPage(driver)
    invalid_emails = ["invalidemail@com", "testuser.example.com", "@example.com"]
    valid_password = "Test@1234"
    for email in invalid_emails:
        # Step 1: Open login page
        login_page.open_login_page()
        assert login_page.is_on_login_page(), f"Login page not displayed for email: {email}"
        # Step 2: Enter invalid email format
        login_page.enter_email(email)
        assert not login_page.is_valid_email_format(email), f"Email format unexpectedly valid: {email}"
        # Step 3: Enter valid password
        login_page.enter_password(valid_password)
        # Step 4: Click Login button
        login_page.click_login()
        # Step 5: Validate error message
        error_msg = login_page.get_error_message()
        validation_msg = login_page.get_validation_error_message()
        expected_error = 'Please enter a valid email address'
        assert (error_msg is not None and expected_error in error_msg) or (validation_msg is not None and expected_error in validation_msg), f"Expected error message not found for email: {email}. Got: '{error_msg}' and '{validation_msg}'"
        # Step 6: Verify user is not logged in
        assert not login_page.is_user_logged_in(), f"User unexpectedly logged in with invalid email: {email}"
        assert login_page.is_on_login_page(), f"User did not remain on login page for email: {email}"
    print("TC_LOGIN_003: Successfully validated login with invalid email formats.")
