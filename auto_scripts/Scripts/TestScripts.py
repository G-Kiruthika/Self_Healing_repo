# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

# TC_SCRUM96_001: User Registration API End-to-End Test
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage
import pytest
import datetime

def test_TC_SCRUM96_001_user_registration_api_e2e():
    """
    TC_SCRUM96_001: User Registration API End-to-End Test
    Steps:
    1. Send POST request to /api/users/register with test data
    2. Assert HTTP 201 Created and verify returned fields
    3. Query the database for user creation and validate email/account status
    4. Check registration confirmation email was sent
    """
    # Test Data
    username = "testuser001"
    email = "testuser001@example.com"
    password = "SecurePass123!"
    first_name = "John"
    last_name = "Doe"
    registration_api = UserRegistrationAPIPage()

    # Step 1: Send POST request to /api/users/register
    response = registration_api.register_user_api(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    # Step 2: Assert HTTP 201 Created and verify returned fields
    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}: {response.text}"
    resp_json = response.json()
    assert "userId" in resp_json, "userId not found in response"
    assert resp_json["username"] == username, "Username mismatch"
    assert resp_json["email"] == email, "Email mismatch"
    assert resp_json["firstName"] == first_name, "First name mismatch"
    assert resp_json["lastName"] == last_name, "Last name mismatch"
    assert "registrationTimestamp" in resp_json, "registrationTimestamp missing"
    assert "password" not in resp_json, "Password should not be returned in response"

    # Step 3: Query the database for user creation and validate email/account status
    user_db_record = registration_api.verify_single_user_in_db(username)
    assert user_db_record is not None, "User not found in DB after registration"
    assert user_db_record["email"] == email, "Email mismatch in DB"
    assert user_db_record["accountStatus"] in ["active", "pending"], "Unexpected account status in DB"

    # Step 4: Check registration confirmation email was sent (simulate if needed)
    email_sent = registration_api.verify_registration_confirmation_email_sent(email)
    assert email_sent, "Registration confirmation email was not sent"
    print("TC_SCRUM96_001 user registration API end-to-end test PASSED.")

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
    Test Case TC_SCRUM96_004: End-to-End user registration, login, JWT validation, and protected endpoint access.
    Steps:
    1. Register a test user account via POST /api/users/register
    2. Login via /api/auth/login and obtain JWT token
    3. Decode and validate JWT token claims
    4. Access protected /api/users/profile endpoint using JWT token
    """
    # Test Data
    username = "logintest"
    email = "logintest@example.com"
    password = "ValidPass123!"
    first_name = "Login"
    last_name = "Test"
    base_url = "https://example-ecommerce.com"

    # Step 1: Register user
    registration_api = UserRegistrationAPIPage()
    reg_response = registration_api.register_user_api(username, email, password, first_name, last_name)
    assert reg_response.status_code == 201, f"Registration failed: {reg_response.text}"
    reg_json = reg_response.json()
    assert reg_json["username"] == username, "Username mismatch after registration"
    assert reg_json["email"] == email, "Email mismatch after registration"
    assert reg_json["accountStatus"] == "active", "Account status not active after registration"

    # Step 2: Login and obtain JWT
    login_api = LoginPage(None, base_url)
    login_response = login_api.api_auth_login(username, password)
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    login_json = login_response.json()
    assert "token" in login_json, "No JWT token in login response"
    jwt_token = login_json["token"]
    assert "refreshToken" in login_json, "No refresh token in login response"
    assert login_json["tokenType"] == "Bearer", "Token type is not Bearer"
    assert login_json["userId"] is not None, "userId missing in login response"
    assert login_json["username"] == username, "Username mismatch in login response"
    assert login_json["email"] == email, "Email mismatch in login response"

    # Step 3: Decode and validate JWT
    payload = JWTUtils.validate_jwt(jwt_token, expected_sub=username)
    assert payload["sub"] == username, "JWT subject claim mismatch"

    # Step 4: Access protected endpoint
    profile_data = ProfilePage.get_profile(jwt_token)
    assert profile_data["username"] == username, "Profile username mismatch"
    assert profile_data["email"] == email, "Profile email mismatch"
    assert "userId" in profile_data, "userId missing in profile response"
    assert "accountStatus" in profile_data, "accountStatus missing in profile response"
    assert "password" not in profile_data, "Password should not be present in profile response"
    print("TC_SCRUM96_004 registration, login, JWT validation, profile access test PASSED.")

# TC_SCRUM96_002: Duplicate User Registration API Test
import pytest
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage

def test_TC_SCRUM96_002_duplicate_user_registration_api():
    """
    TC_SCRUM96_002: Duplicate User Registration API Test
    Steps:
    1. Register user 'duplicateuser' with email 'first@example.com' (expect HTTP 201)
    2. Attempt duplicate registration with same username, different email (expect HTTP 409)
    3. Verify only one user record exists in DB with username 'duplicateuser' and email 'first@example.com'
    """
    # Setup database config if needed
    db_config = {
        "host": "localhost",
        "user": "db_user",
        "password": "db_pass",
        "database": "ecommerce_db"
    }
    api_page = UserRegistrationAPIPage(db_config=db_config)

    # Step 1: Register first user
    response1 = api_page.register_user_api(
        username="duplicateuser",
        email="first@example.com",
        password="Pass123!",
        first_name="First",
        last_name="User"
    )
    assert response1.status_code == 201, f"Expected HTTP 201 Created, got {response1.status_code}: {response1.text}"

    # Step 2: Attempt duplicate registration
    response2 = api_page.register_user_api(
        username="duplicateuser",
        email="second@example.com",
        password="Pass456!",
        first_name="Second",
        last_name="User"
    )
    assert response2.status_code == 409, f"Expected HTTP 409 Conflict, got {response2.status_code}: {response2.text}"
    resp_json = response2.json()
    assert "error" in resp_json, "Error message not present in response"
    assert "username already exists" in resp_json["error"].lower(), f"Expected error 'username already exists', got '{resp_json['error']}'"

    # Step 3: DB verification
    count, db_email = api_page.verify_single_user_in_db("duplicateuser", "first@example.com")
    assert count == 1, f"Expected exactly one user record, found {count}"
    assert db_email == "first@example.com", f"Expected email 'first@example.com', got '{db_email}'"
    print("TC_SCRUM96_002 duplicate user registration API test PASSED.")
