import pytest
from auto_scripts.Pages.LoginPage import LoginPage

# Existing test methods ...

# TC_LOGIN_005: Blank email, valid password, expect error and login prevention
@pytest.mark.login
def test_tc_login_005_blank_email_valid_password(driver):
    login_page = LoginPage(driver)
    # Use the workflow method for TC_LOGIN_005
    login_page.tc_login_005_workflow()

# TC_LOGIN_007: Valid email, wrong password 5 times, lockout message, lockout persists with correct password
@pytest.mark.login
def test_tc_login_007_lockout_after_multiple_failed_attempts(driver):
    login_page = LoginPage(driver)
    # Use the workflow method for TC_LOGIN_007
    login_page.tc_login_007_workflow()
