# Existing imports and test methods...
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PageClasses.LoginPage import LoginPage
from PageClasses.DashboardPage import DashboardPage

# Existing test methods...

def test_TC_SCRUM_115_001_valid_login_session_established(driver):
    """
    Test Case TC-SCRUM-115-001
    Steps:
    1. Navigate to the e-commerce website login page
    2. Enter valid username in the username field
    3. Enter valid password in the password field
    4. Click on the Login button
    5. Verify user session is established (user profile/name is displayed in the header, session cookie is created)
    """
    login_url = "https://ecommerce.example.com/login"
    valid_username = "validuser@example.com"
    valid_password = "ValidPass123!"

    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    # Step 1: Navigate to the login page
    driver.get(login_url)
    assert login_page.is_on_login_page(), "Login page did not load properly."

    # Step 2: Enter valid username
    login_page.enter_email(valid_username)

    # Step 3: Enter valid password
    login_page.enter_password(valid_password)

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Verify dashboard is displayed and user session is established
    assert dashboard_page.is_dashboard_displayed(), "Dashboard not displayed after login."

    # Verify user profile/name is displayed in the header
    profile_name_locator = (By.CSS_SELECTOR, "header .profile-name")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(profile_name_locator),
        message="User profile/name not visible in header."
    )
    profile_name_element = driver.find_element(*profile_name_locator)
    assert profile_name_element.text != "", "Profile name is empty or not displayed."

    # Verify session cookie is created
    session_cookie = driver.get_cookie("sessionid")
    assert session_cookie is not None, "Session cookie 'sessionid' was not created."


# --- New test for TC_SCRUM74_001 appended below ---
from auto_scripts.Pages.TC_SCRUM74_001_TestPage import TC_SCRUM74_001_TestPage

def test_TC_SCRUM74_001_valid_login_workflow(driver):
    """
    Test Case TC_SCRUM74_001: Valid Login Workflow
    Steps:
    1. Navigate to the e-commerce website login page
    2. Enter valid email and password
    3. Click Login button
    4. Validate authentication and dashboard/profile display
    5. Validate session token creation
    """
    email = "validuser@example.com"
    password = "ValidPass123!"
    test_page = TC_SCRUM74_001_TestPage(driver)
    results = test_page.run_tc_scrum74_001(email, password)

    assert results["step_1_navigate_login"], f"Failed to navigate to login page: {results['exception']}"
    assert results["step_2_enter_email"], f"Failed to enter email: {results['exception']}"
    assert results["step_3_enter_password"], f"Failed to enter password: {results['exception']}"
    assert results["step_4_click_login"], f"Failed to click login: {results['exception']}"
    assert results["step_5_dashboard_displayed"], f"Dashboard not displayed: {results['exception']}"
    assert results["step_6_profile_displayed"], f"Profile not displayed: {results['exception']}"
    assert results["step_7_session_token_created"], f"Session token not created: {results['exception']}"
    assert results["overall_pass"], f"Test did not fully pass: {results['exception']}"
