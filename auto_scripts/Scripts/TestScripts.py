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
    ...
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

# TC-SCRUM96_007: Automated Test for Registration, JWT, Profile API, and DB Validation
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage
from auto_scripts.Pages.ProfilePage import ProfilePage
import pytest
import pymysql

def test_TC_SCRUM96_007_registration_login_profile_db_validation():
    '''
    Automated test for TC_SCRUM96_007:
    1. Register and login a test user to obtain JWT
    2. Send GET request to /api/users/profile endpoint with JWT
    3. Validate all profile fields against DB
    '''
    user_data = {
        "username": "profileuser",
        "email": "profileuser@example.com",
        "password": "Profile123!",
        "firstName": "Profile",
        "lastName": "User"
    }
    db_config = {
        "host": "localhost",
        "user": "test",
        "password": "test",
        "database": "ecommerce"
    }
    # Step 1: Register and login user to obtain JWT
    reg_login_result = UserRegistrationAPIPage().tc_scrum96_007_register_and_login(user_data)
    jwt_token = reg_login_result["jwt_token"]
    assert jwt_token, "JWT token must be returned after registration and login"
    # Step 2 & 3: Fetch profile and validate against DB
    profile_result = ProfilePage.tc_scrum96_007_get_profile_and_validate(jwt_token, user_data, db_config)
    assert profile_result["status_code"] == 200, "Profile API must return 200 OK"
    assert profile_result["db_validation"] is True, "Profile data must match DB records"
