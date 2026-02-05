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

    def verify_signin_failure(self, response: requests.Response, expected_error: str):
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        resp_json = response.json()
        assert "error" in resp_json, "No error message in response"
        assert resp_json["error"] == expected_error, f"Expected error '{expected_error}', got '{resp_json['error']}'"

    def verify_no_token(self, response: requests.Response):
        resp_json = response.json()
        assert "token" not in resp_json or not resp_json.get("token"), "Authentication token should not be present in response"

    # --- TC-SCRUM-96-006 additions ---
    def signin_and_get_token(self, email: str, password: str) -> str:
        """
        Sign in as a valid user and return the authentication token.
        """
        url = f"{self.base_url}/api/users/signin"
        payload = {
            "email": email,
            "password": password
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        resp_json = response.json()
        assert "token" in resp_json and resp_json["token"], "No authentication token returned"
        return resp_json["token"]

    def get_user_profile(self, token: str) -> requests.Response:
        """
        Send GET request to /api/users/profile with authentication token.
        """
        url = f"{self.base_url}/api/users/profile"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        return response

    def validate_no_sensitive_info(self, response: requests.Response):
        """
        Validate that sensitive information (like password) is not exposed in the response.
        """
        resp_json = response.json()
        sensitive_fields = ["password", "hash", "salt"]
        for field in sensitive_fields:
            assert field not in resp_json, f"Sensitive field '{field}' should not be present in profile response"
        # Optionally, check nested objects
        for key, value in resp_json.items():
            if isinstance(value, dict):
                for field in sensitive_fields:
                    assert field not in value, f"Sensitive field '{field}' found in nested object '{key}'"

    # Example usage in test case TC-SCRUM-96-006
    # def test_tc_scrum_96_006(self):
    #     token = self.signin_and_get_token("profile@example.com", "Pass123!")
    #     profile_response = self.get_user_profile(token)
    #     self.validate_no_sensitive_info(profile_response)
