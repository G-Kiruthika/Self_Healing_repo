# Existing content of TestScripts.py

# --- TC_LOGIN_016: Login with unregistered email and valid password ---
def test_tc_login_016_unregistered_email(driver):
    """
    TC_LOGIN_016 Steps:
    1. Navigate to the login page.
    2. Enter unregistered email and valid password.
    3. Click the 'Login' button.
    Expected: Error message for unregistered email is shown, login not successful.
    """
    from auto_scripts.Pages.LoginPage import LoginPage
    page = LoginPage(driver)
    result = page.tc_login_016_unregistered_email('unknown@example.com', 'ValidPass123')
    assert result, "Test failed: Error message for unregistered email not shown or login succeeded unexpectedly."

# --- TC010: Multiple failed login attempts, lockout, and error message verification ---
def test_tc010_multiple_failed_logins_and_lockout(driver):
    """
    TC010 Steps:
    1. Attempt login with invalid password 5 times. [Test Data: user@example.com / WrongPassword]
        - Verify login fails and error message displayed each time.
    2. Attempt login with correct credentials after lockout. [Test Data: user@example.com / ValidPassword123]
        - Verify 'Account locked due to multiple failed attempts' error message is displayed.
    Acceptance Criteria: 6
    """
    from auto_scripts.Pages.LoginPage import LoginPage
    page = LoginPage(driver)
    result = page.tc010_attempt_multiple_failed_logins_and_verify_lockout(
        email='user@example.com',
        wrong_password='WrongPassword',
        correct_password='ValidPassword123'
    )
    assert result, "Test failed: TC010 acceptance criteria not met (failed login/error message/lockout error)."
