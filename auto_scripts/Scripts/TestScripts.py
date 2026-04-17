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
    ...
# TC_SCRUM96_002: Duplicate Username Registration and DB Verification Test
from PageClasses.UserRegistrationAPIPage import UserRegistrationAPIPage
from PageClasses.UserDatabaseVerifier import UserDatabaseVerifier
import pytest

def test_TC_SCRUM96_002_duplicate_username_registration_and_db_verification():
    ...

# TC_SCRUM96_005: Negative Login API Audit Log Test (Generated)
from PageClasses.LoginNegativeAPIPage import LoginNegativeAPIPage
import pytest
import datetime

def test_TC_SCRUM96_005_negative_login_api_audit_log():
    ...

import pytest
from auto_scripts.PageClasses.LoginPage import LoginPage
from auto_scripts.PageClasses.UserRegistrationAPIPage import UserRegistrationAPIPage

@pytest.mark.tc_scrum96_006
def test_TC_SCRUM96_006_negative_login_api_and_session_validation():
    """
    TC_SCRUM96_006: Negative Login API & Session Validation
    1. Register a user (validuser/CorrectPass123!)
    2. Login with correct username and wrong password (WrongPassword456!)
    3. Assert 401, correct error, and no token/session.
    """
    registration_api = UserRegistrationAPIPage()
    login_api = LoginPage()
    
    # Step 1: Register user
    registration_response = registration_api.register_user_api(
        username="validuser",
        email="validuser@example.com",
        password="CorrectPass123!",
        first_name="Valid",
        last_name="User"
    )
    assert registration_response.status_code == 201, "User registration failed"

    # Step 2: Attempt login with wrong password
    login_response = login_api.api_auth_login(
        username="validuser",
        password="WrongPassword456!"
    )

    # Step 3: Assert 401 Unauthorized and error message
    login_api.verify_auth_failure(
        response=login_response,
        expected_status=401,
        expected_error_message="Invalid username or password"
    )

    # Step 4: Assert no JWT token and no session
    login_api.verify_no_token_and_no_session(login_response)
