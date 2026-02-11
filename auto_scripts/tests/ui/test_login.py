from auto_scripts.Pages.TC_LOGIN_003_TestPage import TC_LOGIN_003_TestPage
from core.driver_factory import get_driver
import pytest

@pytest.mark.login
def test_tc_login_003_forgot_username():
    driver = get_driver()
    try:
        test_page = TC_LOGIN_003_TestPage(driver)
        email = "testuser@example.com"  # Replace with valid test email
        results = test_page.execute_tc_login_003(email)
        assert results["step_1_navigate_login"] is True, f"Login screen not displayed: {results['exception']}"
        assert results["step_2_forgot_username_clicked"] is True, f"Failed to click 'Forgot Username': {results['exception']}"
        assert results["step_3_recovery_success"] is True, f"Username recovery failed: {results['error_message']}"
        assert results["overall_pass"] is True, f"Test did not pass overall: {results['exception']}"
        assert results["confirmation_message"] is not None, "Confirmation message missing"
    finally:
        driver.quit()
