import requests
from typing import Optional, Dict, Any

class ProfilePage:
    """
    Page Object for user profile management.
    Provides methods for updating user profile via API and verifying persistence in the database.
    """
    API_URL = "https://example-ecommerce.com/api/users/profile"

    def __init__(self, db_connection: Optional[object] = None):
        """
        Optionally pass a database connection for DB verification methods.
        """
        self.db_connection = db_connection

    def update_profile_username(self, auth_token: str, new_username: str) -> requests.Response:
        """
        Sends a PUT request to update the user's profile username.
        Args:
            auth_token (str): JWT authentication token.
            new_username (str): The new username to set.
        Returns:
            requests.Response: The response object from the PUT request.
        Raises:
            AssertionError: If the HTTP status is not 200 or response data is not as expected.
        """
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        payload = {"username": new_username}
        response = requests.put(self.API_URL, json=payload, headers=headers)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
        data = response.json()
        assert data.get("username") == new_username, f"Username not updated in response. Expected {new_username}, got {data.get('username')}"
        return response

    def verify_username_in_db(self, email: str, expected_username: str) -> bool:
        """
        Verifies that the username is updated in the database for the given email.
        Args:
            email (str): User's email address.
            expected_username (str): Expected username value in DB.
        Returns:
            bool: True if the username matches, False otherwise.
        Raises:
            AssertionError: If db_connection is not set.
        """
        assert self.db_connection is not None, "Database connection is not set."
        query = f"SELECT username FROM users WHERE email='{email}'"
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        if result is None:
            return False
        return result[0] == expected_username

    def get_user_profile_api(self, jwt_token: str) -> Dict[str, Any]:
        """
        Fetches user profile via protected API endpoint using JWT token.
        Args:
            jwt_token (str): JWT access token for Authorization header.
        Returns:
            dict: User profile data from API response.
        Raises:
            AssertionError: If HTTP status is not 200 or profile fields are missing.
        """
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(self.API_URL, headers=headers)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
        data = response.json()
        required_fields = ["userId", "username", "email", "firstName", "lastName", "accountStatus"]
        for field in required_fields:
            assert field in data, f"Missing field {field} in profile response"
        assert data["accountStatus"] == "ACTIVE", "Account status must be ACTIVE"
        return data

    # --- TC_SCRUM96_004: New Methods Below ---
    @staticmethod
    def access_profile_with_jwt(jwt_token: str) -> Dict[str, Any]:
        """
        Accesses the /api/users/profile endpoint with JWT and validates response for TC_SCRUM96_004.
        Args:
            jwt_token (str): JWT access token.
        Returns:
            dict: Profile data from API response.
        Raises:
            AssertionError: If HTTP status or profile fields do not match expected.
        """
        api_url = "https://example-ecommerce.com/api/users/profile"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(api_url, headers=headers)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
        data = response.json()
        required_fields = ["userId", "username", "email", "firstName", "lastName", "accountStatus"]
        for field in required_fields:
            assert field in data, f"Missing field {field} in profile response"
        assert data["accountStatus"] == "ACTIVE", "Account status must be ACTIVE"
        return data
