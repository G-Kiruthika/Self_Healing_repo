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
from auto_scripts.Pages.UserSignupPage import UserSignupPage

def test_TC_SCRUM_96_002_user_signup_duplicate_email():
    """
    Test Case TC-SCRUM-96-002: User Signup & Duplicate Email
    Steps:
    1. Create a user with email testuser@example.com
    2. Attempt to create another user with same email
    3. Verify only one user record exists in database
    """
    signup_page = UserSignupPage()
    user1 = {"username": "user1", "email": "testuser@example.com", "password": "Pass123!"}
    user2 = {"username": "user2", "email": "testuser@example.com", "password": "Pass456!"}
    # Step 1: Create user
    signup_page.create_user(user1["username"], user1["email"], user1["password"])
    # Step 2: Attempt duplicate signup and validate error
    signup_page.attempt_duplicate_user_and_validate(user2["username"], user2["email"], user2["password"])
    # Step 3: Verify only one user record in simulated DB
    signup_page.verify_only_one_user_in_db(user1["email"])
