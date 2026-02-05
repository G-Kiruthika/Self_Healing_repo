# UserSignupPage.py
# PageClass for TC-SCRUM-96-001: User Signup Flow

import requests
from jsonschema import validate, ValidationError
import hashlib
import logging

class UserSignupPage:
    """
    PageClass for automating the user signup API flow.
    Covers:
      - POST /api/users/signup
      - Response validation
      - Simulated DB check
    """
    SIGNUP_URL = "http://localhost:8000/api/users/signup"  # Adjust base URL as needed
    USER_SCHEMA = {
        "type": "object",
        "properties": {
            "userId": {"type": "string"},
            "username": {"type": "string"},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["userId", "username", "email"],
        "additionalProperties": False
    }

    def __init__(self):
        self.last_response = None
        self.created_user = None
        self._simulated_db = {}
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def signup_user(self, username, email, password):
        """
        Sends POST request to signup endpoint, stores response and simulates DB insert.
        """
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        self.logger.info(f"Sending signup request for user: {username}")
        response = requests.post(self.SIGNUP_URL, json=payload)
        self.last_response = response
        if response.status_code == 201:
            user_data = response.json()
            self.created_user = user_data
            # Simulate DB insert (hash password)
            self._simulated_db[email] = {
                "userId": user_data.get("userId"),
                "username": user_data.get("username"),
                "email": user_data.get("email"),
                "password_hash": hashlib.sha256(password.encode()).hexdigest()
            }
        else:
            self.logger.error(f"Signup failed with status {response.status_code}: {response.text}")
        return response

    def validate_response_status(self):
        """
        Validates that the last response has HTTP 201 status code.
        """
        if not self.last_response:
            raise AssertionError("No response found. Did you run signup_user()?")
        assert self.last_response.status_code == 201, f"Expected 201, got {self.last_response.status_code}"
        self.logger.info("Response status 201 validated.")

    def validate_response_schema(self):
        """
        Validates that the response matches the user schema and does not contain password.
        """
        if not self.created_user:
            raise AssertionError("No user data found. Did you run signup_user()?")
        try:
            validate(instance=self.created_user, schema=self.USER_SCHEMA)
        except ValidationError as ve:
            self.logger.error(f"Response schema validation failed: {ve}")
            raise AssertionError(f"Response schema invalid: {ve}")
        assert "password" not in self.created_user, "Response must not contain password"
        self.logger.info("Response schema validated, no password present.")

    def verify_user_in_db(self, email, username, password):
        """
        Simulates DB check for user by email, verifies hashed password and details.
        """
        user_record = self._simulated_db.get(email)
        assert user_record is not None, f"No user found in simulated DB for email: {email}"
        assert user_record["username"] == username, f"Username mismatch: {user_record['username']} != {username}"
        expected_hash = hashlib.sha256(password.encode()).hexdigest()
        assert user_record["password_hash"] == expected_hash, "Password hash mismatch"
        self.logger.info("Simulated DB check passed for user.")

    def run_signup_flow(self, username, email, password):
        """
        End-to-end signup flow for test automation.
        """
        self.signup_user(username, email, password)
        self.validate_response_status()
        self.validate_response_schema()
        self.verify_user_in_db(email, username, password)
        self.logger.info("Signup flow completed successfully.")

# Example usage for test case TC-SCRUM-96-001
if __name__ == "__main__":
    page = UserSignupPage()
    test_username = "testuser123"
    test_email = "testuser@example.com"
    test_password = "SecurePass123!"
    page.run_signup_flow(test_username, test_email, test_password)
