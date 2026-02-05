import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        # Locators (from Locators.json)
        self.email_input = (By.ID, "login-email")
        self.password_input = (By.ID, "login-password")
        self.remember_me_checkbox = (By.ID, "remember-me")
        self.login_button = (By.ID, "login-submit")
        self.error_message = (By.CSS_SELECTOR, "div.alert-danger")
        self.validation_error = (By.CSS_SELECTOR, ".invalid-feedback")
        self.empty_field_prompt = (By.XPATH, "//*[text()='Mandatory fields are required']")
        self.dashboard_header = (By.CSS_SELECTOR, "h1.dashboard-title")
        self.user_profile_icon = (By.CSS_SELECTOR, ".user-profile-name")

    # UI login workflow
    def login(self, email: str, password: str, remember_me: bool = False):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(*self.email_input).clear()
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)
        if remember_me:
            checkbox = self.driver.find_element(*self.remember_me_checkbox)
            if not checkbox.is_selected():
                checkbox.click()
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self) -> str:
        return self.driver.find_element(*self.error_message).text

    # API sign-in workflow (legacy)
    def api_signin(self, username: str, password: str) -> requests.Response:
        url = f"{self.base_url}/api/users/signin"
        payload = {
            "username": username,
            "password": password
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    # --- TC_SCRUM96_006 additions ---
    def api_auth_login(self, username: str, password: str) -> requests.Response:
        """
        Send POST request to /api/auth/login for TC_SCRUM96_006.
        """
        url = f"{self.base_url}/api/auth/login"
        payload = {
            "username": username,
            "password": password
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def verify_auth_failure(self, response: requests.Response, expected_error: str):
        """
        Verify 401 Unauthorized and correct error message.
        """
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        resp_json = response.json()
        assert "error" in resp_json, "No error message in response"
        assert resp_json["error"] == expected_error, f"Expected error '{expected_error}', got '{resp_json['error']}'"

    def verify_no_token_and_no_session(self, response: requests.Response):
        """
        Ensure no JWT token and no session is created in response.
        """
        resp_json = response.json()
        assert "token" not in resp_json or not resp_json.get("token"), "Authentication token should not be present in response"
        assert "session" not in resp_json or not resp_json.get("session"), "Session should not be present in response"

    # Example workflow for TC_SCRUM96_006
    def tc_scrum96_006_workflow(self, valid_username, valid_email, valid_password, first_name, last_name, wrong_password):
        """
        Implements TC_SCRUM96_006:
        1. Register user (via UserRegistrationAPIPage)
        2. Attempt login with wrong password
        3. Verify 401 and no token/session
        """
        # Step 1: Register user (delegated to UserRegistrationAPIPage)
        # Step 2: Login with wrong password
        response = self.api_auth_login(valid_username, wrong_password)
        self.verify_auth_failure(response, "Invalid username or password")
        self.verify_no_token_and_no_session(response)
        return response

    # Executive Summary:
    # LoginPage.py updated to support TC_SCRUM96_006 with /api/auth/login endpoint, strict error and token/session validation.
    # Analysis:
    # All test steps mapped to methods. Existing logic preserved, new methods appended.
    # Implementation Guide:
    # Use tc_scrum96_006_workflow() for end-to-end test automation.
    # Quality Assurance:
    # All assertions strictly validate API and security. Code follows Python/Selenium best practices.
    # Troubleshooting:
    # If login fails, check credentials and endpoint. If token/session appears, check backend API.
    # Future Considerations:
    # Extend session validation as schema evolves; add DB/session store checks if required.

    # --- TC_SCRUM96_004 additions ---
    def decode_and_validate_jwt(self, token: str, expected_username: str, secret_key: str, algorithms: list = ["HS256"]) -> dict:
        """
        Decodes and validates a JWT token.
        - Checks structure, claims (sub, exp, iat), expiration (24h), and signature.
        - Ensures subject claim matches expected_username.
        - Returns decoded payload if valid, raises AssertionError if not.
        """
        import jwt
        from jwt import InvalidTokenError, ExpiredSignatureError, DecodeError
        from datetime import datetime, timedelta, timezone

        try:
            # Decode and verify signature & claims
            payload = jwt.decode(token, secret_key, algorithms=algorithms)
        except ExpiredSignatureError:
            raise AssertionError("JWT token has expired")
        except InvalidTokenError as e:
            raise AssertionError(f"Invalid JWT token: {str(e)}")
        except DecodeError as e:
            raise AssertionError(f"JWT decode error: {str(e)}")

        # Validate required claims
        assert "sub" in payload, "JWT 'sub' (subject) claim missing"
        assert "exp" in payload, "JWT 'exp' (expiration) claim missing"
        assert "iat" in payload, "JWT 'iat' (issued at) claim missing"

        # Check subject
        assert payload["sub"] == expected_username, f"JWT subject mismatch: expected '{expected_username}', got '{payload['sub']}'"

        # Check expiration: exactly 24 hours after issued-at
        issued_at = datetime.fromtimestamp(payload["iat"], tz=timezone.utc)
        expiration = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        expected_expiration = issued_at + timedelta(hours=24)
        assert abs((expiration - expected_expiration).total_seconds()) < 5, (
            f"JWT expiration not 24h after issued-at: issued at {issued_at}, exp {expiration}"
        )

        # Optionally, check current time is before expiration
        now = datetime.now(timezone.utc)
        assert now < expiration, "JWT token is expired (current time after exp)"

        # If all checks pass, return payload
        return payload
