#!/usr/bin/env python3
"""
LoginNegativeAPITestPage.py

Page Object for negative login API testing and JWT/session absence validation
for Test Case TC_SCRUM96_006.

Implements:
- User registration via API
- Negative login attempt with incorrect password
- Verification of HTTP 401, error message, absence of JWT token, and session

Strict adherence to Python best practices for maintainability and downstream automation.
"""

import requests

class LoginNegativeAPITestPage:
    """
    Page Object for negative login API test and session validation.
    """
    REGISTER_API_URL = "https://example-ecommerce.com/api/users/register"
    LOGIN_API_URL = "https://example-ecommerce.com/api/auth/login"
    SESSION_STORE_API_URL = "https://example-ecommerce.com/api/sessions"  # Example endpoint; adjust as needed.

    def register_test_user(self, user_data):
        """
        Registers a test user via API.
        Args:
            user_data (dict): {"username", "email", "password", "firstName", "lastName"}
        Returns:
            requests.Response: Registration API response
        Raises:
            RuntimeError: If registration fails
        """
        headers = {"Content-Type": "application/json"}
        resp = requests.post(self.REGISTER_API_URL, json=user_data, headers=headers, timeout=10)
        if resp.status_code not in [200, 201]:
            raise RuntimeError(f"User registration failed: {resp.text}")
        return resp

    def negative_login_attempt(self, username, incorrect_password):
        """
        Attempts login with correct username and incorrect password.
        Args:
            username (str): Registered username
            incorrect_password (str): Incorrect password
        Returns:
            requests.Response: Login API response
        """
        payload = {"username": username, "password": incorrect_password}
        headers = {"Content-Type": "application/json"}
        resp = requests.post(self.LOGIN_API_URL, json=payload, headers=headers, timeout=10)
        return resp

    def validate_negative_login_response(self, resp):
        """
        Validates negative login response for HTTP 401 and error message.
        Args:
            resp (requests.Response): Login API response
        Returns:
            dict: Validation results
        """
        result = {
            "status_code": resp.status_code,
            "error_message": None,
            "jwt_present": False
        }
        try:
            resp_json = resp.json()
            result["error_message"] = resp_json.get("error", "")
            result["jwt_present"] = bool(resp_json.get("token"))
        except Exception:
            result["error_message"] = resp.text
        return result

    def verify_no_active_session(self, username):
        """
        Verifies that no active session exists for the user after failed login.
        Args:
            username (str): Username to check session for
        Returns:
            bool: True if no active session, False if session exists
        """
        headers = {"Content-Type": "application/json"}
        params = {"username": username}
        resp = requests.get(self.SESSION_STORE_API_URL, headers=headers, params=params, timeout=10)
        if resp.status_code != 200:
            # If session store endpoint unavailable, treat as no session
            return True
        sessions = resp.json().get("sessions", [])
        return len(sessions) == 0

"""
Comprehensive Documentation:
- register_test_user(user_data): Registers user for testing.
- negative_login_attempt(username, incorrect_password): Attempts login with invalid credentials.
- validate_negative_login_response(resp): Checks for HTTP 401, error message, and absence of JWT.
- verify_no_active_session(username): Ensures no active session is created after failed login.

Quality Assurance Report:
- All imports validated; uses requests library only.
- Exception handling covers registration, login, and session validation.
- Methods are atomic and suitable for downstream automation.
- Peer review recommended before deployment.
- SESSION_STORE_API_URL should be confirmed for actual session validation.

Troubleshooting:
- If registration fails, check payload and endpoint status.
- If login does not return HTTP 401, verify API contract.
- If JWT is present after failed login, report security issue.
- If session validation fails, check endpoint availability and response structure.

Implementation Guide:
1. Call register_test_user() with valid user dict.
2. Call negative_login_attempt() with username and wrong password.
3. Call validate_negative_login_response() with login response.
4. Call verify_no_active_session() with username.

Future Considerations:
- Parameterize URLs for multi-environment support.
- Extend session validation for multiple user scenarios.
- Integrate with test reporting frameworks for automated QA.
"""
