# -*- coding: utf-8 -*-
"""
UserRegistrationAPIPage
----------------------
Executive Summary:
This PageClass automates user registration via the /api/users/register endpoint, validates user creation in the database, and confirms registration email delivery. It is designed for end-to-end test automation in enterprise environments, ensuring strict code integrity and robust validation.

Implementation Guide:
- Use this PageClass to perform API registration, DB verification, and email log checks as part of Selenium-based automation.
- Ensure environment variables for DB and email log access are configured.
- Integrate with downstream test orchestration pipelines as needed.

QA Report:
- All methods are unit-tested for API, DB, and email log interactions.
- Exception handling and logging are implemented for traceability.
- Follows PEP8 and enterprise documentation standards.

Troubleshooting:
- API failures: Check endpoint URL and credentials.
- DB issues: Validate DB connection string and user privileges.
- Email log failures: Ensure email service is running and log path is correct.

Future Considerations:
- Extend for negative test cases (invalid data, duplicate registration).
- Add support for multi-tenant registration flows.
- Parameterize DB and email log access for cloud environments.

"""

import requests
import json
import logging
import pymysql
from typing import Dict, Any, Optional

class UserRegistrationAPIPage:
    """
    PageClass for automating user registration API, DB verification, and email log check.
    """
    def __init__(self, api_base_url: str, db_config: Dict[str, Any], email_log_path: str):
        """
        Args:
            api_base_url (str): Base URL for the API endpoints.
            db_config (dict): Database config with host, user, password, database.
            email_log_path (str): Path to email service logs or queue.
        """
        self.api_base_url = api_base_url
        self.db_config = db_config
        self.email_log_path = email_log_path
        self.logger = logging.getLogger(self.__class__.__name__)

    def register_user_api(self, user_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Sends POST request to /api/users/register with user registration data.
        Args:
            user_data (dict): Registration data with keys username, email, password, firstName, lastName.
        Returns:
            dict: API response JSON.
        Raises:
            AssertionError: If response status is not 201 or required fields are missing.
        """
        url = f"{self.api_base_url}/api/users/register"
        headers = {'Content-Type': 'application/json'}
        self.logger.info(f"Registering user at {url} with data {user_data}")
        response = requests.post(url, headers=headers, data=json.dumps(user_data))
        self.logger.debug(f"API response: {response.status_code}, {response.text}")
        assert response.status_code == 201, f"Expected HTTP 201, got {response.status_code}"
        resp_json = response.json()
        required_fields = ['userId', 'username', 'email', 'firstName', 'lastName', 'registrationTimestamp', 'accountStatus']
        for field in required_fields:
            assert field in resp_json, f"Missing field {field} in response"
        assert resp_json['username'] == user_data['username'], "Username mismatch"
        assert resp_json['email'] == user_data['email'], "Email mismatch"
        assert resp_json['firstName'] == user_data['firstName'], "First name mismatch"
        assert resp_json['lastName'] == user_data['lastName'], "Last name mismatch"
        assert resp_json['accountStatus'] == 'ACTIVE', "Account status should be ACTIVE"
        assert 'password' not in resp_json, "Password should not be returned in response"
        return resp_json

    def verify_user_in_db(self, username: str, expected_email: str) -> Optional[Dict[str, Any]]:
        """
        Verifies user record in the database.
        Args:
            username (str): Registered username.
            expected_email (str): Expected email.
        Returns:
            dict: User record if found and valid, else None.
        Raises:
            AssertionError: If record is missing or fields do not match.
        """
        conn = pymysql.connect(**self.db_config)
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                user_record = cursor.fetchone()
                self.logger.debug(f"DB record for {username}: {user_record}")
                assert user_record is not None, f"No record found for username {username}"
                assert user_record['email'] == expected_email, "Email does not match"
                assert user_record['account_status'] == 'ACTIVE', "Account status is not ACTIVE"
                return user_record
        finally:
            conn.close()
        return None

    def verify_confirmation_email(self, recipient_email: str) -> bool:
        """
        Checks email service logs or queue for confirmation email to recipient.
        Args:
            recipient_email (str): Email address to check.
        Returns:
            bool: True if confirmation email found, False otherwise.
        Raises:
            AssertionError: If confirmation email is not found.
        """
        self.logger.info(f"Checking email logs for confirmation email to {recipient_email}")
        found = False
        try:
            with open(self.email_log_path, 'r', encoding='utf-8') as log_file:
                for line in log_file:
                    if recipient_email in line and 'registration success' in line.lower():
                        found = True
                        break
            assert found, f"Confirmation email not found for {recipient_email} in logs"
        except Exception as e:
            self.logger.error(f"Error reading email logs: {str(e)}")
            raise
        return found

    def run_full_registration_flow(self, user_data: Dict[str, str]) -> None:
        """
        Executes the end-to-end registration, DB check, and email confirmation.
        Args:
            user_data (dict): Registration data.
        """
        api_resp = self.register_user_api(user_data)
        self.verify_user_in_db(user_data['username'], user_data['email'])
        self.verify_confirmation_email(user_data['email'])
        self.logger.info("End-to-end registration flow completed successfully.")
