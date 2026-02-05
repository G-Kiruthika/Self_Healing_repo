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
