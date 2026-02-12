# tests/ui/test_login.py

from pages.login_page import LoginPage
from core.driver_factory import get_driver


def test_login_validate_remember_me_checkbox_absence():
    """
    TC_LOGIN_002: Validate Absence of 'Remember Me' Checkbox
    
    Steps:
    1. Navigate to the login screen
    2. Assert that the 'Remember Me' checkbox is not present
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Navigate to the login screen
    login_page.open()
    
    # Validate that the 'Remember Me' checkbox is absent
    is_absent = login_page.validate_remember_me_checkbox_absence()
    
    # Assert the checkbox is not present
    assert is_absent, "Remember Me checkbox should not be present on the login page"
    
    driver.quit()
