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

    # --- TC-SCRUM-96-002: Duplicate Email User Signup Test ---
    def tc_scrum_96_002_duplicate_email_signup(self):
        """
        Implements TC-SCRUM-96-002:
        1. Create user with email testuser@example.com
        2. Attempt to create another user with same email, expect HTTP 409 and error message
        3. Verify only one user record exists in DB
        Returns: dict with results for each step
        """
        results = {}
        # Step 1: Create initial user
        username1 = "user1"
        email = "testuser@example.com"
        password1 = "Pass123!"
        response1 = self.signup_user(username1, email, password1)
        results['step1_status'] = response1.status_code
        results['step1_success'] = response1.status_code == 201
        results['step1_response'] = response1.json() if response1.status_code == 201 else response1.text

        # Step 2: Attempt duplicate user creation
        username2 = "user2"
        password2 = "Pass456!"
        payload2 = {
            "username": username2,
            "email": email,
            "password": password2
        }
        response2 = requests.post(self.SIGNUP_URL, json=payload2)
        results['step2_status'] = response2.status_code
        results['step2_success'] = response2.status_code == 409
        results['step2_error_message'] = None
        if response2.status_code == 409:
            try:
                error_json = response2.json()
                results['step2_error_message'] = error_json.get('message', error_json)
            except Exception:
                results['step2_error_message'] = response2.text
        # Step 3: Verify only one record exists in simulated DB
        count = sum(1 for user in self._simulated_db.values() if user['email'] == email)
        results['step3_db_count'] = count
        results['step3_success'] = count == 1
        return results

# Example usage for test case TC-SCRUM-96-002
if __name__ == "__main__":
    page = UserSignupPage()
    results = page.tc_scrum_96_002_duplicate_email_signup()
    print(results)
