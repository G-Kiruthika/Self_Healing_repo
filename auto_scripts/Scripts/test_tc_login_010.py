import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.TC_LOGIN_010_TestPage import TC_LOGIN_010_TestPage

# Test Data
LOGIN_URL = "https://app.example.com/login"  # As per PageClass
EMAIL_WITH_SPECIAL_CHARS = "test.user+tag@example.com"
VALID_PASSWORD = "ValidPass123!"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def test_tc_login_010_special_char_email(driver):
    """
    TC-LOGIN-010: Login with email containing special characters
    Acceptance Criteria: 
    - Login page is displayed
    - Email with special characters is accepted
    - Password is entered and masked
    - If credentials are valid, login succeeds; otherwise appropriate error is shown
    """
    page = TC_LOGIN_010_TestPage(driver)
    results = page.run_tc_login_010(EMAIL_WITH_SPECIAL_CHARS, VALID_PASSWORD)

    # Step 1: Login page is displayed
    assert results["step_1_navigate_login"], "Login page did not display."

    # Step 2: Email with special characters is accepted
    assert results["step_2_enter_email"], "Email with special characters was not accepted."

    # Step 3: Password is entered and masked
    assert results["step_3_enter_password"], "Password was not entered or not masked."

    # Step 4: Click Login button
    assert results["step_4_click_login"], "Login button was not clicked."

    # Step 5: If credentials are valid, login succeeds; otherwise error is shown
    # Since we do not know if the credentials are valid, check for error or login page state
    if results["step_5_error_message"] or results["step_6_validation_error"]:
        # Error message or validation error present
        assert results["step_7_login_prevented"], (
            f"Login should be prevented, but was not. Error: {results['step_5_error_message']}, Validation: {results['step_6_validation_error']}"
        )
    else:
        # No error, check if not on login page (login succeeded)
        assert not results["step_7_login_prevented"], "Login did not succeed when it should have."

    # No unexpected exception
    assert not results["exception"], f"Unexpected exception: {results['exception']}"
