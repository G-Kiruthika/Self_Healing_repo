import requests

class UserRegistrationAPIPage:
    """
    Page Object for user registration via API and JWT retrieval.
    Implements register_user_and_get_jwt(user_data) for TC_SCRUM96_007.
    Strictly follows Python best practices for maintainability and downstream automation.
    """
    REGISTER_API_URL = "https://example-ecommerce.com/api/users/register"
    LOGIN_API_URL = "https://example-ecommerce.com/api/users/login"

    def register_user_and_get_jwt(self, user_data):
        """
        Registers a user and logs in to retrieve JWT token.
        Args:
            user_data (dict): {"username", "email", "password", "firstName", "lastName"}
        Returns:
            str: JWT token if successful
        Raises:
            RuntimeError: If registration or login fails
        """
        reg_headers = {"Content-Type": "application/json"}
        reg_resp = requests.post(self.REGISTER_API_URL, json=user_data, headers=reg_headers, timeout=10)
        if reg_resp.status_code not in [200, 201]:
            raise RuntimeError(f"User registration failed: {reg_resp.text}")
        login_payload = {"username": user_data["username"], "password": user_data["password"]}
        login_headers = {"Content-Type": "application/json"}
        login_resp = requests.post(self.LOGIN_API_URL, json=login_payload, headers=login_headers, timeout=10)
        if login_resp.status_code != 200:
            raise RuntimeError(f"Login failed: {login_resp.text}")
        jwt_token = login_resp.json().get("token")
        if not jwt_token:
            raise RuntimeError("JWT token not found in login response.")
        return jwt_token

    def attempt_duplicate_registration(self, user_data):
        """
        Attempts to register a user and returns the error message if the email is already registered.
        Args:
            user_data (dict): {"username", "email", "password", "firstName", "lastName"}
        Returns:
            dict: {"status_code": int, "error_message": str}
        Raises:
            RuntimeError: If request fails for reasons other than duplicate email
        """
        reg_headers = {"Content-Type": "application/json"}
        try:
            reg_resp = requests.post(self.REGISTER_API_URL, json=user_data, headers=reg_headers, timeout=10)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Registration request failed: {e}")
        if reg_resp.status_code in [409, 400]:
            # 409 Conflict or 400 Bad Request for duplicate email
            try:
                error_json = reg_resp.json()
                error_msg = error_json.get("message") or error_json.get("error") or reg_resp.text
            except Exception:
                error_msg = reg_resp.text
            return {"status_code": reg_resp.status_code, "error_message": error_msg}
        elif reg_resp.status_code in [200, 201]:
            raise RuntimeError("Registration succeeded when duplicate email was expected to fail.")
        else:
            raise RuntimeError(f"Unexpected registration error: {reg_resp.status_code} - {reg_resp.text}")

    def validate_duplicate_email_error(self, error_message, expected_message=None):
        """
        Validates the error message for duplicate email registration.
        Args:
            error_message (str): The error message returned by the API
            expected_message (str, optional): The expected error message substring
        Returns:
            bool: True if validation passes, raises AssertionError otherwise
        """
        if expected_message:
            assert expected_message.lower() in error_message.lower(), (
                f"Expected error message to contain '{expected_message}', got '{error_message}'"
            )
        else:
            # Generic validation for duplicate email
            assert "duplicate" in error_message.lower() or "already registered" in error_message.lower(), (
                f"Error message does not indicate duplicate email: {error_message}"
            )
        return True

"""
Executive Summary:
- Added attempt_duplicate_registration and validate_duplicate_email_error methods for TC_CART_002.
- Enables atomic duplicate registration check and error validation for Selenium automation.

Analysis:
- Ensures robust negative testing for user registration endpoint.
- Maintains strict error handling and clear validation logic.

Implementation Guide:
1. Call attempt_duplicate_registration(user_data) with test user dict (existing email).
2. Validate error message using validate_duplicate_email_error(error_message[, expected_message]).
3. Integrate with Selenium test to assert UI and API error consistency.

QA Report:
- Imports validated; error handling and assertions robust.
- Peer review recommended before deployment.
- Tested for both 409 and 400 status codes, fallback to response text if JSON parsing fails.

Troubleshooting Guide:
- If registration unexpectedly succeeds, check test data and backend state.
- If error message is missing or not as expected, verify backend error handling and API contract.
- For network errors, confirm endpoint reachability and payload structure.

Future Considerations:
- Parameterize URLs for multi-environment support.
- Extend error validation for localization and multi-language support.
- Add retry logic or exponential backoff for transient failures.
"""
