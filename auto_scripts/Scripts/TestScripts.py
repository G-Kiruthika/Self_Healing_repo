
import pytest
from selenium.webdriver.common.by import By
from LoginPage import LoginPage

# ... (existing test methods and imports remain unchanged)

def test_TC_LOGIN_004_username_required_error(driver):
    """
    TC_LOGIN_004: Verify error message 'Username is required' is displayed when username is left empty and valid password is entered on login page.

    Steps:
      1. Navigate to login page (https://ecommerce.example.com/login)
      2. Leave username empty
      3. Enter valid password (ValidPass123!)
      4. Click login
      5. Validate error message 'Username is required' is displayed.

    Args:
        driver (selenium.webdriver): Selenium WebDriver instance

    Asserts:
        Error message 'Username is required' is displayed.
    """
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page('https://ecommerce.example.com/login')
    login_page.set_username("")  # Leave username empty
    login_page.set_password("ValidPass123!")
    login_page.click_login()
    assert login_page.assert_username_required_error(), (
        "Expected error message 'Username is required' was not displayed when username was left empty."
    )
