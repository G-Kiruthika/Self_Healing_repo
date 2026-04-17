# Existing imports and test methods...
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PageClasses.LoginPage import LoginPage
from PageClasses.DashboardPage import DashboardPage

# Existing test methods...

def test_TC_SCRUM_115_001_valid_login_session_established(driver):
    ...<existing test code>...

# --- New test for TC_SCRUM74_001 appended below ---
from auto_scripts.Pages.TC_SCRUM74_001_TestPage import TC_SCRUM74_001_TestPage

def test_TC_SCRUM74_001_valid_login_workflow(driver):
    ...<existing test code>...

# --- New test for TC_LOGIN_006 appended below ---
from auto_scripts.Pages.TC_LOGIN_006_TestPage import TC_LOGIN_006_TestPage

@pytest.mark.tc_login_006
def test_TC_LOGIN_006_valid_username_empty_password(driver):
    ...<existing test code>...

# --- Appended test for TC_SCRUM74_001 below ---
@pytest.mark.tc_scrum74_001
def test_TC_SCRUM74_001_valid_login_e2e(driver):
    ...<existing test code>...

# --- Appended test for TC_LOGIN_010 below ---
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

@pytest.mark.tc_login_010
def test_TC_LOGIN_010_password_recovery_workflow(driver):
    """
    Test Case TC_LOGIN_010:
    1. Navigate to the login page (https://ecommerce.example.com/login)
    2. Click the Forgot Password link (redirects to https://ecommerce.example.com/password-recovery)
    3. Verify password recovery page elements: email input field and submit button
    4. Enter registered email address (testuser@example.com)
    5. Click Submit button
    6. Validate success message is displayed
    """
    recovery_email = "testuser@example.com"

    # Step 1: Navigate to password recovery page directly
    recovery_page = PasswordRecoveryPage(driver)
    recovery_page.go_to_password_recovery_page()

    # Step 2: Verify page elements
    assert recovery_page.verify_page_elements(), "Password recovery elements not found."

    # Step 3: Enter email
    recovery_page.enter_email(recovery_email)

    # Step 4: Click submit
    recovery_page.click_submit()

    # Step 5: Validate success message
    success_msg = recovery_page.get_success_message()
    assert success_msg is not None and success_msg.strip() != "", "Success message not displayed after password recovery."

# --- Appended test for TC_LOGIN_001 below ---
from auto_scripts.Pages.TC_LOGIN_001_TestPage import TC_LOGIN_001_TestPage

@pytest.mark.tc_login_001
def test_TC_LOGIN_001_valid_login_workflow(driver):
    """
    Test Case TC_LOGIN_001:
    1. Navigate to the login page (https://ecommerce.example.com/login)
    2. Enter valid registered email address (testuser@example.com)
    3. Enter valid password (ValidPass123!)
    4. Click Login button
    5. Assert user is redirected to dashboard/home page (dashboard header/profile icon visible)
    """
    email = "testuser@example.com"
    password = "ValidPass123!"
    test_page = TC_LOGIN_001_TestPage(driver)
    results = test_page.run_tc_login_001(email, password)
    assert results["step_1_navigate_login"], f"Login page not displayed: {results.get('exception')}"
    assert results["step_2_enter_email"], "Email entry failed"
    assert results["step_3_enter_password"], "Password entry failed"
    assert results["step_4_click_login"], "Login button click failed"
    assert results["step_5_dashboard_displayed"], "Dashboard header not visible after login"
    assert results["step_6_profile_displayed"], "User profile icon not visible after login"
    assert results["step_7_session_token_created"], "Session token not created"
    assert results["overall_pass"], f"TC_LOGIN_001 failed: {results.get('exception')}"