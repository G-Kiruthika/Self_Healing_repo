import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import jwt
from typing import Optional, Dict, Any

class LoginPage:
    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        # Locators (from Locators.json)
        self.email_input = (By.ID, "login-email")
        self.password_input = (By.ID, "login-password")
        self.login_button = (By.ID, "login-submit")
        self.error_message = (By.CSS_SELECTOR, "div.alert-danger")
        self.dashboard_header = (By.CSS_SELECTOR, "h1.dashboard-title")
        self.user_profile_icon = (By.CSS_SELECTOR, ".user-profile-name")

    # UI login workflow
    def login(self, email: str, password: str) -> Optional[str]:
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(*self.email_input).clear()
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.dashboard_header)
        )
        # Optionally fetch JWT token from local storage if set by frontend
        return self.get_jwt_token_from_storage()

    def get_error_message(self) -> str:
        return self.driver.find_element(*self.error_message).text

    # API sign-in workflow
    def api_signin(self, email: str, password: str) -> requests.Response:
        url = f"{self.base_url}/api/users/signin"
        payload = {
            "email": email,
            "password": password
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def verify_signin_success(self, response: requests.Response) -> Optional[str]:
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        resp_json = response.json()
        assert "token" in resp_json, "Authentication token not returned"
        return resp_json["token"]

    @staticmethod
    def validate_jwt_token(token: str, secret: str, algorithms: Optional[list] = None) -> Dict[str, Any]:
        """
        Decodes and validates JWT token.
        Returns the decoded payload if valid, raises jwt exceptions otherwise.
        """
        if algorithms is None:
            algorithms = ["HS256"]
        payload = jwt.decode(token, secret, algorithms=algorithms)
        # Validate required claims
        assert "userId" in payload, "userId missing in JWT"
        assert "email" in payload, "email missing in JWT"
        assert "exp" in payload, "exp (expiration) missing in JWT"
        return payload

    def get_jwt_token_from_storage(self) -> Optional[str]:
        # Example for localStorage; adapt for your app's storage mechanism
        try:
            token = self.driver.execute_script("return window.localStorage.getItem('jwt_token');")
            return token
        except Exception:
            return None

    # Existing methods preserved from previous implementation
    def verify_signin_failure(self, response: requests.Response, expected_error: str):
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        resp_json = response.json()
        assert "error" in resp_json, "No error message in response"
        assert resp_json["error"] == expected_error, f"Expected error '{expected_error}', got '{resp_json['error']}'"

    def verify_no_token(self, response: requests.Response):
        resp_json = response.json()
        assert "token" not in resp_json or not resp_json.get("token"), "Authentication token should not be present in response"
