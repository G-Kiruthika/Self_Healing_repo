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
from auto_scripts.Pages.ProductSpecialCharAndInjectionTestPage import ProductSpecialCharAndInjectionTestPage
import requests
import pymysql
import os
import datetime

def test_TC_SCRUM96_010_product_search_special_char_sql_injection_db_log():
    db_config = {"host": "localhost", "user": "dbuser", "password": "dbpass", "database": "ecommercedb"}
    log_config = {"log_file_path": "/var/log/app/application.log"}
    page = ProductSpecialCharAndInjectionTestPage(db_config, log_config)
    product_data = {"name": "C++ Programming Book", "description": "Learn C++ programming", "price": 49.99}
    injection_string = "' OR '1'='1"
    results = page.run_tc_scrum96_010(product_data, injection_string)
    assert results["step_1_insert_pass"], f"Step 1 failed: {results.get('step_1_insert_error', '')}"
    assert results["step_2_api_search_pass"], f"Step 2 failed: {results.get('step_2_api_search_error', '')}"
    assert results["step_3_injection_response_pass"], f"Step 3 failed: {results.get('step_3_injection_response_error', '')}"
    assert results["step_4_db_integrity_pass"], f"Step 4 failed: {results.get('step_4_db_integrity_error', '')}"
    assert results["step_5_log_detection_pass"], f"Step 5 failed: {results.get('step_5_log_detection_error', '')}"
    print("TC_SCRUM96_010 results:", results)

# TC-SCRUM96_010: Product CRUD and SQL Injection Validation Test (Appended for compliance)
def test_TC_SCRUM96_010_product_crud_and_sql_injection_validation():
    db_config = {"host": "localhost", "user": "dbuser", "password": "dbpass", "database": "ecommercedb"}
    log_config = {"log_file_path": "/var/log/app/application.log"}
    page = ProductSpecialCharAndInjectionTestPage(db_config, log_config)
    product_data = {"name": "C++ Programming Book", "description": "Learn C++ programming", "price": 49.99}
    injection_string = "' OR '1'='1"

    # Step 1: Insert product with special chars
    try:
        resp_insert = page.insert_product_with_special_chars(product_data)
        assert resp_insert.status_code in [200, 201], f"Step 1 failed: Unexpected status code {resp_insert.status_code}"
    except Exception as e:
        raise AssertionError(f"Step 1 failed: {str(e)}")

    # Step 2: Search product via API
    try:
        resp_search = page.search_product_via_api(product_data["name"])
        search_results = resp_search.json() if resp_search.content else {}
        assert resp_search.status_code == 200 and any(product_data["name"] in p.get("name", "") for p in search_results), f"Step 2 failed: Product not found in API search"
    except Exception as e:
        raise AssertionError(f"Step 2 failed: {str(e)}")

    # Step 3: SQL injection attempt
    try:
        resp_injection = page.send_sql_injection_attempt(injection_string)
        injection_results = resp_injection.json() if resp_injection.content else {}
        assert resp_injection.status_code in [400, 422, 200] and not injection_results.get("error", "").lower().startswith("internal server error"), f"Step 3 failed: SQL injection vulnerability detected"
    except Exception as e:
        raise AssertionError(f"Step 3 failed: {str(e)}")

    # Step 4: DB integrity check
    try:
        assert page.verify_db_integrity_for_products(), "Step 4 failed: DB integrity compromised"
    except Exception as e:
        raise AssertionError(f"Step 4 failed: {str(e)}")

    # Step 5: Log check for injection detection
    try:
        assert page.check_application_logs_for_injection_detection(injection_string), "Step 5 failed: SQL injection not detected/logged"
    except Exception as e:
        raise AssertionError(f"Step 5 failed: {str(e)}")

    print("TC_SCRUM96_010 Product CRUD and SQL Injection Validation Test completed successfully.")
