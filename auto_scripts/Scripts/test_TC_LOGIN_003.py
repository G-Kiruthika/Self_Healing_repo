import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.TC_LOGIN_003_TestPage import TC_LOGIN_003_TestPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_003_negative_login_and_username_recovery(driver):
    """
    Test Case TC-LOGIN-003: Negative login scenario with username recovery
    Steps:
      1. Navigate to login page
      2. Enter valid registered email address
      3. Enter incorrect password
      4. Click Login button
      5. Assert error message is displayed
      6. Assert user remains on login page
      7. Click 'Forgot Username' link
      8. Recover username and assert confirmation
    """
    email = "testuser@example.com"
    wrong_password = "WrongPassword456"
    test_page = TC_LOGIN_003_TestPage(driver)

    # Step 1-8: Execute test flow
    results = test_page.execute_tc_login_003(email, wrong_password)

    # Step 1: Navigate to login page
    assert results["step_1_navigate_login"] is True, "Login page was not displayed."
    
    # Step 2: Enter valid registered email address
    assert results["step_2_enter_email"] is True, "Email was not entered correctly."

    # Step 3: Enter incorrect password
    assert results["step_3_enter_wrong_password"] is True, "Password was not entered (masked)."

    # Step 4: Click Login button
    assert results["step_4_click_login"] is True, "Login button was not clicked."

    # Step 5: Assert error message
    assert results["step_5_error_message"] is not None, "No error message displayed."
    assert "invalid email or password" in results["step_5_error_message"].lower(), \
        f"Unexpected error message: {results['step_5_error_message']}"

    # Step 6: Assert user remains on login page
    assert results["step_6_on_login_page"] is True, "User is not on login page after failed login."

    # Step 7: Click 'Forgot Username' link
    assert results["step_7_forgot_username_clicked"] is True, \
        f"Failed to click 'Forgot Username': {results.get('exception', '')}"

    # Step 8: Recover username and assert confirmation
    assert results["step_8_recovery_success"] is True, \
        f"Username recovery failed: {results.get('exception', '')}"
    assert results["confirmation_message"] is not None, "No confirmation message after username recovery."

    # Overall test pass
    assert results["overall_pass"] is True, \
        f"Test did not pass overall: {results.get('exception', '')}"
