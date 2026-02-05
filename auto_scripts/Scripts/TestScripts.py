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

# TC_SCRUM96_002: Duplicate Username Registration and Conflict Validation Test
import pytest
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage

def test_TC_SCRUM96_002_duplicate_username_registration_conflict():
    """
    TC_SCRUM96_002: Duplicate Username Registration and Conflict Validation Test
    Steps:
    1. Register a user with username 'duplicateuser' and email 'first@example.com'
    2. Attempt duplicate registration with same username but email 'second@example.com'
    3. Validate HTTP 201 for first, HTTP 409 for duplicate, and error message
    4. Confirm only one DB record for username with first email
    """
    username = "duplicateuser"
    first_email = "first@example.com"
    first_password = "Pass123!"
    first_first_name = "First"
    first_last_name = "User"
    second_email = "second@example.com"
    second_password = "Pass456!"
    second_first_name = "Second"
    second_last_name = "User"

    registration_api = UserRegistrationAPIPage()

    result = registration_api.register_duplicate_user_and_validate_conflict(
        username,
        first_email,
        first_password,
        first_first_name,
        first_last_name,
        second_email,
        second_password,
        second_first_name,
        second_last_name
    )

    assert result["first_registration_status"] == 201, f"Expected HTTP 201 Created for first user, got {result['first_registration_status']}"
    assert result["duplicate_registration_status"] == 409, f"Expected HTTP 409 Conflict for duplicate username, got {result['duplicate_registration_status']}"
    assert "already exists" in result["duplicate_error_message"].lower(), f"Expected error message indicating username already exists, got: {result['duplicate_error_message']}"
    assert result["db_user_count"] == 1, f"Expected only one record for username 'duplicateuser', found {result['db_user_count']}"
    assert result["db_email"] == first_email, f"Expected email '{first_email}' for username 'duplicateuser', got '{result['db_email']}"