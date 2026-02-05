import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        # Locators (assumed from Locators.json)
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "loginBtn")
        self.error_message = (By.ID, "loginError")

    # UI login workflow
    def login(self, username: str, password: str):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(*self.username_input).clear()
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self) -> str:
        return self.driver.find_element(*self.error_message).text

    # API sign-in workflow
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

    # Example usage in test case
    # def test_api_signin_failure(self):
    #     response = self.api_signin("known_user", "wrong_password")
    #     self.verify_signin_failure(response, "Invalid username or password")
    #     self.verify_no_token(response)