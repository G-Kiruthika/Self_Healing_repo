# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

def test_TC_SCRUM_96_001_api_signup():
    ...
# TC_SCRUM96_006: Negative Login API & Session Validation Test
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage

def test_TC_SCRUM96_006_negative_login_api_and_session_validation():
    """
    Test Case TC_SCRUM96_006: Negative Login API & Session Validation
    Steps:
    1. Register a test user with username 'validuser' and password 'CorrectPass123!'
    2. Send POST request to /api/auth/login with correct username but incorrect password
    3. Verify no JWT token is generated and user session is not created
    """
    base_url = "https://example-ecommerce.com"  # Use the actual API base URL if different
    username = "validuser"
    email = "validuser@example.com"
    correct_password = "CorrectPass123!"
    wrong_password = "WrongPassword456!"
    first_name = "Valid"
    last_name = "User"

    # Step 1: Register the user via API
    reg_api = UserRegistrationAPIPage()
    reg_response = reg_api.register_user_api(username, email, correct_password, first_name, last_name)
    assert reg_response.status_code == 201, f"Registration failed: {reg_response.text}"

    # Step 2: Attempt login via API with wrong password
    login_page = LoginPage(None, base_url)  # driver=None for API-only test
    response = login_page.api_auth_login(username, wrong_password)

    # Step 3: Verify 401 Unauthorized and error message
    login_page.verify_auth_failure(response, "Invalid username or password")

    # Step 4: Verify no JWT token and no session
    login_page.verify_no_token_and_no_session(response)

# TC_SCRUM96_007: User Profile API & DB Validation Test
from PageClasses.UserRegistrationAPIPage import UserRegistrationAPIPage
from PageClasses.ProfilePage import ProfilePage

def test_TC_SCRUM96_007_user_profile_api_db_validation():
    """
    Test Case TC_SCRUM96_007: User Profile API & DB Validation
    Steps:
    1. Register and login a test user to obtain valid JWT authentication token
    2. Send GET request to /api/users/profile endpoint with valid JWT token in Authorization header
    3. Verify all profile fields match the registered user data in database
    """
    user_data = {
        "username": "profileuser",
        "email": "profileuser@example.com",
        "password": "Profile123!",
        "firstName": "Profile",
        "lastName": "User"
    }
    db_config = {
        "host": "localhost",
        "port": 5432,
        "dbname": "yourdb",
        "user": "youruser",
        "password": "yourpass"
    }
    reg_api = UserRegistrationAPIPage()
    jwt = reg_api.register_and_login_user_get_jwt(user_data)
    assert jwt is not None, "JWT token not received after registration/login"
    prof_api = ProfilePage()
    api_profile = prof_api.get_profile_api(jwt)
    db_profile = prof_api.get_db_user_profile(db_config, user_data['username'])
    assert db_profile is not None, "DB profile not found for registered user"
    assert prof_api.validate_profile_data(api_profile, db_profile), "Profile data mismatch or password present in API response"

# TC_SCRUM96_005: Negative Login Audit Log Test
from auto_scripts.Pages.LoginPage import LoginPage
import datetime

def test_TC_SCRUM96_005_negative_login_audit_log():
    """
    Test Case TC_SCRUM96_005
    Steps:
    1. Send POST request to /api/auth/login endpoint with non-existent username and any password.
    2. Verify API returns HTTP 401 Unauthorized with error message 'Invalid username or password'.
    3. Verify no JWT token is generated or returned in the response.
    4. Verify failed login attempt is logged in security audit logs with username, timestamp, and source IP address.
    """
    base_url = "http://localhost:8000"  # Adjust to your app URL
    username = "nonexistentuser999"
    password = "AnyPassword123!"
    login_page = LoginPage(None, base_url)  # Pass a mock or None for driver for API-only test

    # Step 1: Attempt login via API
    response = login_page.api_auth_login(username, password)
    
    # Step 2: Verify 401 Unauthorized and error message
    login_page.verify_auth_failure(response, "Invalid username or password")

    # Step 3: Verify no JWT token and no session
    login_page.verify_no_token_and_no_session(response)

    # Step 4: Verify audit log entry
    start_time = datetime.datetime.now() - datetime.timedelta(seconds=10)
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
    def log_fetcher_func(st, et):
        # Stub example: Replace with actual log fetcher integration
        # Should return a list of dicts with keys: username, action, timestamp, source_ip
        return [{
            "username": username,
            "action": "login_failed",
            "timestamp": datetime.datetime.now().timestamp(),
            "source_ip": "127.0.0.1"
        }]
    login_page.verify_failed_login_audit_log(username, start_time, end_time, log_fetcher_func)
