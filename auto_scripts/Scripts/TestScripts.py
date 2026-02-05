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
from auto_scripts.Pages.api_auth_page import ApiAuthPage
from auto_scripts.Pages.api_profile_page import ApiProfilePage
from auto_scripts.Pages.db_user_page import DbUserPage
import pytest


def test_TC_SCRUM96_007_user_profile_api_db_validation():
    """
    Test Case TC_SCRUM96_007: User Profile API & DB Validation
    Steps:
    1. Register and login a test user to obtain valid JWT authentication token
    2. Send GET request to /api/users/profile endpoint with valid JWT token in Authorization header
    3. Verify all profile fields match the registered user data in database
    """
    # Setup test user data
    user_data = {
        "username": "profileuser",
        "email": "profileuser@example.com",
        "password": "Profile123!",
        "firstName": "Profile",
        "lastName": "User"
    }
    db_config = {
        "host": "localhost",
        "user": "youruser",
        "password": "yourpass",
        "database": "yourdb"
    }
    # Step 1: Register user and login to get JWT token
    from pages.UserRegistrationAPIPage import UserRegistrationAPIPage
    registration_api = UserRegistrationAPIPage()
    jwt_token = registration_api.register_user_and_get_jwt(user_data)
    assert jwt_token is not None, "JWT token not found in registration/login response"

    # Step 2: Fetch user profile via API
    from ProfilePage import ProfilePage
    profile_page = ProfilePage(None)
    profile_response = profile_page.fetch_profile_api(jwt_token)
    assert profile_page.validate_profile_response(profile_response)

    # Step 3: Validate profile fields against database
    from pages.DatabaseValidationHelper import DatabaseValidationHelper
    db_helper = DatabaseValidationHelper(db_config)
    db_record = db_helper.get_user_from_db(user_data["username"])
    assert db_record is not None, "User not found in DB"
    assert db_helper.compare_db_and_api_profile(db_record, profile_response)

# TC_SCRUM96_005: Negative Login Audit Log Test
from auto_scripts.Pages.LoginPage import LoginPage
import datetime

def test_TC_SCRUM_96_005_negative_login_audit_log():
    ...
# TC_SCRUM96_008: Product Search API Case-Insensitive Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
import requests

def test_TC_SCRUM_96_008_product_search_case_insensitive():
    ...
