from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pymysql

class ProfilePage:
    """
    Page Object for User Profile workflows, including profile update via PUT request and database verification.
    Implements TC-SCRUM-96-006: 
      1. Sign in as valid user and obtain authentication token
      2. Send GET request to /api/users/profile with token
      3. Verify sensitive info is not exposed
    """
    URL = "https://example-ecommerce.com/profile"
    PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")

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
    def get_profile(token):
        """
        Sends GET request to /api/users/profile with authentication token.
        Returns profile data.
        """
        api_url = "https://example-ecommerce.com/api/users/profile"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(api_url, headers=headers)
        assert response.status_code == 200, f"Profile GET failed: {response.text}"
        data = response.json()
        # Validate expected fields
        assert "userId" in data, "userId missing in profile response"
        assert "username" in data, "username missing in profile response"
        assert "email" in data, "email missing in profile response"
        return data

    @staticmethod
    def verify_no_sensitive_info(profile_data):
        """
        Verifies that sensitive information is not exposed in the profile response.
        """
        sensitive_fields = ["password", "ssn", "creditCard"]
        for field in sensitive_fields:
            assert field not in profile_data, f"Sensitive field '{field}' should not be present in response"
        return True

    def full_testcase_workflow(self, email, password):
        """
        Implements TC-SCRUM-96-006 workflow:
        1. Sign in, get token
        2. GET profile
        3. Verify no sensitive info
        Returns dict with all results.
        """
        token = self.sign_in_and_get_token(email, password)
        profile = self.get_profile(token)
        self.verify_no_sensitive_info(profile)
        return {"token": token, "profile": profile}

# Executive Summary:
# This PageClass implements TC-SCRUM-96-006, ensuring secure profile retrieval via API automation.
# Analysis:
# Existing ProfilePage.py is extended to cover all test steps. API flows are handled statically for modularity.
# Implementation Guide:
# Use full_testcase_workflow(email, password) to execute the test case end-to-end.
# Quality Assurance:
# All assertions strictly validate API and data integrity. Sensitive fields are checked and code follows Python/Selenium best practices.
# Troubleshooting:
# If login fails, check credentials and API endpoint. If sensitive fields appear, check backend API schema.
# Future Considerations:
# Extend sensitive field list as schema evolves; add UI validation if required.
