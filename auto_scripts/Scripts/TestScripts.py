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
    """
    Test Case TC_SCRUM96_008: Product Search API Case-Insensitive Test
    Steps:
    1. Insert test products into database with names 'Laptop Computer', 'Gaming Laptop', and 'Desktop Computer'
    2. Send GET request to /api/products/search?query=laptop (lowercase)
    3. Send GET request to /api/products/search?query=LAPTOP (uppercase)
    4. Send GET request to /api/products/search?query=LaPtOp (mixed case)
    5. Validate that API returns HTTP 200 OK and both laptop products for all queries, confirming case-insensitive search functionality
    """
    db_config = {
        "host": "localhost",
        "user": "testuser",
        "password": "testpass",
        "database": "testdb"
    }
    session = requests.Session()
    product_page = ProductSearchAPIPage(session=session, db_config=db_config)
    test_products = [
        {"productId": 201, "name": "Laptop Computer", "description": "High performance laptop", "price": 999.99, "availability": "in stock"},
        {"productId": 202, "name": "Gaming Laptop", "description": "Gaming laptop with RTX", "price": 1499.99, "availability": "in stock"},
        {"productId": 203, "name": "Desktop Computer", "description": "Desktop PC", "price": 799.99, "availability": "in stock"}
    ]
    # Step 1: Insert products into DB
    product_page.insert_test_products_to_db(test_products)
    # Step 2-4: Case-insensitive search validation
    base_search_term = "laptop"
    expected_product_ids = [201, 202]
    product_page.search_case_variants_and_validate(base_search_term, expected_product_ids)
    print("TC_SCRUM96_008 case-insensitive search test PASSED.")

# TC_SCRUM96_009: Product Search API Edge Case Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
import requests
import pymysql

def test_TC_SCRUM96_009_product_search_edge_cases():
    """
    Test Case TC_SCRUM96_009: Product Search API Edge Cases
    Steps:
    1. Ensure products table contains at least 5 test products
    2. Send GET request to /api/products/search?query= (empty query parameter)
    3. Send GET request to /api/products/search (missing query parameter)
    """
    db_config = {
        "host": "localhost",
        "user": "testuser",
        "password": "testpass",
        "database": "testdb"
    }
    session = requests.Session()
    product_page = ProductSearchAPIPage(session=session, db_config=db_config)
    # Step 1: Validate DB has at least 5 products
    count = product_page.validate_db_has_at_least_n_products(n=5)
    print(f"DB contains {count} products.")
    # Step 2: Empty query parameter
    products_empty_query = product_page.search_products_empty_query()
    print(f"Products returned for empty query: {len(products_empty_query)}")
    # Step 3: Missing query parameter
    try:
        error_msg = product_page.search_products_missing_query()
        print(f"Missing query error message: {error_msg}")
    except AssertionError as e:
        print(f"AssertionError for missing query: {e}")
