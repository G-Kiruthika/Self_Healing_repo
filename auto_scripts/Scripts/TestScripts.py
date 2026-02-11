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
    # [existing code...]
    pass

# New method using Page Object class TC_LOGIN_003_TestPage
from auto_scripts.Pages.TC_LOGIN_003_TestPage import TC_LOGIN_003_TestPage

def test_tc_login_003_invalid_email_pageobject(driver):
    # [existing code...]
    pass

def test_tc_login_004_negative_login_valid_email_invalid_password(driver):
    # [existing code...]
    pass

def test_tc_login_005_empty_email_valid_password(driver):
    # [existing code...]
    pass

def test_tc_login_006_empty_fields_validation(driver):
    # [existing code...]
    pass

def test_tc_login_007_account_lockout(driver):
    # [existing code...]
    pass

def test_tc_login_008_password_visibility_toggle(driver):
    # [existing code...]
    pass

# New method for TC_LOGIN_009 using Page Object class
from auto_scripts.Pages.TC_LOGIN_009_TestPage import TC_LOGIN_009_TestPage

def test_tc_login_009_special_character_email(driver):
    # [existing code...]
    pass

# New method for TC_LOGIN_010 using Page Object class
from auto_scripts.Pages.TC_LOGIN_010_TestPage import TC_LOGIN_010_TestPage

def test_tc_login_010_network_disconnection_and_retry(driver):
    # [existing code...]
    pass

def test_tc_login_002_invalid_username_valid_password(driver):
    # [existing code...]
    pass

# TC_LOGIN_003: Valid username, invalid password scenario (Page Object Reference)
def test_tc_login_003_invalid_password_pageobject(driver):
    """
    Test Case TC_LOGIN_003: Invalid Password Login (Page Object Reference)

    Steps:
        1. Navigate to the login page (https://example-ecommerce.com/login)
        2. Enter valid username (validuser@example.com)
        3. Enter invalid password (WrongPass456!)
        4. Click Login
        5. Validate error message 'Invalid username or password' is displayed
        6. Verify user remains on login page

    Args:
        driver: Selenium WebDriver instance

    Raises:
        AssertionError: If any step fails
    """
    test_page = TC_LOGIN_003_TestPage(driver)
    result = test_page.run_invalid_password_login_test()
    assert result["error_displayed"], "Error message not displayed for invalid password login."
    assert result["remain_on_login"], "User did not remain on login page after invalid password login."
    print("TC_LOGIN_003_PageObject: Passed for invalid password login.")

# New method for TC_LOGIN_004 using Page Object class
from auto_scripts.Pages.TC_LOGIN_004_TestPage import TC_LOGIN_004_TestPage

def test_tc_login_004_empty_username_valid_password(driver):
    """
    Test Case TC_LOGIN_004: Login with empty username and valid password (Page Object Reference)

    Steps:
        1. Navigate to login page
        2. Leave username field empty
        3. Enter valid password
        4. Click Login
        5. Validate error message 'Username is required' is displayed

    Args:
        driver: Selenium WebDriver instance

    Raises:
        AssertionError: If any step fails
    """
    test_page = TC_LOGIN_004_TestPage(driver)
    result = test_page.run_test_case()
    assert result, "Error message 'Username is required' not displayed as expected."
    print("TC_LOGIN_004_PageObject: Passed for empty username and valid password.")
