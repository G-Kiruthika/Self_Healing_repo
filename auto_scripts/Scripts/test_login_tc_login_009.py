# test_login_tc_login_009.py
"""
Automated Selenium Test Script for TC-LOGIN-009
Validates system behavior with extremely long password input (>1000 chars).

Traceability:
- Test Case ID: 236
- Acceptance Criteria: TS-007
- PageClass: LoginPage
- Script Location: auto_scripts/Scripts/test_login_tc_login_009.py

Author: Enterprise Automation Agent
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import string

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


def test_tc_login_009_extremely_long_password(driver):
    """
    Steps:
        1. Navigate to login page
        2. Enter valid email
        3. Enter extremely long password (>1000 chars)
        4. Click Login
        5. Validate error/truncation and login prevention
    """
    # Step 1: Navigate to login page
    login_page = LoginPage(driver)
    long_password = 'VeryLongPassword' * 80  # 80*16 = 1280 chars
    email = 'testuser@example.com'
    results = login_page.run_tc_login_009_extremely_long_password(email, long_password)

    # Step 1 Assert: Login page is displayed
    assert results['step_1_navigate_login'] is True, f"Step 1 Failed: {results.get('exception', 'Login page not visible')}"

    # Step 2 Assert: Email entered correctly
    assert results['step_2_enter_email'] is True, "Step 2 Failed: Email entry not successful."

    # Step 3 Assert: Long password entered
    assert results['step_3_enter_long_password'] is True, "Step 3 Failed: Password entry not successful."

    # Step 4 Assert: Login button clicked
    assert results['step_4_click_login'] is True, "Step 4 Failed: Login button not clicked."

    # Step 5 Assert: Error message or validation error is present
    error_present = results['step_5_error_message'] or results['step_6_validation_error']
    assert error_present, f"Step 5 Failed: No error/validation message. Actual: {results['step_5_error_message']} | {results['step_6_validation_error']}"

    # Step 6 Assert: Login is prevented (still on login page)
    assert results['step_7_login_prevented'] is True, "Step 6 Failed: User not prevented from login."

    # Final Assert: Test overall pass
    assert results['overall_pass'] is True, f"Overall Test Failed: Exception={results['exception']}"

    # Traceability output
    print("TC-LOGIN-009 Results:", results)
