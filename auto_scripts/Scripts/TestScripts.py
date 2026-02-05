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

# TC-SCRUM-96-002: Duplicate Email Signup Handling
from auto_scripts.Pages.UserSignupPage import UserSignupPage

def test_TC_SCRUM_96_002_duplicate_email_signup(driver, db_connection):
    """
    Test Case TC-SCRUM-96-002: Duplicate Email Signup Handling
    Steps:
    1. Create user with email testuser@example.com (username: user1, password: Pass123!)
    2. Attempt to create another user with same email (username: user2, password: Pass456!)
    3. Verify only one user record exists in simulated DB for that email
    Acceptance criteria: Registration fails with 409 Conflict and error message 'Email already exists', DB contains only one record.
    """
    signup_page = UserSignupPage(driver)
    user1 = "user1"
    email = "testuser@example.com"
    pwd1 = "Pass123!"
    user2 = "user2"
    pwd2 = "Pass456!"
    # Register first user and then attempt to register duplicate
    first_result, second_result = signup_page.register_and_validate_duplicate(user1, email, pwd1, user2, pwd2)
    assert first_result["status"] == "success", f"Expected success for first user, got {first_result}"
    assert second_result["status"] == "conflict", f"Expected conflict for duplicate email, got {second_result}"
    assert "Email already exists" in second_result["message"], f"Expected error message 'Email already exists', got {second_result['message']}"
    # Database validation
    user_count = UserSignupPage.verify_user_count_in_db(db_connection, email)
    assert user_count == 1, f"Expected only one user record in DB for {email}, got {user_count}"
