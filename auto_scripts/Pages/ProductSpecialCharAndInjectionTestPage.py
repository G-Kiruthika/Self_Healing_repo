import requests
import pymysql
import re
from typing import Dict, Any

class ProductSpecialCharAndInjectionTestPage:
    """
    Executive Summary:
    - Automates TC_SCRUM96_010: Product CRUD and SQL injection validation.
    - Implements: special character insert, API search, SQL injection attempt, DB integrity check, log verification.
    - Strict Python/Selenium automation best practices, atomic methods, robust error handling, and docstring reporting.

    Analysis:
    - Covers all critical paths for product special character and injection scenarios.
    - API, DB, and log checks ensure multi-layer validation and code integrity.
    - Follows structure and conventions of existing PageClasses for maintainability and downstream automation.

    Implementation Guide:
    1. Instantiate ProductSpecialCharAndInjectionTestPage with db_config and log_config.
    2. Call run_tc_scrum96_010(product_data, injection_string) for end-to-end test.
    3. Validate returned dict for stepwise results: insert, search, injection, DB integrity, log detection.
    4. Use atomic methods for granular checks if needed.

    Example:
        db_config = {"host": "localhost", "user": "dbuser", "password": "dbpass", "database": "ecommercedb"}
        log_config = {"log_file_path": "/var/log/app/application.log"}
        page = ProductSpecialCharAndInjectionTestPage(db_config, log_config)
        product_data = {"name": "Test@Product!", "description": "Special chars: <script>'\"%$#@!", "price": 99.99}
        injection_string = "1; DROP TABLE products; --"
        results = page.run_tc_scrum96_010(product_data, injection_string)
        assert results["step_1_insert_pass"]
        assert results["step_2_api_search_pass"]
        assert results["step_3_injection_response_pass"]
        assert results["step_4_db_integrity_pass"]
        assert results["step_5_log_detection_pass"]

    QA Report:
    - All imports validated (requests, pymysql, re, typing).
    - Exception handling ensures atomic failure reporting.
    - Output structure matches project and downstream requirements.
    - Peer review and static analysis recommended before deployment.

    Troubleshooting:
    - If DB fails: check credentials, connection, and product table structure.
    - If API fails: validate endpoint, payload, and backend logic.
    - If logs not found: validate log path and application logging.
    - Increase timeouts for slow environments.

    Future Considerations:
    - Parameterize endpoints, DB, and log paths for multi-environment support.
    - Extend for multi-locale error validation and log parsing.
    - Integrate with CI/CD for full E2E coverage.
    - Add retry logic and audit reporting.
    """

    PRODUCT_API_URL = "https://example-ecommerce.com/api/products"
    PRODUCT_SEARCH_API_URL = "https://example-ecommerce.com/api/products/search"

    def __init__(self, db_config: Dict[str, Any], log_config: Dict[str, Any]):
        """
        Args:
            db_config (dict): Database config with keys host, user, password, database
            log_config (dict): Log config with key log_file_path
        """
        self.db_config = db_config
        self.log_file_path = log_config.get("log_file_path")

    def insert_product_with_special_chars(self, product_data: Dict[str, Any]) -> requests.Response:
        """
        Inserts a product with special characters via POST API.
        Args:
            product_data (dict): {"name": str, "description": str, "price": float}
        Returns:
            requests.Response: API response
        """
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.PRODUCT_API_URL, json=product_data, headers=headers, timeout=10)
        return response

    def search_product_via_api(self, search_query: str) -> requests.Response:
        """
        Searches for product via API using special character query.
        Args:
            search_query (str): Product name or description with special chars
        Returns:
            requests.Response: API response
        """
        params = {"q": search_query}
        response = requests.get(self.PRODUCT_SEARCH_API_URL, params=params, timeout=10)
        return response

    def send_sql_injection_attempt(self, injection_string: str) -> requests.Response:
        """
        Sends SQL injection attempt via API search.
        Args:
            injection_string (str): SQL injection payload
        Returns:
            requests.Response: API response
        """
        params = {"q": injection_string}
        response = requests.get(self.PRODUCT_SEARCH_API_URL, params=params, timeout=10)
        return response

    def verify_db_integrity_for_products(self) -> bool:
        """
        Verifies integrity of products table in DB (no dropped/altered table, special char records intact).
        Returns:
            bool: True if integrity passes, else raises AssertionError
        """
        connection = pymysql.connect(
            host=self.db_config["host"],
            user=self.db_config["user"],
            password=self.db_config["password"],
            database=self.db_config["database"],
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE 'products'")
                table_exists = cursor.fetchone()
                assert table_exists, "Products table does not exist (possible injection damage)."
                cursor.execute("SELECT * FROM products WHERE name LIKE '%@%' OR description LIKE '%<script>%' LIMIT 1")
                record = cursor.fetchone()
                assert record, "Product with special characters not found in DB."
        finally:
            connection.close()
        return True

    def check_application_logs_for_injection_detection(self, injection_string: str) -> bool:
        """
        Checks application logs for SQL injection detection and logging.
        Args:
            injection_string (str): SQL injection payload
        Returns:
            bool: True if detection/logging found, else raises AssertionError
        """
        try:
            with open(self.log_file_path, "r", encoding="utf-8") as log_file:
                logs = log_file.read()
                detected = re.search(r"SQL injection detected.*" + re.escape(injection_string), logs, re.IGNORECASE)
                assert detected, f"SQL injection not detected/logged for payload: {injection_string}"
        except Exception as e:
            raise AssertionError(f"Error reading logs: {str(e)}")
        return True

    def run_tc_scrum96_010(self, product_data: Dict[str, Any], injection_string: str) -> Dict[str, Any]:
        """
        End-to-end execution for TC_SCRUM96_010.
        Args:
            product_data (dict): Product info with special chars
            injection_string (str): SQL injection payload
        Returns:
            dict: Stepwise results and validation messages
        """
        results = {}
        # Step 1: Insert product with special chars
        try:
            resp_insert = self.insert_product_with_special_chars(product_data)
            results["step_1_insert_status_code"] = resp_insert.status_code
            results["step_1_insert_response_body"] = resp_insert.json() if resp_insert.content else {}
            results["step_1_insert_pass"] = resp_insert.status_code in [200, 201]
        except Exception as e:
            results["step_1_insert_pass"] = False
            results["step_1_insert_error"] = str(e)
        # Step 2: Search product via API
        try:
            resp_search = self.search_product_via_api(product_data["name"])
            results["step_2_api_search_status_code"] = resp_search.status_code
            results["step_2_api_search_response_body"] = resp_search.json() if resp_search.content else {}
            results["step_2_api_search_pass"] = resp_search.status_code == 200 and any(product_data["name"] in p.get("name", "") for p in resp_search.json())
        except Exception as e:
            results["step_2_api_search_pass"] = False
            results["step_2_api_search_error"] = str(e)
        # Step 3: SQL injection attempt
        try:
            resp_injection = self.send_sql_injection_attempt(injection_string)
            results["step_3_injection_response_status_code"] = resp_injection.status_code
            results["step_3_injection_response_body"] = resp_injection.json() if resp_injection.content else {}
            # Expect API to block/handle injection, e.g., return 400/422 or safe error
            results["step_3_injection_response_pass"] = resp_injection.status_code in [400, 422, 200] and not resp_injection.json().get("error", "").lower().startswith("internal server error")
        except Exception as e:
            results["step_3_injection_response_pass"] = False
            results["step_3_injection_response_error"] = str(e)
        # Step 4: DB integrity check
        try:
            results["step_4_db_integrity_pass"] = self.verify_db_integrity_for_products()
        except Exception as e:
            results["step_4_db_integrity_pass"] = False
            results["step_4_db_integrity_error"] = str(e)
        # Step 5: Log check for injection detection
        try:
            results["step_5_log_detection_pass"] = self.check_application_logs_for_injection_detection(injection_string)
        except Exception as e:
            results["step_5_log_detection_pass"] = False
            results["step_5_log_detection_error"] = str(e)
        results["overall_pass"] = all([
            results.get("step_1_insert_pass"),
            results.get("step_2_api_search_pass"),
            results.get("step_3_injection_response_pass"),
            results.get("step_4_db_integrity_pass"),
            results.get("step_5_log_detection_pass")
        ])
        return results
