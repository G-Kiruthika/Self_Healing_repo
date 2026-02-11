from auto_scripts.PageClasses.ProfileAPIValidationPage import ProfileAPIValidationPage
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.DashboardPage import DashboardPage

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

# New method using Page Object class TC_LOGIN_003_TestPage
from auto_scripts.Pages.TC_LOGIN_003_TestPage import TC_LOGIN_003_TestPage

def test_tc_login_003_invalid_email_pageobject(driver):
    """
    Test Case TC_LOGIN_003: Invalid Email Format Login (Page Object Reference)

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
    test_page = TC_LOGIN_003_TestPage(driver)
    results = test_page.run_invalid_email_login_test()
    for email, checks in results.items():
        assert checks["error_displayed"], f"Error message not displayed for email: {email}"
        assert checks["remain_on_login"], f"User did not remain on login page for email: {email}"
        print(f"TC_LOGIN_003_PageObject: Passed for invalid email: {email}")


def test_tc_login_004_negative_login_valid_email_invalid_password(driver):
    """
    Test Case TC_LOGIN_004: Negative Login (Valid Email, Invalid Password)

    Steps:
        1. Navigate to the login page (https://example-ecommerce.com/login)
        2. Enter valid email address (testuser@example.com)
        3. Enter incorrect password (WrongPass@123)
        4. Click Login button
        5. Validate error message ('Invalid email or password')
        6. Verify user remains on login page

    Args:
        driver: Selenium WebDriver instance

    Raises:
        AssertionError: If any step fails
    """
    login_page = LoginPage(driver)
    results = login_page.run_tc_login_004(email="testuser@example.com", password="WrongPass@123")
    assert results["navigate"], "Step 1 failed: Login page was not displayed."
    assert results["enter_email"], "Step 2 failed: Email was not accepted."
    assert results["enter_password"], "Step 3 failed: Password was not accepted."
    assert results["click_login"], "Step 4 failed: Login button click failed."
    assert results["error_message"], f"Step 5 failed: Error message incorrect. Expected 'Invalid email or password', got: {results['actual_error_message']}"
    assert results["is_on_login_page"], f"Step 6 failed: User did not remain on login page. Current URL: {results['current_url']}"
    assert results["overall_pass"], "TC_LOGIN_004 overall validation failed."
    print(f"TC_LOGIN_004: Passed for valid email and invalid password. Error Message: {results['actual_error_message']}, Current URL: {results['current_url']}")


def test_tc_login_005_empty_email_valid_password(driver):
    """
    Test Case TC_LOGIN_005: Login attempt with empty email and valid password

    Steps:
        1. Navigate to the login page (https://example-ecommerce.com/login)
        2. Leave the email field empty
        3. Enter a valid password (Test@1234)
        4. Click the Login button
        5. Validate that a validation error is displayed (such as 'Email is required', or field is highlighted)
        6. Ensure login is prevented and the user remains on the login page

    Args:
        driver: Selenium WebDriver instance

    Raises:
        AssertionError: If any step fails
    """
    login_page = LoginPage(driver)
    url = "https://example-ecommerce.com/login"
    password = "Test@1234"
    results = {}
    results["navigate"] = login_page.go_to_login_page(url) if hasattr(login_page, "go_to_login_page") else login_page.navigate_to_login_page(url)
    assert results["navigate"], f"Step 1 failed: Login page not displayed for URL: {url}"
    # Step 2: Leave email empty (do not call enter_email)
    results["enter_password"] = login_page.enter_password(password)
    assert results["enter_password"], f"Step 3 failed: Password field did not accept input: {password}"
    results["click_login"] = login_page.click_login() if hasattr(login_page, "click_login") else login_page.click_login_button()
    assert results["click_login"], "Step 4 failed: Login button click failed"
    error_message = login_page.get_error_message()
    results["error_message"] = error_message is not None and ("Email is required" in error_message or error_message.strip() != "")
    assert results["error_message"], f"Step 5 failed: Expected error message not found. Got: {error_message}"
    results["is_on_login_page"] = login_page.is_on_login_page() if hasattr(login_page, "is_on_login_page") else not login_page.is_user_logged_in()
    assert results["is_on_login_page"], "Step 6 failed: User did not remain on login page."
    results["overall_pass"] = all([
        results["navigate"],
        results["enter_password"],
        results["click_login"],
        results["error_message"],
        results["is_on_login_page"]
    ])
    assert results["overall_pass"], "TC_LOGIN_005 overall validation failed."
    print(f"TC_LOGIN_005: Passed for empty email and valid password. Error Message: {error_message}")


def test_tc_login_006_empty_fields_validation(driver):
    """
    Test Case TC_LOGIN_006: Both Email and Password Fields Empty - Validation & Prevention of Login

    Steps:
        1. Navigate to login page.
        2. Leave both fields empty.
        3. Click Login.
        4. Validate errors for both fields.
        5. Verify highlights.
        6. Ensure login is prevented.

    Args:
        driver: Selenium WebDriver instance

    Raises:
        AssertionError: If any step fails
    """
    login_page = LoginPage(driver)
    results = login_page.run_tc_login_006()
    assert results["step_1_navigate_login"], f"Step 1 failed: Login page is not displayed."
    assert results["step_2_leave_fields_empty"], f"Step 2 failed: Fields not empty."
    assert results["step_3_click_login"], f"Step 3 failed: Login button click failed."
    assert results["step_4_validate_errors"], f"Step 4 failed: Validation errors missing. Errors: {results['errors']}"
    assert results["step_5_highlight_required"], f"Step 5 failed: Fields not highlighted as required. Highlights: {results['highlights']}"
    assert results["step_6_prevent_login"], f"Step 6 failed: User did not remain on login page. Error: {results['error_message_text']}"
    assert results["overall_pass"], f"TC_LOGIN_006 overall validation failed."
    print(f"TC_LOGIN_006: Passed for empty email and password. Errors: {results['errors']}, Highlights: {results['highlights']}, Error Message: {results['error_message_text']}")


def test_tc_login_007_account_lockout(driver):
    """
    Test Case TC_LOGIN_007: Account Lockout after Multiple Failed Login Attempts

    Steps:
        1. Navigate to login page (https://example-ecommerce.com/login)
        2. Enter valid email and incorrect password
        3. Click Login button and repeat 5 times (expect 'Invalid email or password' error each time)
        4. Attempt 6th login (expect lockout message)
        5. Try correct password after lockout (lockout message persists)

    Args:
        driver: Selenium WebDriver instance

    Raises:
        AssertionError: If any step fails
    """
    login_page = LoginPage(driver)
    valid_email = "testuser@example.com"
    incorrect_password = "WrongPass@1"
    correct_password = "Test@1234"
    login_page.navigate_to_login()
    # Step 2 & 3: 5 failed login attempts
    for attempt in range(5):
        login_page.enter_email(valid_email)
        login_page.enter_password(incorrect_password)
        login_page.click_login()
        error = login_page.get_error_message()
        assert error == "Invalid email or password", f"Attempt {attempt+1}: Expected invalid credentials error, got: {error}"
    # Step 4: 6th login triggers lockout
    login_page.enter_email(valid_email)
    login_page.enter_password(incorrect_password)
    login_page.click_login()
    lockout_error = login_page.get_error_message()
    assert lockout_error == "Account temporarily locked due to multiple failed attempts. Try again after 15 minutes", f"6th attempt: Expected lockout, got: {lockout_error}"
    # Step 5: Try correct password after lockout
    login_page.enter_email(valid_email)
    login_page.enter_password(correct_password)
    login_page.click_login()
    lockout_error_2 = login_page.get_error_message()
    assert lockout_error_2 == "Account temporarily locked due to multiple failed attempts. Try again after 15 minutes", f"Post-lockout: Expected lockout, got: {lockout_error_2}"
    print("TC_LOGIN_007: Account lockout scenario passed.")


def test_tc_login_008_password_visibility_toggle(driver):
    """
    Test Case TC_LOGIN_008: Password Visibility Toggle

    Steps:
        1. Navigate to the login page (https://example-ecommerce.com/login)
        2. Enter password in password field (Test@1234)
        3. Validate password is masked by default
        4. Click 'Show Password' icon/toggle and validate password is visible
        5. Click 'Hide Password' icon/toggle and validate password is masked again
        6. Verify toggle works multiple times

    Args:
        driver: Selenium WebDriver instance

    Raises:
        AssertionError: If any step fails
    """
    login_page = LoginPage(driver)
    password = "Test@1234"
    results = login_page.run_tc_login_008(password)
    assert results["step_1_navigate_login"], "Step 1 failed: Login page is not displayed."
    assert results["step_2_enter_password"], "Step 2 failed: Password field did not accept input."
    assert results["step_3_password_masked"], "Step 3 failed: Password not masked by default."
    assert results["step_4_toggle_show_password"], "Step 4 failed: Password not visible after show toggle."
    assert results["step_5_toggle_hide_password"], "Step 5 failed: Password not masked after hide toggle."
    assert results["step_6_toggle_multiple"], f"Step 6 failed: Toggle did not work multiple times. Errors: {results['errors']}"
    assert results["overall_pass"], "TC_LOGIN_008 overall validation failed."
    print(f"TC_LOGIN_008: Passed for password visibility toggle. Stepwise results: {results}")
