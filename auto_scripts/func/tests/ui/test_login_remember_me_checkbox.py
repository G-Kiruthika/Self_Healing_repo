from auto_scripts.Pages.LoginPage import LoginPage
from core.driver_factory import get_driver

def test_login_remember_me_checkbox_absence():
    """
    TC_LOGIN_002: Validate Absence of 'Remember Me' Checkbox
    Steps:
        1. Navigate to the login screen.
        2. Assert that the 'Remember Me' checkbox is not present.
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    assert login_page.validate_remember_me_checkbox_absence() is True
    driver.quit()
