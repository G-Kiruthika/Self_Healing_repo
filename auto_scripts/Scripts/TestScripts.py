<existing TestScripts.py content with the following appended test method>

def test_tc_login_016_unregistered_email_valid_password(driver):
    '''
    Test Case TC_LOGIN_016: Enter unregistered email and valid password, click login, validate error message for unregistered email, and confirm login is not successful.
    '''
    page = LoginPage(driver)
    result = page.execute_tc_login_016_unregistered_email_valid_password(email="unknown@example.com", password="ValidPass123")
    assert result["error_message"] is not None, "Error message for unregistered email should be shown."
    assert result["login_unsuccessful"] is True, "Login should not be successful with unregistered email."
