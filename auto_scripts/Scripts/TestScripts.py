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
    """
    TC_LOGIN_001: Valid Login Workflow
    Steps:
      1. Navigate to login page (https://ecommerce.example.com/login)
      2. Enter valid email (testuser@example.com)
      3. Enter valid password (ValidPass123!)
      4. Click Login button
      5. Assert user is logged in and redirected to dashboard
    """
    test_page = TC_LOGIN_001_TestPage(driver)
    result = test_page.run_tc_login_001(email="testuser@example.com", password="ValidPass123!")
    assert isinstance(result, dict), "Result should be a dictionary with step outcomes"
    for step, passed in result.items():
        assert passed, f"Step '{step}' did not pass"

# --- Appended test for TC_LOGIN_004 below ---
from auto_scripts.Pages.TC_LOGIN_004_TestPage import TC_LOGIN_004_TestPage

@pytest.mark.tc_login_004
def test_TC_LOGIN_004_empty_username_valid_password(driver):
    ...<existing test code>...
