# tests/ui/test_login_invalid_credentials.py

from pages.LoginPage import LoginPage
from core.driver_factory import get_driver

def test_login_invalid_credentials():
    """
    TC_LOGIN_001: Test login with invalid credentials
    Validates that error message is displayed for invalid login attempt
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Load the login page
    login_page.load()
    
    # Attempt login with invalid credentials
    login_page.login("invalid_user", "invalid_password")
    
    # Verify error is displayed
    assert login_page.is_error_displayed(), "Error message should be displayed for invalid credentials"
    
    # Verify error message text
    error_text = login_page.get_error_text()
    assert error_text is not None and len(error_text) > 0, "Error message text should not be empty"
    
    driver.quit()
