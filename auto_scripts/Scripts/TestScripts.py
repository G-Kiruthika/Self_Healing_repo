# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

def test_TC_SCRUM_96_001_api_signup():
    ...
# TC_SCRUM96_006: Negative Login Test for Registered User
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage
import requests

def test_TC_SCRUM96_006_negative_login():
    """
    Test Case TC_SCRUM96_006: Negative Login Test for Registered User
    Steps:
    1. Register a test user with username 'validuser' and password 'CorrectPass123!'.
    2. Send POST request to /api/auth/login with correct username but wrong password.
    3. Verify 401 Unauthorized and error message.
    4. Verify no JWT token/session is created.
    """
    # Test Data
    username = 'validuser'
    email = 'validuser@example.com'
    password = 'CorrectPass123!'
    first_name = 'Valid'
    last_name = 'User'
    wrong_password = 'WrongPassword456!'

    # Step 1: Register user via API
    registration_page = UserRegistrationAPIPage()
    reg_response = registration_page.register_user_api(username, email, password, first_name, last_name)
    assert reg_response.status_code == 201, f"Expected 201 Created, got {reg_response.status_code}, response: {reg_response.text}"

    # Step 2 & 3: Attempt login with wrong password and verify failure
    login_page = LoginPage(driver=None, base_url=LoginPage.BASE_URL)
    response = login_page.api_auth_login(username, wrong_password)
    login_page.verify_auth_failure(response, "Invalid username or password")
    login_page.verify_no_token_and_no_session(response)
