# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

# TC_SCRUM96_001: User Registration API End-to-End Test
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage
import pytest
import datetime

def test_TC_SCRUM96_001_user_registration_api_e2e():
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
    ...
# TC_SCRUM96_005: Negative Login Audit Log Test
from auto_scripts.Pages.LoginPage import LoginPage
import datetime

def test_TC_SCRUM_96_005_negative_login_audit_log():
    ...
# TC_SCRUM96_008: Product Search API Case-Insensitive Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
import requests
import pymysql


def test_TC_SCRUM96_008_product_search_case_insensitive():
    ...
# TC_SCRUM96_009: Product Search API Edge Case Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
import requests
import pymysql

def test_TC_SCRUM96_009_product_search_edge_cases():
    ...
# TC_SCRUM96_010: Product Search API Special Character, SQL Injection, DB Integrity, Log Validation Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
import requests
import pymysql
import os
import datetime

def test_TC_SCRUM96_010_product_search_special_char_sql_injection_db_log():
    ...

# TC_SCRUM96_004: End-to-End Registration, Login, JWT Validation, Protected Endpoint Test
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage
from auto_scripts.Pages.JWTUtils import JWTUtils
from auto_scripts.Pages.ProfilePage import ProfilePage
import requests
import pytest

def test_TC_SCRUM96_004_registration_login_jwt_profile():
    """
    Test Case TC_SCRUM96_004: End-to-End Registration, Login, JWT Validation, Protected Endpoint Test
    Steps:
    1. Register a test user account via POST /api/users/register
    2. Login via /api/auth/login and extract JWT
    3. Decode and validate JWT claims
    4. Access protected endpoint /api/users/profile
    """
    # Step 1: Register user
    registration_api = UserRegistrationAPIPage()
    user_data = {
        "username": "logintest",
        "email": "logintest@example.com",
        "password": "ValidPass123!",
        "firstName": "Login",
        "lastName": "Test"
    }
    registration_response = registration_api.register_user(user_data)
    assert registration_response.status_code == 201 or registration_response.status_code == 200, f"Registration failed: {registration_response.text}"

    # Step 2: Login and extract JWT
    login_api = LoginPage()
    credentials = {
        "username": "logintest",
        "password": "ValidPass123!"
    }
    login_response = login_api.login_user(credentials)
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    login_json = login_response.json()
    jwt_token = login_json.get("accessToken") or login_json.get("jwt")
    refresh_token = login_json.get("refreshToken")
    token_type = login_json.get("tokenType")
    user_details = {
        "userId": login_json.get("userId"),
        "username": login_json.get("username"),
        "email": login_json.get("email")
    }
    assert jwt_token is not None, "JWT token missing in login response"
    assert token_type == "Bearer", f"Token type mismatch: {token_type}"
    assert user_details["username"] == "logintest", f"Username mismatch: {user_details['username']}"
    assert user_details["email"] == "logintest@example.com", f"Email mismatch: {user_details['email']}"

    # Step 3: Decode and validate JWT
    jwt_utils = JWTUtils()
    payload = jwt_utils.decode_jwt(jwt_token)
    assert jwt_utils.validate_jwt_claims(payload, expected_username="logintest", expiration_seconds=86400), "JWT claims validation failed"

    # Step 4: Access protected endpoint
    profile_api = ProfilePage()
    profile_response = profile_api.get_profile(jwt_token)
    assert profile_response.status_code == 200, f"Profile endpoint failed: {profile_response.text}"
    profile_json = profile_response.json()
    assert profile_json.get("username") == "logintest", f"Profile username mismatch: {profile_json.get('username')}"
    assert profile_json.get("email") == "logintest@example.com", f"Profile email mismatch: {profile_json.get('email')}"

# TC_SCRUM96_002: Duplicate Username Registration and DB Verification Test
from PageClasses.UserRegistrationAPIPage import UserRegistrationAPIPage
from PageClasses.UserDatabaseVerifier import UserDatabaseVerifier
import pytest

def test_TC_SCRUM96_002_duplicate_username_registration_and_db_verification():
    """
    TC_SCRUM96_002: Duplicate Username Registration and DB Verification
    Steps:
    1. Register a user with username 'duplicateuser', email 'first@example.com', password 'Pass123!', firstName 'First', lastName 'User'.
    2. Attempt to register another user with the same username 'duplicateuser', but different email 'second@example.com'.
    3. Verify only one user record exists in DB with username 'duplicateuser' and email 'first@example.com'.
    """
    # Step 1: Register initial user
    registration_api = UserRegistrationAPIPage()
    user_data_1 = {
        "username": "duplicateuser",
        "email": "first@example.com",
        "password": "Pass123!",
        "firstName": "First",
        "lastName": "User"
    }
    registration_api.register_user(user_data_1)

    # Step 2: Attempt duplicate registration
    user_data_2 = {
        "username": "duplicateuser",
        "email": "second@example.com",
        "password": "Pass456!",
        "firstName": "Second",
        "lastName": "User"
    }
    registration_api.register_duplicate_user(user_data_2)

    # Step 3: Verify DB
    db_verifier = UserDatabaseVerifier(host='localhost', dbname='ecommerce', user='testuser', password='testpass')
    count = db_verifier.count_users_by_username("duplicateuser")
    assert count == 1, f"Expected 1 user with username 'duplicateuser', found {count}"
    db_user = db_verifier.get_user_by_username("duplicateuser")
    assert db_user is not None, "No user found in DB with username 'duplicateuser'"
    assert db_user[0] == "duplicateuser", f"Expected username 'duplicateuser', found {db_user[0]}"
    assert db_user[1] == "first@example.com", f"Expected email 'first@example.com', found {db_user[1]}"
    db_verifier.close()
    print("TC_SCRUM96_002 duplicate username registration and DB verification PASSED.")
