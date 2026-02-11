from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
from auto_scripts.Pages.TC_LOGIN_003_TestPage import TC_LOGIN_003_TestPage
from core.driver_factory import get_driver
import pytest

@pytest.mark.ui
def test_tc_login_003_forgot_username_workflow():
    """
    Test Case TC_LOGIN_003: End-to-end Forgot Username workflow.
    Steps:
      1. Navigate to login screen.
      2. Click on 'Forgot Username' link.
      3. Follow instructions to recover username.
    """
    driver = get_driver()
    email = "testuser@example.com"  # Replace with valid test email
    test_page = TC_LOGIN_003_TestPage(driver)
    results = test_page.execute_tc_login_003(email)

    assert results["step_1_navigate_login"], "Login screen is not displayed."
    assert results["step_2_forgot_username_clicked"], "Failed to click 'Forgot Username' link."
    assert results["step_3_recovery_success"], f"Username recovery failed: {results.get('error_message', results.get('exception'))}"
    assert results["overall_pass"], f"Test did not pass: {results.get('exception', 'Unknown error')}"
    assert results["confirmation_message"] is not None, "Confirmation message not received."
    driver.quit()
