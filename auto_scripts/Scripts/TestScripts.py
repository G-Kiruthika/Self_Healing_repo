from auto_scripts.PageClasses.ProfileAPIValidationPage import ProfileAPIValidationPage
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.DashboardPage import DashboardPage
from auto_scripts.Pages.TC_LOGIN_002_TestPage import TC_LOGIN_002_TestPage

def test_tc_login_001_invalid_credentials(driver):
    # [existing logic for invalid credentials test]
    pass

def test_tc_login_001_valid_credentials(driver):
    # [existing logic for valid credentials test]
    pass

def test_tc_login_002_remember_me_persistence(driver_factory):
    # [existing logic for remember me test]
    pass

def test_tc_login_003_invalid_email_format(driver):
    """
    Test Case TC_LOGIN_003: Invalid Email Format Login
    Steps:
        1. Navigate to the login page (https://example-ecommerce.com/login)
        2. Enter invalid email formats (invalidemail@com, testuser.example.com, @example.com)
        3. Enter valid password (Test@1234)
        4. Click Login
        5. Validate error message and user is not logged in
    Args:
        driver: Selenium WebDriver instance
    Raises:
        AssertionError: If any step fails
    """
    login_page = LoginPage(driver)
    url = "https://example-ecommerce.com/login"
    invalid_emails = ["invalidemail@com", "testuser.example.com", "@example.com"]
    password = "Test@1234"
    for email in invalid_emails:
        results = {}
        results["navigate"] = login_page.navigate_to_login_page(url)
        assert results["navigate"], f"Login page not displayed for URL: {url}"
        results["enter_email"] = login_page.enter_email(email)
        assert results["enter_email"], f"Email field did not accept input: {email}"
        results["enter_password"] = login_page.enter_password(password)
        assert results["enter_password"], f"Password field did not accept input: {password}"
        results["click_login"] = login_page.click_login_button()
        assert results["click_login"], "Login button click failed"
        error_message = login_page.get_error_message()
        results["error_message"] = error_message == "Please enter a valid email address"
        assert results["error_message"], f"Expected error message not found for email: {email}. Got: {error_message}"
        results["user_logged_in"] = not login_page.is_user_logged_in()
        assert results["user_logged_in"], f"User should not be logged in with invalid email: {email}"
        results["overall"] = all([
            results["navigate"],
            results["enter_email"],
            results["enter_password"],
            results["click_login"],
            results["error_message"],
            results["user_logged_in"]
        ])
        assert results["overall"], f"TC_LOGIN_003 failed for email: {email}"
        print(f"TC_LOGIN_003: Passed for invalid email: {email}")

# ... (rest of the file omitted for brevity)

def test_tc_login_002_invalid_login(driver):
    """
    Test Case TC_LOGIN_002: Invalid Login Attempt
    Steps:
        1. Instantiate TC_LOGIN_002_TestPage
        2. Call run_tc_login_002 with invalid username and valid password
        3. Validate expected error message and step results
    Args:
        driver: Selenium WebDriver instance
    Raises:
        AssertionError: If any step fails
    """
    page = TC_LOGIN_002_TestPage(driver)
    results = page.run_tc_login_002(
        username='invaliduser@example.com',
        password='ValidPass123!',
        expected_error='Invalid username or password'
    )
    assert results["navigate"], "Failed to navigate to login page"
    assert results["enter_username"], "Failed to enter username"
    assert results["enter_password"], "Failed to enter password"
    assert results["click_login"], "Failed to click login button"
    assert results["error_message"], f"Expected error message not found. Got: {results.get('actual_error_message', '')}"
    assert results["user_logged_in"] is False, "User should not be logged in with invalid credentials"
    print("TC_LOGIN_002: Passed invalid login scenario")
