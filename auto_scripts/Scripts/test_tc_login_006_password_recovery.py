# Test Script for TC-LOGIN-006: Password Recovery Navigation and UI Validation
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
from selenium.common.exceptions import WebDriverException

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_006_navigate_and_verify_password_recovery(driver):
    """
    TC-LOGIN-006: Verify navigation from Login to Password Recovery and UI correctness
    Steps:
    1. Navigate to login page and verify 'Forgot Password' link
    2. Click 'Forgot Password' and verify navigation to recovery page
    3. Validate UI elements on password recovery page
    """
    login_page = LoginPage(driver)

    # Step 1 & 2: Navigate and click 'Forgot Password' link
    result = login_page.tc_login_006_navigate_to_password_recovery()
    assert result, "Failed to navigate to password recovery page via 'Forgot Password' link."

    # Step 3: Verify Password Recovery Page UI
    recovery_page = PasswordRecoveryPage(driver)
    try:
        ui_result = recovery_page.tc_login_006_verify_password_recovery_page_ui()
        assert ui_result, "Password Recovery page UI validation failed."
    except AssertionError as ae:
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(f"Unexpected error during Password Recovery UI validation: {e}")
