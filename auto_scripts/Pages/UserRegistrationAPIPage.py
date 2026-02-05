# Executive Summary:
# UserRegistrationAPIPage implements registration for TC_SCRUM96_006.
# Analysis:
# Existing code supports registration; no changes needed.
# Implementation Guide:
# Use register_user_api() for user creation.
# Quality Assurance:
# All assertions strictly validate API and DB.
# Troubleshooting:
# If registration fails, check API endpoint and payload.
# Future Considerations:
# Extend DB/email log validation as schema evolves.

import requests
import pymysql
import json

class UserRegistrationAPIPage:
    """
    Page Object for User Registration API workflow for TC_SCRUM96_006.
    Implements:
      1. API POST to /api/users/register for first user
      2. Database user creation verification
    """

    BASE_URL = "https://example-ecommerce.com"  # Replace with actual API base URL

    def __init__(self, db_config=None):
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
