# Executive Summary:
# UserRegistrationAPIPage implements TC_SCRUM96_001: API registration, DB validation, and email log verification.
# Analysis:
# This PageClass enables robust API automation for user registration workflows, database integrity checks, and email confirmation validation.
# Implementation Guide:
# Use register_user_api(), verify_user_in_db(), and check_email_log() methods for end-to-end test automation.
# Quality Assurance:
# All assertions strictly validate API, DB, and email log criteria. Code follows Python/Selenium best practices.
# Troubleshooting:
# If registration fails, check API endpoint and payload. DB validation requires correct connection and schema. Email log check depends on log format and access.
# Future Considerations:
# Extend DB/email log validation as schema evolves; add UI registration validation if required.

import requests
import pymysql
import json

class UserRegistrationAPIPage:
    """
    Page Object for User Registration API workflow.
    Implements:
      1. API POST to /api/users/register
      2. Database user creation verification
      3. Registration email log check
    """

    BASE_URL = "https://example-ecommerce.com"  # Replace with actual API base URL

    def __init__(self, db_config=None, email_log_path=None):
        """
        db_config: dict with keys host, user, password, database
        email_log_path: path to email service log file or endpoint
        """
        self.db_config = db_config
        self.email_log_path = email_log_path

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
        assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"
        resp_json = response.json()
        assert "userId" in resp_json, "userId missing in response"
        assert resp_json["username"] == username, "Username mismatch"
        assert resp_json["email"] == email, "Email mismatch"
        assert resp_json["firstName"] == first_name, "First name mismatch"
        assert resp_json["lastName"] == last_name, "Last name mismatch"
        assert "password" not in resp_json, "Password should not be returned in response"
        return resp_json

    def verify_user_in_db(self, username):
        """
        Queries DB users table for the registered username.
        Returns dict with DB record.
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
                query = f"SELECT userId, username, email, password, account_status FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                assert result is not None, f"No user found for username {username}"
                user_id, db_username, db_email, db_password, account_status = result
                assert db_username == username, "Username mismatch in DB"
                assert db_email is not None and "@" in db_email, "Email format incorrect in DB"
                assert db_password is not None and db_password != password, "Password should be hashed in DB"
                assert account_status == "ACTIVE", f"Account status is not ACTIVE, got {account_status}"
                return {
                    "userId": user_id,
                    "username": db_username,
                    "email": db_email,
                    "password_hash": db_password,
                    "account_status": account_status
                }
        finally:
            connection.close()

    def check_email_log(self, recipient_email):
        """
        Checks email service logs or queue for confirmation email sent to recipient.
        Returns log entry or raises AssertionError.
        """
        assert self.email_log_path is not None, "Email log path not provided"
        # Example: log file parsing; adapt as needed for log service/queue
        with open(self.email_log_path, "r") as log_file:
            logs = log_file.readlines()
            found = False
            for line in logs:
                if recipient_email in line and "registration success" in line.lower():
                    found = True
                    break
            assert found, f"No confirmation email found for {recipient_email} in logs"
        return True

    def full_workflow(self, username, email, password, first_name, last_name):
        """
        Executes TC_SCRUM96_001 end-to-end workflow.
        """
        api_resp = self.register_user_api(username, email, password, first_name, last_name)
        db_record = self.verify_user_in_db(username)
        email_log_result = self.check_email_log(email)
        return {
            "api_response": api_resp,
            "db_record": db_record,
            "email_log": email_log_result
        }

# Example usage:
# db_cfg = {"host": "localhost", "user": "root", "password": "pwd", "database": "ecommerce"}
# email_log = "/var/log/email_service.log"
# page = UserRegistrationAPIPage(db_config=db_cfg, email_log_path=email_log)
# page.full_workflow("testuser001", "testuser001@example.com", "SecurePass123!", "John", "Doe")
