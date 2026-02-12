# tests/ui/test_login_forgot_username.py

from pages.login_page import LoginPage
from pages.username_recovery_page import UsernameRecoveryPage
from pages.tc_login_003_test_page import TC_LOGIN_003_TestPage
from core.driver_factory import get_driver


def test_login_forgot_username():
    """
    Test Case: TC_LOGIN_003 - Forgot Username Workflow
    Steps:
    1. Navigate to login screen
    2. Click 'Forgot Username' link
    3. Recover username
    4. Validate the results
    """
    driver = get_driver()
    
    try:
        # Step 1: Navigate to login screen
        login_page = LoginPage(driver)
        login_page.open()
        
        # Step 2: Click 'Forgot Username' link
        login_page.click_forgot_username()
        
        # Step 3: Recover username
        username_recovery_page = UsernameRecoveryPage(driver)
        username_recovery_page.recover_username()
        
        # Step 4: Validate the results
        test_page = TC_LOGIN_003_TestPage(driver)
        assert test_page.is_recovery_successful(), "Username recovery validation failed"
        
    finally:
        driver.quit()
