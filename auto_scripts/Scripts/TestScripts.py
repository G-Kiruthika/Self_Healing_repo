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
    """
    Test Case TC-SCRUM-96-010: Cart API End-to-End Test
    Steps:
    1. Sign in as a user with no existing cart
    2. Add a product to the cart via API (lazy cart creation)
    3. Validate cart and item in the database
    4. Retrieve cart details and assert correctness
    """
    # Test Data
    email = "newcartuser@example.com"
    password = "Pass123!"
    product_id = "PROD-001"
    quantity = 2
    db_config = {
        "host": "localhost",
        "user": "dbuser",
        "password": "dbpass",
        "database": "ecommerce_db"
    }
    logger = logging.getLogger("TC_SCRUM_96_010")
    cart_page = CartAPIPage(db_config=db_config, logger=logger)
    # Step 1: Sign in
    cart_page.sign_in_user(email, password)
    # Step 2: Add product to cart
    cart_page.add_product_to_cart(product_id, quantity)
    # Step 3: Validate cart in DB
    cart_page.verify_cart_in_database()
    # Step 4: Retrieve and assert cart details
    cart_details = cart_page.get_cart_details()
    items = cart_details["items"]
    assert any(item["productId"] == product_id and item["quantity"] == quantity for item in items), \
        f"Product {product_id} with quantity {quantity} not found in cart details"
    print("TC-SCRUM-96-010 Cart API end-to-end test PASSED.")

# TC-SCRUM96_002: User Registration, Duplicate Registration, and DB Verification Test
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage
import pytest

def test_TC_SCRUM96_002_user_registration_duplicate_and_db_verification():
    """
    Test Case TC_SCRUM96_002:
    1. Register a user with username 'duplicateuser' and email 'first@example.com'.
    2. Attempt to register another user with the same username but different email 'second@example.com'.
    3. Verify only one user record exists in the database for username 'duplicateuser' and email 'first@example.com'.
    """
    user_registration_page = UserRegistrationAPIPage()
    # Step 1: Register user
    user_data_first = {
        "username": "duplicateuser",
        "email": "first@example.com",
        "password": "Pass123!",
        "firstName": "First",
        "lastName": "User"
    }
    jwt_token = user_registration_page.register_user_and_get_jwt(user_data_first)
    assert jwt_token is not None, "JWT token should be returned for successful registration"

    # Step 2: Attempt duplicate registration
    user_data_second = {
        "username": "duplicateuser",
        "email": "second@example.com",
        "password": "Pass456!",
        "firstName": "Second",
        "lastName": "User"
    }
    duplicate_result = user_registration_page.attempt_duplicate_registration(user_data_second)
    assert duplicate_result["status_code"] == 409, "API should return HTTP 409 Conflict for duplicate username"
    assert "username" in duplicate_result["error_message"].lower(), "Error message should indicate username conflict"

    # Step 3: Verify single user in DB
    db_check = user_registration_page.verify_single_user_in_db("duplicateuser", "first@example.com")
    assert db_check is True, "Only one user record should exist in DB with expected email"
    print("TC_SCRUM96_002 user registration, duplicate, and DB verification PASSED.")
