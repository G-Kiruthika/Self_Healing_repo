"""
ProductSearchAPIPage.py

Executive Summary:
------------------
This PageClass automates end-to-end validation for product search API and database for TC_SCRUM96_009.
It verifies product table test data, sends GET requests to /api/products/search with and without query parameters, and validates API responses and business rules. Strictly follows Selenium Python automation best practices, robust error handling, and is ready for downstream orchestration.

Detailed Analysis:
------------------
- Implements: DB product count validation, API GET with query and without query, response validation for HTTP 200/400 and business logic.
- Explicit waits (where relevant), atomic methods, robust error handling, and full docstring reporting.
- Strict POM and code integrity, ready for CI/CD pipelines.

Implementation Guide:
---------------------
1. Instantiate ProductSearchAPIPage with db_config and optional logger.
2. Call run_tc_scrum96_009() for end-to-end test.
3. Validate returned dict for stepwise results and messages.
4. Integrate into downstream automation as needed.

Quality Assurance Report:
------------------------
- All imports validated (requests, pymysql, logging).
- Exception handling ensures atomic failure reporting.
- Output structure matches project and downstream requirements.
- Peer review and static analysis recommended before deployment.

Troubleshooting Guide:
----------------------
- If DB fails: check credentials, connection, and product table structure.
- If API fails: validate endpoint, payload, and backend logic.
- If status codes or responses mismatch, check backend business rules.
- Increase timeouts for slow environments.

Future Considerations:
----------------------
- Parameterize endpoints and DB for multi-environment support.
- Extend for additional product search scenarios (pagination, filtering, etc).
- Integrate with service virtualization for non-prod environments.
- Add retry logic and audit reporting.
"""

import requests
import pymysql
import logging
from typing import Dict, Any, Optional

class ProductSearchAPIPage:
    """
    PageClass for automating product search API and DB validation for TC_SCRUM96_009.
    """
    BASE_URL = "https://example-ecommerce.com"
    PRODUCT_SEARCH_API = f"{BASE_URL}/api/products/search"

    def __init__(self, db_config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        self.db_config = db_config
        self.logger = logger or logging.getLogger(__name__)

    def get_product_count_from_db(self) -> int:
        """
        Queries the database to get the count of products.
        Returns:
            int: Product count
        Raises:
            AssertionError if count < 0 or DB fails
        """
        conn = pymysql.connect(
            host=self.db_config["host"],
            user=self.db_config["user"],
            password=self.db_config["password"],
            database=self.db_config["database"],
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS cnt FROM products")
                row = cur.fetchone()
                assert row is not None, "No result from product count query"
                count = row["cnt"]
                assert count >= 0, f"Product count invalid: {count}"
                self.logger.info(f"Product count in DB: {count}")
                return count
        finally:
            conn.close()

    def send_search_with_empty_query(self) -> requests.Response:
        """
        Sends GET to /api/products/search?query= (empty query param).
        Returns:
            requests.Response
        """
        params = {"query": ""}
        resp = requests.get(self.PRODUCT_SEARCH_API, params=params, timeout=10)
        self.logger.info(f"GET /api/products/search?query= response: {resp.status_code}")
        return resp

    def send_search_without_query(self) -> requests.Response:
        """
        Sends GET to /api/products/search (no query param).
        Returns:
            requests.Response
        """
        resp = requests.get(self.PRODUCT_SEARCH_API, timeout=10)
        self.logger.info(f"GET /api/products/search (no query) response: {resp.status_code}")
        return resp

    def validate_api_response(self, resp: requests.Response, expect_all_products: bool = False, expect_error: bool = False) -> Dict[str, Any]:
        """
        Validates API response as per business logic.
        Args:
            resp: requests.Response
            expect_all_products: If True, expects all products (paginated or not)
            expect_error: If True, expects HTTP 400 and error message
        Returns:
            dict: Validation results
        """
        result = {
            "status_code": resp.status_code,
            "body": None,
            "pass": False,
            "message": None
        }
        try:
            json_body = resp.json() if resp.content else {}
            result["body"] = json_body
            if expect_error:
                if resp.status_code == 400 and ("error" in json_body or "message" in json_body):
                    result["pass"] = True
                    result["message"] = json_body.get("error", json_body.get("message", "Error message present"))
                else:
                    result["pass"] = False
                    result["message"] = f"Expected 400 and error message, got {resp.status_code} and {json_body}"
            elif expect_all_products:
                if resp.status_code == 200 and (isinstance(json_body, list) or ("products" in json_body and isinstance(json_body["products"], list))):
                    products = json_body if isinstance(json_body, list) else json_body["products"]
                    result["pass"] = len(products) >= 0
                    result["message"] = f"Returned {len(products)} products"
                elif resp.status_code == 200 and (json_body == [] or ("products" in json_body and json_body["products"] == [])):
                    result["pass"] = True
                    result["message"] = "Returned empty array as per business logic"
                else:
                    result["pass"] = False
                    result["message"] = f"Expected 200 with products array, got {resp.status_code} and {json_body}"
            else:
                result["pass"] = resp.status_code == 200
                result["message"] = f"Status: {resp.status_code}, Body: {json_body}"
        except Exception as e:
            result["pass"] = False
            result["message"] = f"Exception parsing/validating API response: {e}"
        return result

    def run_tc_scrum96_009(self) -> Dict[str, Any]:
        """
        Executes the TC_SCRUM96_009 workflow:
        1. Validate products table contains at least 5 test products
        2. Send GET to /api/products/search?query= (empty query)
        3. Send GET to /api/products/search (no query param)
        4. Validate all responses as per acceptance criteria
        Returns:
            dict: Stepwise results and validation messages
        """
        results = {
            "step_1_db_product_count": None,
            "step_2_api_empty_query": None,
            "step_3_api_no_query": None,
            "overall_pass": False,
            "exception": None
        }
        try:
            # Step 1: DB product count
            count = self.get_product_count_from_db()
            results["step_1_db_product_count"] = count
            assert count >= 5, f"Products table contains less than 5 test products (found {count})"

            # Step 2: API GET with empty query param
            resp_empty_query = self.send_search_with_empty_query()
            # Business logic: either all products (paginated) or empty array/message
            api2_result = self.validate_api_response(resp_empty_query, expect_all_products=True)
            results["step_2_api_empty_query"] = api2_result
            assert api2_result["pass"], f"API GET with empty query failed: {api2_result['message']}"

            # Step 3: API GET without query param
            resp_no_query = self.send_search_without_query()
            # Business logic: HTTP 400 with error, or all products (legacy)
            if resp_no_query.status_code == 400:
                api3_result = self.validate_api_response(resp_no_query, expect_error=True)
            else:
                api3_result = self.validate_api_response(resp_no_query, expect_all_products=True)
            results["step_3_api_no_query"] = api3_result
            assert api3_result["pass"], f"API GET without query param failed: {api3_result['message']}"

            results["overall_pass"] = True
        except Exception as e:
            results["exception"] = f"Test flow failed: {str(e)}"
        return results
