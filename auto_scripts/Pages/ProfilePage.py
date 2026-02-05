from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pymysql
from JWTUtils import JWTUtils

class ProfilePage:
    ...
    # --- TC_SCRUM96_004 additions ---
    @staticmethod
    def tc_scrum96_004_get_profile_and_validate(jwt_token: str, expected_username: str, expected_email: str):
        """
        Implements TC_SCRUM96_004 Step 4: Access protected profile endpoint and validate user data.
        Args:
            jwt_token (str): JWT token for Authorization
            expected_username (str): Expected username in profile
            expected_email (str): Expected email in profile
        Returns:
            dict: {"status_code": int, "profile_data": dict}
        Raises:
            AssertionError: On validation failure
        """
        api_url = "https://example-ecommerce.com/api/users/profile"
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(api_url, headers=headers)
        assert response.status_code == 200, f"Profile GET failed: {response.text}"
        data = response.json()
        expected_fields = ["userId", "username", "email", "firstName", "lastName", "registrationDate", "accountStatus"]
        for field in expected_fields:
            assert field in data, f"{field} missing in profile response"
        assert data["username"] == expected_username, f"Username mismatch: expected {expected_username}, got {data['username']}"
        assert data["email"] == expected_email, f"Email mismatch: expected {expected_email}, got {data['email']}"
        payload = JWTUtils.decode_jwt(jwt_token, verify_signature=False)
        assert payload["sub"] == expected_username, f"JWT subject claim mismatch: expected {expected_username}, got {payload['sub']}"
        return {"status_code": response.status_code, "profile_data": data}

    # --- TC_SCRUM96_007 additions ---
    @staticmethod
    def tc_scrum96_007_get_profile_and_validate(jwt_token: str, expected_user_data: dict, db_config: dict):
        """
        Implements TC_SCRUM96_007 Steps 2 & 3: GET /api/users/profile and validate all fields against DB.
        Args:
            jwt_token (str): JWT token for Authorization
            expected_user_data (dict): Registered user data
            db_config (dict): DB connection parameters
        Returns:
            dict: {"status_code": int, "profile_data": dict, "db_validation": bool}
        """
        api_url = "https://example-ecommerce.com/api/users/profile"
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(api_url, headers=headers)
        assert response.status_code == 200, f"Profile GET failed: {response.text}"
        profile_data = response.json()
        expected_fields = ["userId", "username", "email", "firstName", "lastName", "registrationDate", "accountStatus"]
        for field in expected_fields:
            assert field in profile_data, f"{field} missing in profile response"
        # DB validation
        conn = pymysql.connect(**db_config)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT userId, username, email, firstName, lastName, registrationDate, accountStatus FROM users WHERE username=%s", (expected_user_data["username"],))
                db_row = cur.fetchone()
                assert db_row, f"No DB record found for username={expected_user_data['username']}"
                db_fields = dict(zip(expected_fields, db_row))
                for field in expected_fields:
                    assert profile_data[field] == db_fields[field], f"Mismatch in {field}: API={profile_data[field]}, DB={db_fields[field]}"
        finally:
            conn.close()
        return {"status_code": response.status_code, "profile_data": profile_data, "db_validation": True}
