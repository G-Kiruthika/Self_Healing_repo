# Executive Summary:
# UserRegistrationAPIPage implements TC_SCRUM96_002: API registration, DB validation, and duplicate username handling.
# Analysis:
# This PageClass enables robust API automation for user registration workflows, including duplicate username conflict handling and database integrity checks.
# Implementation Guide:
# Use register_user_api(), register_duplicate_user_api(), and verify_single_user_in_db() methods for end-to-end test automation of TC_SCRUM96_002.
# Quality Assurance:
# All assertions strictly validate API, DB, and error criteria. Code follows Python/Selenium best practices.
# Troubleshooting:
# If registration fails, check API endpoint and payload. DB validation requires correct connection and schema. Conflict handling depends on API error response.
# Future Considerations:
# Extend DB/email log validation as schema evolves; add UI registration validation if required.

import requests
import pymysql
import json

class UserRegistrationAPIPage:
    """
    Page Object for User Registration API workflow for TC_SCRUM96_002.
    Implements:
      1. API POST to /api/users/register for first user
      2. API POST to /api/users/register for duplicate username
      3. Database user creation verification (only one user with username)
    """

    BASE_URL = "https://example-ecommerce.com"  # Replace with actual API base URL

    def __init__(self, db_config=None):
        """
        db_config: dict with keys host, user, password, database
        """
        self.db_config = db_config

    def register_user_api(self, username, email, password, first_name, last_name):
        """
        Sends POST request to /api/users/register with user data.
        Returns response object.
        """
        url = f"{self.BASE_URL}/api/users/register"
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "firstName": first_name,
            "lastName": last_name
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        return response

    def register_duplicate_user_api(self, username, email, password, first_name, last_name):
        """
        Attempts to register a user with a duplicate username.
        Returns response object.
        """
        return self.register_user_api(username, email, password, first_name, last_name)

    def verify_single_user_in_db(self, username, expected_email):
        """
        Queries DB users table for the registered username.
        Asserts that only one record exists and email matches expected_email.
        Returns count and email.
        """
        assert self.db_config is not None, "Database config not provided"
        connection = pymysql.connect(
            host=self.db_config["host"],
            user=self.db_config["user"],
            password=self.db_config["password"],
            database=self.db_config["database"]
        )
        try:
            with connection.cursor() as cursor:
                query = "SELECT COUNT(*), email FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                count, db_email = result
                assert count == 1, f"Expected 1 record for username {username}, found {count}"
                assert db_email == expected_email, f"Expected email {expected_email}, got {db_email}"
                return count, db_email
        finally:
            connection.close()

    def full_tc_scrum96_002_workflow(self):
        """
        Implements TC_SCRUM96_002 end-to-end workflow:
        1. Register first user
        2. Attempt duplicate registration
        3. Verify DB only has one record
        """
        # Step 1: Register first user
        resp1 = self.register_user_api("duplicateuser", "first@example.com", "Pass123!", "First", "User")
        assert resp1.status_code == 201, f"Expected 201 Created, got {resp1.status_code}, response: {resp1.text}"

        # Step 2: Attempt duplicate registration
        resp2 = self.register_duplicate_user_api("duplicateuser", "second@example.com", "Pass456!", "Second", "User")
        assert resp2.status_code == 409, f"Expected 409 Conflict, got {resp2.status_code}, response: {resp2.text}"
        assert "username already exists" in resp2.text.lower(), f"Expected error message for duplicate username, got: {resp2.text}"

        # Step 3: Verify only one user record exists in DB
        count, db_email = self.verify_single_user_in_db("duplicateuser", "first@example.com")
        assert count == 1, f"Expected 1 user record, found {count}"
        assert db_email == "first@example.com", f"Expected email 'first@example.com', got {db_email}"
        return {
            "api_response_1": resp1.text,
            "api_response_2": resp2.text,
            "db_user_count": count,
            "db_email": db_email
        }

# Example usage:
# db_cfg = {"host": "localhost", "user": "root", "password": "pwd", "database": "ecommerce"}
# page = UserRegistrationAPIPage(db_config=db_cfg)
# page.full_tc_scrum96_002_workflow()
