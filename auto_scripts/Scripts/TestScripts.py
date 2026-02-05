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
    base_url = "http://localhost:8000"  # Replace with actual API base URL
    db_config = {
        "host": "localhost",
        "port": 5432,
        "dbname": "yourdb",
        "user": "youruser",
        "password": "yourpass"
    }
    user_data = {
        "username": "profileuser",
        "email": "profileuser@example.com",
        "password": "Profile123!",
        "firstName": "Profile",
        "lastName": "User"
    }
    # Step 1: Register user and login to get JWT token
    api_auth = ApiAuthPage(base_url)
    reg_response = api_auth.register_user(
        user_data["username"],
        user_data["email"],
        user_data["password"],
        user_data["firstName"],
        user_data["lastName"]
    )
    login_response = api_auth.login_user(user_data["username"], user_data["password"])
    jwt_token = api_auth.get_jwt_token(login_response)
    assert jwt_token is not None, "JWT token not found in login response"

    # Step 2: Fetch user profile via API
    api_profile_page = ApiProfilePage(base_url)
    profile_response = api_profile_page.get_user_profile(jwt_token)
    # Validate profile schema and absence of password
    assert api_profile_page.validate_profile_response(profile_response)

    # Step 3: Fetch user from DB and compare
    db_user_page = DbUserPage(db_config)
    db_user = db_user_page.get_user_from_db(user_data["username"])
    assert db_user is not None, "User not found in DB"
    assert db_user_page.compare_profile_to_db(profile_response, db_user)

# TC_SCRUM96_005: Negative Login Audit Log Test
from auto_scripts.Pages.LoginPage import LoginPage
import datetime

def test_TC_SCRUM_96_005_negative_login_audit_log():
    ...
# TC_SCRUM96_008: Product Search API Case-Insensitive Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
import requests
import pymysql

def test_TC_SCRUM_96_008_product_search_case_insensitive():
    """
    Test Case TC_SCRUM96_008: Product Search API Case-Insensitive Test
    Steps:
    1. Insert three products into DB: 'Laptop Computer', 'Gaming Laptop', 'Desktop Computer'
    2. Send GET requests to /api/products/search?query=laptop, LAPTOP, LaPtOp
    3. Validate HTTP 200 and that both 'Laptop Computer' and 'Gaming Laptop' are returned for all queries
    """
    db_config = {
        "host": "localhost",
        "user": "testuser",
        "password": "testpass",
        "database": "testdb"
    }
    session = requests.Session()
    product_page = ProductSearchAPIPage(session=session, db_config=db_config)
    products = [
        {"productId": 101, "name": "Laptop Computer", "description": "High performance laptop", "price": 999.99, "availability": "In stock"},
        {"productId": 102, "name": "Gaming Laptop", "description": "Gaming laptop with RTX", "price": 1499.99, "availability": "In stock"},
        {"productId": 103, "name": "Desktop Computer", "description": "Desktop PC", "price": 799.99, "availability": "In stock"}
    ]
    base_search_term = "laptop"
    product_page.tc_scrum96_008_full_workflow(products, base_search_term)
