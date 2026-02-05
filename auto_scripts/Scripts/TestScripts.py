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
    # End-to-end test
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

# TC-SCRUM-96-002: User Signup & Duplicate Email

def test_TC_SCRUM_96_002_user_signup_duplicate_email():
    """
    Test Case TC-SCRUM-96-002: User Signup & Duplicate Email
    Steps:
    1. Create a user with email testuser@example.com
       [Test Data: {"username": "user1", "email": "testuser@example.com", "password": "Pass123!"}]
       [Acceptance Criteria: AC-001]
       Expected: User created successfully
    2. Attempt to create another user with same email
       [Test Data: {"username": "user2", "email": "testuser@example.com", "password": "Pass456!"}]
       [Acceptance Criteria: AC-001]
       Expected: Registration fails with HTTP 409 Conflict status and error message 'Email already exists'
    3. Verify only one user record exists in database
       [Test Data: Query: SELECT COUNT(*) FROM users WHERE email='testuser@example.com']
       [Acceptance Criteria: AC-001]
       Expected: Database contains only one record for testuser@example.com
    """
    signup_page = UserSignupPage()
    result = signup_page.run_signup_duplicate_flow(
        first_user={"username": "user1", "email": "testuser@example.com", "password": "Pass123!"},
        second_user={"username": "user2", "email": "testuser@example.com", "password": "Pass456!"}
    )
    assert result["first_signup_success"], "First user signup failed"
    assert result["second_signup_status"] == 409, f"Expected HTTP 409 Conflict, got {result['second_signup_status']}"
    assert "Email already exists" in result["second_signup_error"], "Expected error message for duplicate email"
    assert result["user_count"] == 1, f"Expected only one user record, found {result['user_count']}"