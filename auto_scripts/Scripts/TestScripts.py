# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

def test_TC_SCRUM_96_001_api_signup():
    ...
# TC-SCRUM96_006: Negative Login API & Session Validation Test
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage

def test_TC_SCRUM96_006_negative_login_api_and_session_validation():
    ...
# TC-SCRUM96_007: User Profile API & DB Validation Test
from auto_scripts.Pages.api_auth_page import ApiAuthPage
from auto_scripts.Pages.api_profile_page import ApiProfilePage
from auto_scripts.Pages.db_user_page import DbUserPage
import pytest

def test_TC_SCRUM96_007_user_profile_api_db_validation():
    ...
# TC-SCRUM96_005: Negative Login Audit Log Test
from auto_scripts.Pages.LoginPage import LoginPage
import datetime

def test_TC_SCRUM_96_005_negative_login_audit_log():
    ...
# TC-SCRUM96_008: Product Search API Case-Insensitive Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
import requests
import pymysql


def test_TC_SCRUM96_008_product_search_case_insensitive():
    ...
# TC-SCRUM96_009: Product Search API Edge Case Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
import requests
import pytest

def test_TC_SCRUM96_009_product_search_api_edge_case():
    ...
# TC-SCRUM96_010: Product Search API Special Character, SQL Injection, DB Integrity, Log Validation Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
import requests
import pymysql
import os
import datetime

def test_TC_SCRUM96_010_product_search_special_char_sql_injection_db_log():
    ...

# TC-SCRUM96_004: End-to-End Registration, Login, JWT Validation, Protected Endpoint Test
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage
from auto_scripts.Pages.JWTUtils import JWTUtils
from auto_scripts.Pages.ProfilePage import ProfilePage
import requests
import pytest

# New test for TC_SCRUM96_004

def test_TC_SCRUM96_004_registration_login_jwt_profile():
    """
    End-to-end test for user registration, login, JWT validation, and protected profile access.
    Steps:
    1. Register a test user account via API
    2. Log in via API and retrieve JWT
    3. Decode and validate JWT structure and claims
    4. Access protected profile endpoint using JWT
    """
    # Step 1: Register test user
    user_data = {
        "username": "logintest",
        "email": "logintest@example.com",
        "password": "ValidPass123!",
        "firstName": "Login",
        "lastName": "Test"
    }
    registration_response = LoginPage.register_user_api(user_data)
    assert registration_response["accountStatus"] == "ACTIVE", "User account should be ACTIVE after registration."
    assert registration_response["username"] == "logintest", "Username should match test data."
    assert registration_response["email"] == "logintest@example.com", "Email should match test data."

    # Step 2: Login via API
    login_response = LoginPage.login_api(user_data["username"], user_data["password"])
    access_token = login_response["accessToken"]
    assert access_token is not None, "JWT access token should be present in login response."
    assert login_response["tokenType"] == "Bearer", "Token type should be 'Bearer'."
    assert login_response["username"] == "logintest", "Username should match test data."
    assert login_response["email"] == "logintest@example.com", "Email should match test data."

    # Step 3: Decode and validate JWT
    jwt_payload = LoginPage.decode_and_validate_jwt(access_token)
    assert jwt_payload["sub"] == "logintest", "Subject claim in JWT should match username."
    assert jwt_payload["exp"] > jwt_payload["iat"], "Expiration time should be after issued at."

    # Step 4: Access protected profile endpoint
    profile_data = ProfilePage.access_profile_with_jwt(access_token)
    assert profile_data["username"] == "logintest", "Profile username should match test data."
    assert profile_data["email"] == "logintest@example.com", "Profile email should match test data."
    assert profile_data["accountStatus"] == "ACTIVE", "Account status should be ACTIVE in profile response."
    print("TC_SCRUM96_004 registration, login, JWT validation, and profile access PASSED.")

# TC-SCRUM-96-006: User Profile API Sensitive Data Exposure Test
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.ProfilePage import ProfilePage
import pytest

def test_TC_SCRUM_96_006_user_profile_api_sensitive_data_exposure():
    ...
# TC-SCRUM-96-007: User Profile Update and DB Verification Test
from auto_scripts.Pages.ProfilePage import ProfilePage
import pytest
import pymysql


def test_TC_SCRUM_96_007_profile_update_and_db_verification():
    ...
# TC-SCRUM-96-010: Cart API End-to-End Test
from auto_scripts.Pages.CartAPIPage import CartAPIPage
import pytest
import logging

def test_TC_SCRUM_96_010_cart_api_e2e():
    ...
# TC-SCRUM96_002: User Registration, Duplicate Registration, and DB Verification Test
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage
import pytest

def test_TC_SCRUM96_002_user_registration_duplicate_and_db_verification():
    ...

# TC-SCRUM96_003: Duplicate Email Registration and DB Verification Test
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage
import pytest

def test_TC_SCRUM96_003_duplicate_email_registration_and_db_verification():
    ...
