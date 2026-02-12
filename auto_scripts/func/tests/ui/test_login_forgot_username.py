# tests/ui/test_login_forgot_username.py

from pages.login_page import LoginPage
from pages.username_recovery_page import UsernameRecoveryPage
from core.driver_factory import get_driver


def test_login_forgot_username_workflow():
    """
    Test Case: TC_LOGIN_003 - Forgot Username Workflow
    Steps:
    1. Navigate to login screen
    2. Click 'Forgot Username' link
    3. Follow instructions to recover username
    4. Verify username recovery page is displayed
    """
    driver = get_driver()
    
    try:
        # Step 1: Navigate to login screen
        login_page = LoginPage(driver)
        login_page.open()
        
        # Verify login page is loaded
        assert login_page.is_page_loaded(), "Login page failed to load"
        
        # Step 2: Click 'Forgot Username' link
        login_page.click_forgot_username()
        
        # Step 3: Follow instructions to recover username
        username_recovery_page = UsernameRecoveryPage(driver)
        
        # Verify username recovery page is displayed
        assert username_recovery_page.is_page_loaded(), "Username recovery page failed to load"
        
        # Verify recovery instructions are visible
        assert username_recovery_page.is_recovery_instructions_visible(), "Recovery instructions are not visible"
        
    finally:
        driver.quit()
