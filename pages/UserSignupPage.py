import requests
import re
import pymysql
from typing import Dict, Any

class UserSignupPage:
    """
    Page Object for User Signup API interactions and validations.
    Implements TC-SCRUM-96-003: Invalid email format on signup.
    Strictly follows Selenium Python best practices for structure and reporting.
    """

    SIGNUP_API_URL = "https://example-ecommerce.com/api/users/signup"

    def __init__(self, db_config: Dict[str, Any]):
        """
        db_config: dict with keys host, user, password, database
        """
        self.db_config = db_config

    def send_signup_request(self, username: str, email: str, password: str) -> requests.Response:
        """
        Sends POST request to signup API with provided data.
        Returns the response object.
        """
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.SIGNUP_API_URL, json=payload, headers=headers, timeout=10)
        return response

    def validate_error_response(self, response: requests.Response) -> bool:
        """
        Validates that the response indicates an invalid email format error.
        Returns True if validation passes, else raises AssertionError.
        """
        assert response.status_code == 400, f"Expected HTTP 400, got {response.status_code}"
        data = response.json()
        assert "message" in data, "No error message in response body"
        assert re.search(r"invalid email format", data["message"], re.IGNORECASE), \
            f"Expected 'Invalid email format' message, got: {data['message']}"
        return True

    def verify_no_user_created(self, username: str) -> bool:
        """
        Verifies that no user record exists for the given username in the database.
        Returns True if no record exists, else raises AssertionError.
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
                cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
                result = cursor.fetchone()
                assert result is None, f"User record found for username '{username}' when none expected."
        finally:
            connection.close()
        return True

    def run_tc_scrum_96_003(self, username: str = "testuser", email: str = "invalidemail", password: str = "Pass123!") -> Dict[str, Any]:
        """
        End-to-end execution for TC-SCRUM-96-003.
        Returns a dict with stepwise results and validation messages.
        """
        results = {}
        # Step 1: Send POST request
        response = self.send_signup_request(username, email, password)
        results["step_1_response_code"] = response.status_code
        results["step_1_response_body"] = response.json() if response.content else {}
        # Step 2: Validate error message
        try:
            results["step_2_error_validation"] = self.validate_error_response(response)
        except AssertionError as e:
            results["step_2_error_validation"] = False
            results["step_2_error_message"] = str(e)
        # Step 3: Verify no user record in DB
        try:
            results["step_3_no_user_in_db"] = self.verify_no_user_created(username)
        except AssertionError as e:
            results["step_3_no_user_in_db"] = False
            results["step_3_db_error_message"] = str(e)
        return results

"""
Executive Summary:
- UserSignupPage.py is newly created to automate TC-SCRUM-96-003: invalid email format on signup.
- It provides end-to-end API, error validation, and DB verification in one PageClass for seamless downstream automation.

Detailed Analysis:
- No existing UserSignupPage.py; this class is necessary for API-based signup validation.
- Implements strict error and DB validation, with stepwise reporting.
- All logic is self-contained, using best practices for structure, error handling, and reporting.

Implementation Guide:
1. Instantiate UserSignupPage with DB config dict:
   db_config = {"host": "localhost", "user": "dbuser", "password": "dbpass", "database": "ecommercedb"}
   page = UserSignupPage(db_config)
2. Call run_tc_scrum_96_003() for end-to-end test. Analyze returned dict for stepwise results.
3. Use validate_error_response and verify_no_user_created for granular checks.

Quality Assurance Report:
- All imports validated (requests, pymysql, re, typing).
- Error handling robust; all assertion failures reported in results dict.
- API and DB logic separated for maintainability.
- Peer review and static analysis recommended before deployment.

Troubleshooting Guide:
- If DB connection fails, check db_config and DB availability.
- If API returns unexpected code, validate endpoint and test data.
- If error message not found, check API contract and error handling.
- Increase timeouts for slow environments.

Future Considerations:
- Parameterize API URL and DB config for multi-environment support.
- Extend for multi-locale error message validation.
- Integrate with test reporting and CI/CD pipeline for full E2E coverage.
- Add retry logic for flaky API/DB responses.
"""
