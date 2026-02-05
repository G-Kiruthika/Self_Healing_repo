import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import datetime
from JWTUtils import JWTUtils

class LoginPage:
    ...
    # --- TC_SCRUM96_004 additions ---
    def tc_scrum96_004_login_and_validate_tokens(self, username: str, password: str, expected_email: str):
        """
        Implements TC_SCRUM96_004 Step 2: Login and validate JWT, tokens, and user details.
        Args:
            username (str): Username for login
            password (str): Password for login
            expected_email (str): Expected email in response
        Returns:
            dict: {"status_code": int, "jwt_token": str, "refresh_token": str, "token_type": str, "user_details": dict}
        Raises:
            AssertionError: On validation failure
        """
        url = f"{self.base_url}/api/auth/login"
        payload = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        assert response.status_code == 200, f"Login failed: {response.text}"
        resp_json = response.json()
        jwt_token = resp_json.get("accessToken") or resp_json.get("token")
        refresh_token = resp_json.get("refreshToken")
        token_type = resp_json.get("tokenType")
        user_details = {
            "userId": resp_json.get("userId"),
            "username": resp_json.get("username"),
            "email": resp_json.get("email")
        }
        assert jwt_token, "JWT access token missing"
        assert refresh_token, "Refresh token missing"
        assert token_type and token_type.lower() == "bearer", f"Token type should be 'Bearer', got '{token_type}'"
        assert user_details["userId"] and user_details["username"] and user_details["email"], "User details missing in response"
        assert user_details["username"] == username, f"Username mismatch: expected {username}, got {user_details['username']}"
        assert user_details["email"] == expected_email, f"Email mismatch: expected {expected_email}, got {user_details['email']}"
        JWTUtils.validate_jwt(jwt_token, username)
        return {
            "status_code": response.status_code,
            "jwt_token": jwt_token,
            "refresh_token": refresh_token,
            "token_type": token_type,
            "user_details": user_details
        }