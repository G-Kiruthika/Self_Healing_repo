import requests
import re

class UserRegistrationAPIPage:
    REGISTER_API_URL = "https://example-ecommerce.com/api/users/register"
    LOGIN_API_URL = "https://example-ecommerce.com/api/auth/login"
    DB_SIMULATION = {}
    DB_EMAIL_SIM = {}
    ...
    # --- TC_SCRUM96_004 additions ---
    def tc_scrum96_004_register_user_and_get_jwt(self, user_data):
        """
        Implements TC_SCRUM96_004 Step 1: Register user and return JWT token.
        Args:
            user_data (dict): {"username", "email", "password", "firstName", "lastName"}
        Returns:
            dict: {"status_code": int, "response": dict, "jwt_token": str}
        Raises:
            AssertionError: On registration failure
        """
        self._validate_user_data(user_data)
        reg_headers = {"Content-Type": "application/json"}
        reg_resp = requests.post(self.REGISTER_API_URL, json=user_data, headers=reg_headers, timeout=10)
        assert reg_resp.status_code in [200, 201], f"User registration failed: {reg_resp.text}"
        response_json = reg_resp.json() if reg_resp.content else {}
        self.DB_SIMULATION[user_data["username"]] = user_data["email"]
        self.DB_EMAIL_SIM[user_data["email"]] = user_data["username"]
        login_payload = {"username": user_data["username"], "password": user_data["password"]}
        login_headers = {"Content-Type": "application/json"}
        login_resp = requests.post(self.LOGIN_API_URL, json=login_payload, headers=login_headers, timeout=10)
        assert login_resp.status_code == 200, f"Login after registration failed: {login_resp.text}"
        jwt_token = login_resp.json().get("token")
        assert jwt_token, "JWT token not found in login response."
        return {"status_code": reg_resp.status_code, "response": response_json, "jwt_token": jwt_token}

    # --- TC_SCRUM96_007 additions ---
    def tc_scrum96_007_register_and_login(self, user_data):
        """
        Implements TC_SCRUM96_007 Step 1: Register and login a test user to obtain valid JWT authentication token.
        Args:
            user_data (dict): {"username", "email", "password", "firstName", "lastName"}
        Returns:
            dict: {"status_code": int, "response": dict, "jwt_token": str}
        """
        return self.tc_scrum96_004_register_user_and_get_jwt(user_data)
