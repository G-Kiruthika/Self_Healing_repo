# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

def test_TC_SCRUM_96_001_api_signup():
    ...
# TC-SCRUM-96-001: User Signup Flow with UserSignupPage
from auto_scripts.Pages.UserSignupPage import UserSignupPage

def test_TC_SCRUM_96_001_user_signup_flow():
    ...
# TC-LOGIN-008: Minimum allowed length for login credentials
from auto_scripts.Pages.LoginPage import LoginPage

def test_TC_LOGIN_008_min_length_login(driver):
    ...
# TC-SCRUM-96-002: Duplicate Email Signup Handling
from auto_scripts.Pages.UserSignupPage import UserSignupPage

def test_TC_SCRUM_96_002_duplicate_email_signup(driver, db_connection):
    ...
# TC-LOGIN-10: Maximum allowed length for login credentials
from auto_scripts.Pages.LoginPage import LoginPage

def test_TC_LOGIN_10_max_length_login(driver):
    ...

# TC-SCRUM-96-003: Invalid Email Signup Handling
from auto_scripts.Pages.UserSignupPage import UserSignupPage

def test_TC_SCRUM_96_003_invalid_email_signup(driver, db_connection):
    """
    TC-SCRUM-96-003: Test signup with invalid email format.
    1. Send POST request to /api/users/signup with invalid email format.
    2. Verify error message indicates email format issue.
    3. Verify no user record is created in the database.
    """
    page = UserSignupPage(driver)
    username = 'testuser'
    invalid_email = 'invalidemail'
    password = 'Pass123!'
    # The page method should handle the POST and validations
    result = page.signup_with_invalid_email_and_validate(invalid_email, username, password, db_connection)

    # Assert API response status (e.g., 400 Bad Request)
    assert result['response'].status_code == 400, f"Expected 400, got {result['response'].status_code}"

    # Assert error message indicates email format issue
    assert 'email' in result['response'].json().get('error', '').lower(), \
        "Error message does not indicate email format issue"

    # Assert no user record is created in the database
    assert not result['db_user_exists'], "User record should not be created for invalid email"
