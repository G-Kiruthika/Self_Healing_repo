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
    page = ProductSearchAPIPage()
    queries = ["laptop", "LAPTOP", "LaPtOp"]
    expected_products = ["Laptop Computer", "Gaming Laptop"]
    # Step 1: Insert test products into the database (assumed DB setup is handled externally)
    # Step 2-4: Validate API returns expected products for all query cases
    page.validate_case_insensitive_search(queries, expected_products)
    # Optionally, print QA report
    report = page.report_case_insensitive_search(queries, expected_products)
    for query, result in report.items():
        print(f"Query: {query} => {result}")
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

# TC-SCRUM96_007: End-to-End Profile API Validation Test (NEW)
from auto_scripts.Pages.ProfileAPIValidationPage import ProfileAPIValidationPage
from auto_scripts.Pages.JWTUtils import JWTUtils
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage
import pytest

class DummyDBClient:
    def get_user_by_username(self, username):
        return {
            "userId": 123,
            "username": "profileuser",
            "email": "profileuser@example.com",
            "firstName": "Profile",
            "lastName": "User",
            "registrationDate": "2024-06-01T12:00:00Z",
            "accountStatus": "active"
        }

@pytest.mark.tc_scrum96_007
def test_TC_SCRUM96_007_profile_api_and_db_validation():
    jwt_utils = JWTUtils()
    registration_api = UserRegistrationAPIPage()
    db_client = DummyDBClient()
    profile_api_page = ProfileAPIValidationPage(jwt_utils, registration_api, db_client)

    user_data = {
        "username": "profileuser",
        "email": "profileuser@example.com",
        "password": "Profile123!",
        "firstName": "Profile",
        "lastName": "User"
    }

    jwt_token = profile_api_page.register_and_login_user(user_data)
    profile_data = profile_api_page.get_profile_with_jwt(jwt_token)
    expected_data = db_client.get_user_by_username(user_data["username"])
    profile_api_page.validate_profile_fields(profile_data, expected_data)
