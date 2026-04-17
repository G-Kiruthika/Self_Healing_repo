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
    ...<existing test code>...

# --- Appended test for TC_LOGIN_001 below ---
from auto_scripts.Pages.TC_LOGIN_001_TestPage import TC_LOGIN_001_TestPage

@pytest.mark.tc_login_001
def test_TC_LOGIN_001_valid_login_workflow(driver):
    ...<existing test code>...

# --- Appended test for TC_LOGIN_004 below ---
from auto_scripts.Pages.TC_LOGIN_004_TestPage import TC_LOGIN_004_TestPage

@pytest.mark.tc_login_004
def test_TC_LOGIN_004_empty_username_valid_password(driver):
    """
    TC-SCRUM-115-004:
    1. Navigate to login page
    2. Leave username field empty
    3. Enter valid password (ValidPass123!)
    4. Click Login
    5. Validate error message: 'Username is required. Please enter your username.'
    6. Validate username field is highlighted in red, error icon is shown, and focus is set to the field.
    """
    page = TC_LOGIN_004_TestPage(driver)
    page.navigate_to_login()
    page.enter_username("")  # Leave username empty
    page.enter_password("ValidPass123!")
    page.click_login()
    
    # Validate error message
    error_msg = page.get_username_error_message()
    assert error_msg == 'Username is required. Please enter your username.', f"Expected error message, got: {error_msg}"

    # Validate username field is highlighted in red
    assert page.is_username_field_highlighted_red(), "Username field should be highlighted in red."

    # Validate error icon is shown
    assert page.is_username_error_icon_visible(), "Error icon should be visible for username field."

    # Validate focus is set to username field
    assert page.is_username_field_focused(), "Focus should be set to the username field."
