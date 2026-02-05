# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

def test_TC_SCRUM_96_001_api_signup():
    """
    Test Case TC-SCRUM-96-001: API Signup Automation
    Steps:
    1. Send POST request to /api/users/signup with valid user data (username, email, password)
    2. Validate HTTP 201 response and correct schema (userId, username, email, no password)
    3. Verify user data is stored in database with hashed password and correct details
    """
    username = "testuser123"
    email = "testuser@example.com"
    password = "SecurePass123!"
    api_signup_page = APISignupPage()
    assert api_signup_page.run_full_signup_test(username, email, password), "Signup test failed"

# TC-SCRUM-96-001: User Signup Flow with UserSignupPage
from auto_scripts.Pages.UserSignupPage import UserSignupPage

def test_TC_SCRUM_96_001_user_signup_flow():
    """
    Test Case TC-SCRUM-96-001: User Signup Flow
    Steps:
    1. Send POST request to /api/users/signup with valid user data
    2. Validate HTTP 201 response and correct schema
    3. Verify user data is stored in simulated DB with hashed password
    """
    username = "testuser123"
    email = "testuser@example.com"
    password = "SecurePass123!"
    signup_page = UserSignupPage()
    signup_page.run_signup_flow(username, email, password)

# TC-LOGIN-008: Minimum allowed length for login credentials
from auto_scripts.Pages.LoginPage import LoginPage

def test_TC_LOGIN_008_min_length_login(driver):
    """
    Test Case TC_LOGIN_008: Minimum allowed length for login credentials
    Steps:
    1. Navigate to the login page.
    2. Enter email and password with minimum allowed length (email: a@b.co, password: 123456).
    3. Click Login and assert login is accepted if credentials are valid.
    Acceptance Criteria: 8
    """
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    assert login_page.is_min_length_accepted("a@b.co", "123456"), "Minimum length credentials were not accepted."

# TC-SCRUM-96-002: Duplicate Email Signup Handling
from auto_scripts.Pages.UserSignupPage import UserSignupPage

def test_TC_SCRUM_96_002_duplicate_email_signup():
    """
    Test Case TC-SCRUM-96-002: Duplicate Email Signup Handling
    Steps:
    1. Create user with email testuser@example.com (username: user1, password: Pass123!)
    2. Attempt to create another user with same email (username: user2, password: Pass456!)
    3. Verify only one user record exists in simulated DB for that email
    Acceptance criteria: Registration fails with 409 Conflict and error message 'Email already exists', DB contains only one record.
    """
    signup_page = UserSignupPage()
    signup_page.signup_duplicate_email_test()

# TC-SCRUM-96-003: Invalid Email Signup Automation Test
from auto_scripts.Pages.UserSignupPage import UserSignupPage

def test_TC_SCRUM_96_003_invalid_email_signup(driver, db_connection):
    """
    Test Case TC-SCRUM-96-003: Invalid Email Signup Automation
    Steps:
    1. Send POST request to /api/users/signup with invalid email format (username: testuser, email: invalidemail, password: Pass123!)
    2. Validate HTTP 400 response and error messaging
    3. Perform equivalent UI flow and check for error message
    4. Query database to confirm no user record was created
    """
    signup_page = UserSignupPage(driver)
    result = signup_page.signup_with_invalid_email_and_validate(
        invalid_email="invalidemail",
        username="testuser",
        password="Pass123!",
        db_connection=db_connection
    )
    assert result["db_user_count"] == 0, f"User with invalid email should not be created. Found {result['db_user_count']} records."
    assert "invalid email" in result["ui_error_message"].lower() or "email format" in result["ui_error_message"].lower(), f"Expected email format error in UI, got: {result['ui_error_message']}"
    assert "invalid email" in result["api_response"].lower() or "email format" in result["api_response"].lower(), f"Expected email format error in API response, got: {result['api_response']}"

# TC-LOGIN-07-02: Short email and password negative login scenario
from auto_scripts.Pages.LoginPage import LoginPage

def test_TC_LOGIN_07_02_short_email_and_password(driver):
    """
    Test Case TC_LOGIN_07_02: Short email and password negative login scenario
    Steps:
    1. Navigate to the login page.
    2. Enter an email address shorter than the minimum allowed length (e.g., 1 character).
    3. Enter a password shorter than the minimum allowed length (e.g., 3 characters).
    4. Click the 'Login' button.
    Expected: System displays an error or prevents login; appropriate error message is shown.
    """
    login_page = LoginPage(driver)
    login_page.test_login_with_short_email_and_password(email="a@", password="abc")
