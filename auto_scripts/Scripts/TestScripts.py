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
