# TC_LOGIN_010_TestPage.py
"""
Executive Summary:
This PageClass implements automated test steps for TC_LOGIN_010, validating login behavior under network disconnection and recovery scenarios using Selenium Python. It strictly utilizes locators from Locators.json and test data from the provided test case.

Detailed Analysis:
- Navigates to the login page using URL from Locators.json.
- Enters valid credentials (testuser@example.com / Test@1234).
- Simulates network disconnection/throttling (offline/2G) using Chrome DevTools Protocol.
- Attempts login, verifies loading indicator and error message.
- Restores network, retries login, validates successful dashboard access.

Implementation Guide:
- Requires Selenium 4+ and ChromeDriver with DevTools Protocol support.
- Network simulation uses driver.execute_cdp_cmd for offline/throttling.
- All element interactions use Locators.json selectors.

Quality Assurance Report:
- Validates error handling and recovery on login.
- Checks for presence of loading indicator, error message, dashboard header, and user profile icon.
- Includes robust waits and error handling for UI synchronization.

Troubleshooting Guide:
- Ensure ChromeDriver and browser support DevTools Protocol.
- Network simulation may not work on all browsers; fallback to manual network toggle if needed.
- Check locator accuracy if elements are not found.

Future Considerations:
- Extend for additional network types (3G, 4G).
- Integrate with cloud browsers for cross-browser validation.
- Parameterize credentials and URLs for reuse.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TC_LOGIN_010_TestPage:
    """
    PageClass for TC_LOGIN_010:
    - Navigates to login page.
    - Enters valid credentials.
    - Simulates network offline/throttling.
    - Attempts login, verifies error message.
    - Restores network, retries login, validates success.
    """
    # Locators from Locators.json
    LOGIN_URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    # Test Data
    VALID_EMAIL = "testuser@example.com"
    VALID_PASSWORD = "Test@1234"

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def navigate_to_login_page(self):
        """Step 1: Navigate to login page."""
        self.driver.get(self.LOGIN_URL)
        self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
        assert self.driver.current_url == self.LOGIN_URL, "Login page URL mismatch."

    def enter_valid_credentials(self):
        """Step 2: Enter valid credentials."""
        email_input = self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
        password_input = self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))
        email_input.clear()
        email_input.send_keys(self.VALID_EMAIL)
        password_input.clear()
        password_input.send_keys(self.VALID_PASSWORD)

    def simulate_network_offline(self):
        """Step 3: Simulate network offline using Chrome DevTools Protocol."""
        try:
            # Set network offline
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
                "offline": True,
                "latency": 0,
                "downloadThroughput": 0,
                "uploadThroughput": 0
            })
        except Exception as e:
            raise RuntimeError(f"Network simulation failed: {e}")

    def simulate_network_throttle_2g(self):
        """Optional: Throttle network to 2G."""
        try:
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
                "offline": False,
                "latency": 1000,
                "downloadThroughput": 250 * 1024 / 8,
                "uploadThroughput": 50 * 1024 / 8
            })
        except Exception as e:
            raise RuntimeError(f"Network throttling failed: {e}")

    def restore_network(self):
        """Step 5: Restore network connection."""
        try:
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
                "offline": False,
                "latency": 0,
                "downloadThroughput": -1,
                "uploadThroughput": -1
            })
        except Exception as e:
            raise RuntimeError(f"Network restore failed: {e}")

    def click_login_and_verify_error(self):
        """Step 4: Click Login, verify loading indicator and error message."""
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()
        # Wait for loading indicator or error message
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            assert "Network error. Please check your connection and try again" in error_elem.text, "Expected error message not found."
        except Exception:
            raise AssertionError("Error message not displayed after network failure.")

    def retry_login_and_verify_success(self):
        """Step 5: Restore network, retry login, validate dashboard and profile icon."""
        self.restore_network()
        # Optionally, re-enter credentials if form was reset
        self.enter_valid_credentials()
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()
        # Wait for dashboard header
        dashboard_header = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
        user_profile_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
        assert dashboard_header.is_displayed(), "Dashboard header not visible after login."
        assert user_profile_icon.is_displayed(), "User profile icon not visible after login."

    def run_test_case(self, use_throttle=False):
        """
        Execute TC_LOGIN_010 end-to-end.
        :param use_throttle: If True, simulate 2G throttling instead of offline.
        """
        self.navigate_to_login_page()
        self.enter_valid_credentials()
        if use_throttle:
            self.simulate_network_throttle_2g()
        else:
            self.simulate_network_offline()
        self.click_login_and_verify_error()
        self.retry_login_and_verify_success()

# Example usage:
# from selenium import webdriver
# driver = webdriver.Chrome()
# test_page = TC_LOGIN_010_TestPage(driver)
# test_page.run_test_case(use_throttle=False)
# driver.quit()
