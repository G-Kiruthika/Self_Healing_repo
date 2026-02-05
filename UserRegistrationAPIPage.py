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

"""
Executive Summary:
- Implements register_user_and_get_jwt for TC_SCRUM96_007.
- Strict error handling and JWT extraction for downstream automation.

Analysis:
- Enables atomic registration and login for test users.

Implementation Guide:
1. Call register_user_and_get_jwt(user_data) with valid user dict.
2. Use returned JWT for profile and API validation.

QA Report:
- Imports validated; exception handling robust.
- Peer review recommended before deployment.

Troubleshooting:
- If registration/login fails, check API payload and endpoint status.
- If JWT missing, validate login response structure.

Future Considerations:
- Parameterize URLs for multi-environment support.
- Extend with additional user attributes and error reporting.
"""
