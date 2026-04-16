"""
Selenium pytest automation script for TC-LOGIN-002: Negative Login Workflow (Invalid/Unregistered Email)

This script uses the TC_LOGIN_002_TestPage PageClass to validate:
- Navigation to login page
- Entering invalid email and password
- Clicking login
- Error message validation
- Ensuring user remains on login page

Test Data:
    - Email: invaliduser@example.com
    - Password: SomePassword123
"""
import pytest
from selenium import webdriver
from auto_scripts.Pages.TC_LOGIN_002_TestPage import TC_LOGIN_002_TestPage

@pytest.fixture(scope="module")
def driver():
    # Setup Chrome WebDriver (headless for CI)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.mark.tc_login_002
def test_tc_login_002_negative_login(driver):
    invalid_email = "invaliduser@example.com"
    password = "SomePassword123"
    test_page = TC_LOGIN_002_TestPage(driver)
    results = test_page.run_tc_login_002(invalid_email, password)

    # Step 1: Login page displayed
    assert results["step_1_navigate_login"], "Step 1 failed: Login page not displayed."
    # Step 2: Email entered
    assert results["step_2_enter_email"], "Step 2 failed: Invalid email not entered."
    # Step 3: Password entered
    assert results["step_3_enter_password"], "Step 3 failed: Password not entered."
    # Step 4: Login button clicked
    assert results["step_4_click_login"], "Step 4 failed: Login button not clicked."
    # Step 5: Error message validation
    assert results["step_5_error_message"] is not None, "Step 5 failed: Error message not displayed."
    assert "invalid email or password" in results["step_5_error_message"].lower(), (
        f"Step 5 failed: Unexpected error message: {results['step_5_error_message']}"
    )
    # Step 6: User remains on login page
    assert results["step_6_on_login_page"], "Step 6 failed: User is not on login page after failed login."
    # Overall pass
    assert results["overall_pass"], f"Test failed overall: {results['exception']}"
