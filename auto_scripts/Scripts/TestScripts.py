from auto_scripts.PageClasses.ProfileAPIValidationPage import ProfileAPIValidationPage
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
from auto_scripts.Pages.LoginPage import LoginPage

def test_tc_login_001_invalid_credentials(driver):
    ...[existing method code]...

def test_tc_login_005_empty_email(driver):
    """
    TC_LOGIN_005: Validate login attempt with empty email field.
    Steps:
      1. Attempt login with empty email and valid password ('Test@1234').
      2. Verify appropriate error message is displayed.
    """
    try:
        login_page = LoginPage(driver)
        result = login_page.validate_empty_email_login(password='Test@1234')
        assert result['success'] is False, f"Expected login failure, got success: {result}"
        assert 'email' in result['errors'], f"Expected email error, got: {result['errors']}"
    except Exception as e:
        raise AssertionError(f"TC_LOGIN_005 failed due to exception: {e}")

def test_tc_login_007_account_lockout(driver):
    """
    TC_LOGIN_007: Validate account lockout after repeated failed login attempts.
    Steps:
      1. Attempt login with incorrect password multiple times for 'testuser@example.com'.
      2. Attempt login with correct password after lockout.
      3. Verify account is locked and proper error is shown.
    """
    try:
        login_page = LoginPage(driver)
        result = login_page.validate_account_lockout_on_failed_logins(
            email='testuser@example.com',
            incorrect_password='WrongPass@1',
            valid_password='Test@1234'
        )
        assert result['locked'] is True, f"Expected account lockout, got: {result}"
        assert 'lockout' in result['errors'], f"Expected lockout error, got: {result['errors']}"
    except Exception as e:
        raise AssertionError(f"TC_LOGIN_007 failed due to exception: {e}")
