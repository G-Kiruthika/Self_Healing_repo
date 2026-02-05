from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pymysql

class ProfilePage:
    """
    Page Object for User Profile workflows, including profile update via PUT request and database verification.
    """
    URL = "https://example-ecommerce.com/profile"
    PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")  # From LoginPage locators
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")  # For post-login verification

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to_profile_page(self):
        """
        Navigates to the Profile page after login.
        """
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.PROFILE_ICON))

    @staticmethod
    def sign_in_and_get_token(email, password):
        """
        Signs in via API and returns authentication token.
        """
        api_url = "https://example-ecommerce.com/api/users/login"
        payload = {"email": email, "password": password}
        response = requests.post(api_url, json=payload)
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "token" in data, "No token returned in login response"
        return data["token"]

    @staticmethod
    def update_profile_put(token, username):
        """
        Sends PUT request to update profile username. Returns response.
        """
        api_url = "https://example-ecommerce.com/api/users/profile"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"username": username}
        response = requests.put(api_url, json=payload, headers=headers)
        assert response.status_code == 200, f"Profile update failed: {response.text}"
        data = response.json()
        assert data.get("username") == username, f"Returned username mismatch: {data}"
        return data

    @staticmethod
    def verify_username_in_db(db_connection, email, expected_username):
        """
        Verifies the updated username in the database.
        """
        query = f"SELECT username FROM users WHERE email='{email}'"
        cursor = db_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        assert result is not None, f"No user found for email {email}"
        actual_username = result[0]
        assert actual_username == expected_username, f"Expected username '{expected_username}', got '{actual_username}'"
        return actual_username

    def full_profile_update_workflow(self, email, password, new_username, db_connection):
        """
        Complete workflow:
        1. Sign in and get token
        2. Send PUT request to update username
        3. Verify DB persistence
        """
        token = self.sign_in_and_get_token(email, password)
        api_result = self.update_profile_put(token, new_username)
        db_username = self.verify_username_in_db(db_connection, email, new_username)
        return {
            "api_result": api_result,
            "db_username": db_username
        }
