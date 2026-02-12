# tests/ui/test_login_remember_me_checkbox.py

from auto_scripts.Pages.LoginPage import LoginPage
from core.driver_factory import get_driver


def test_login_remember_me_checkbox_absence():
    """
    Test Case: TC_LOGIN_002 - Validate Remember Me Checkbox Absence
    Steps:
    1. Navigate to login screen
    2. Check for 'Remember Me' checkbox is not present
    """
    driver = get_driver()
    
    try:
        # Step 1: Navigate to login screen
        login_page = LoginPage(driver)
        
        # Step 2: Validate Remember Me checkbox is absent
        result = login_page.validate_remember_me_checkbox_absence()
        
        # Assert the result is True
        assert result is True, "Remember Me checkbox should not be present on the login screen"
        
    finally:
        driver.quit()
