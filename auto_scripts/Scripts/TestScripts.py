# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage
from auto_scripts.Pages.UserSignupPage import UserSignupPage

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


def test_TC_SCRUM_96_002_signup_duplicate_email():
    """
    Test Case TC-SCRUM-96-002: User Signup and Duplicate Email Handling
    Steps:
    1. Create a user with email testuser@example.com (user1, Pass123!)
    2. Attempt to create another user with same email (user2, Pass456!)
    3. Verify only one user record exists in simulated DB
    """
    username1 = "user1"
    email = "testuser@example.com"
    password1 = "Pass123!"
    username2 = "user2"
    password2 = "Pass456!"
    signup_page = UserSignupPage()
    signup_page.run_signup_duplicate_email_flow(username1, email, password1, username2, password2)
