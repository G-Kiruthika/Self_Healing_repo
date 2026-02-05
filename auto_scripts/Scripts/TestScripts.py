# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

def test_TC_SCRUM_96_001_api_signup():
    ...
# TC_SCRUM96_006: Negative Login API & Session Validation Test
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage

def test_TC_SCRUM96_006_negative_login_api_and_session_validation():
    ...

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
