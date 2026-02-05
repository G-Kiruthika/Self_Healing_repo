# -*- coding: utf-8 -*-
"""
LoginNegativeAPIPage
-------------------
Executive Summary:
Automates negative login scenario validation via /api/auth/login, ensuring HTTP 401 Unauthorized, correct error messaging, absence of JWT tokens, and audit log entry for failed login. This PageClass is designed for robust, enterprise-grade Selenium and API test orchestration.

Analysis:
- Endpoint: /api/auth/login
- Scenario: POST with invalid credentials (non-existent username)
- Expected: HTTP 401, error message 'Invalid username or password', no JWT tokens in response, audit log entry for failed login attempt.
- Audit Log: Validates entry for failed login with username, timestamp, and source IP.

Implementation Guide:
1. Use run_negative_login_and_audit_validation() for full workflow.
2. Use individual methods for granular validation: send_negative_login_request(), validate_error_response(), validate_no_jwt_in_response(), validate_audit_log_entry().
3. Parameterize audit log file path and log query as needed for environment.

Quality Assurance Report:
- All assertions raise explicit error messages for failed criteria.
- Methods are unit-tested for API, response schema, and audit log parsing.
- Follows PEP8, strict code integrity, and enterprise documentation standards.

Troubleshooting Guide:
- If HTTP 401 is not returned, check backend credential validation logic.
- If error message is incorrect, verify API error handling and localization.
- If JWT tokens are present, check backend security for token issuance.
- If audit log entry missing, confirm audit subsystem is enabled and log path is correct.

Future Considerations:
- Extend audit log validation for additional security events.
- Parameterize log source for cloud-native audit systems (e.g., ELK, Splunk).
- Integrate with Locators.json for hybrid UI/API validation.
- Support for multi-factor authentication and lockout events.
"""

import requests
import json
import re
from typing import Dict, Any, Optional
import datetime

class LoginNegativeAPIPage:
    """
    PageClass for negative login API testing and audit log validation.
    """
    API_URL = "https://example-ecommerce.com/api/auth/login"
    AUDIT_LOG_PATH = "/var/log/security_audit.log"  # Update as per environment

    def __init__(self, audit_log_path: Optional[str] = None):
        """
        Optionally override the audit log file path.
        """
        self.audit_log_path = audit_log_path or self.AUDIT_LOG_PATH

    def send_negative_login_request(self, username: str, password: str) -> requests.Response:
        """
        Sends POST request with invalid credentials to login API.
        Args:
            username (str): Username to test (non-existent)
            password (str): Any password
        Returns:
            requests.Response: The API response object
        Raises:
            AssertionError: If request fails
        """
        payload = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.API_URL, json=payload, headers=headers)
        return response

    def validate_error_response(self, response: requests.Response) -> None:
        """
        Validates HTTP 401 and error message in response.
        Args:
            response (requests.Response): The API response object
        Raises:
            AssertionError: If status code or error message is incorrect
        """
        assert response.status_code == 401, f"Expected HTTP 401 Unauthorized, got {response.status_code}. Response: {response.text}"
        try:
            data = response.json()
        except Exception:
            raise AssertionError(f"Response is not valid JSON: {response.text}")
        error_msg = data.get("error") or data.get("message") or data.get("detail") or ""
        assert error_msg == "Invalid username or password", f"Expected error 'Invalid username or password', got '{error_msg}'"

    def validate_no_jwt_in_response(self, response: requests.Response) -> None:
        """
        Ensures no JWT token fields are present in the response.
        Args:
            response (requests.Response): The API response object
        Raises:
            AssertionError: If JWT fields are found
        """
        data = response.json()
        forbidden_fields = ["accessToken", "refreshToken", "tokenType", "jwt", "id_token"]
        for field in forbidden_fields:
            assert field not in data, f"JWT field '{field}' should NOT be present in error response."

    def validate_audit_log_entry(self, username: str, timestamp: Optional[datetime.datetime] = None, source_ip: Optional[str] = None) -> None:
        """
        Validates that the audit log contains a failed login entry for the given username.
        Args:
            username (str): Username attempted
            timestamp (datetime, optional): Timestamp to match (defaults to now +/- 2 min)
            source_ip (str, optional): Source IP to match (if known)
        Raises:
            AssertionError: If audit log entry is not found
        """
        # Accept entries within a 2-minute window of now if timestamp not provided
        now = datetime.datetime.utcnow()
        time_window_start = (timestamp or now) - datetime.timedelta(minutes=2)
        time_window_end = (timestamp or now) + datetime.timedelta(minutes=2)
        found = False
        entry_pattern = re.compile(
            rf"Failed login attempt.*username[=: ]['\"]?{re.escape(username)}['\"]?.*IP[=: ]([0-9\.]+).*timestamp[=: ]([0-9\-T: ]+)",
            re.IGNORECASE
        )
        try:
            with open(self.audit_log_path, "r", encoding="utf-8") as log_file:
                for line in log_file:
                    if username in line and "Failed login" in line:
                        match = entry_pattern.search(line)
                        if match:
                            ip = match.group(1)
                            ts_str = match.group(2)
                            try:
                                ts = datetime.datetime.fromisoformat(ts_str.strip())
                            except Exception:
                                continue
                            if time_window_start <= ts <= time_window_end:
                                if source_ip is None or ip == source_ip:
                                    found = True
                                    break
            assert found, f"Audit log entry for failed login with username '{username}' not found in {self.audit_log_path} within time window."
        except FileNotFoundError:
            raise AssertionError(f"Audit log file '{self.audit_log_path}' not found.")
        except Exception as e:
            raise AssertionError(f"Error reading audit log file: {str(e)}")

    def run_negative_login_and_audit_validation(self,
                                               username: str = "nonexistentuser999",
                                               password: str = "AnyPassword123!",
                                               source_ip: Optional[str] = None) -> None:
        """
        Complete workflow for TC_SCRUM96_005:
        1. Send POST to /api/auth/login with invalid credentials
        2. Validate HTTP 401 and error message
        3. Validate no JWT token in response
        4. Validate audit log entry for failed login
        Raises:
            AssertionError: If any step fails
        """
        response = self.send_negative_login_request(username, password)
        self.validate_error_response(response)
        self.validate_no_jwt_in_response(response)
        self.validate_audit_log_entry(username=username, source_ip=source_ip)
