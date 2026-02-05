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
