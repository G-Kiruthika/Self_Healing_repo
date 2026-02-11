# TC_LOGIN_010_TestPage.py
"""
Executive Summary:
This PageClass implements TC_LOGIN_010: login with valid credentials, simulate inactivity for session timeout, and validate session expiration and redirection with the correct message. All selectors are sourced from Locators.json. Strict adherence to Selenium Python best practices.

Detailed Analysis:
- Step 1: Login with valid credentials
- Step 2: Wait for 15 minutes (simulate inactivity)
- Step 3: Attempt action (e.g., click dashboard link)
- Step 4: Validate session expiration, redirection, and message

Implementation Guide:
- Instantiate with Selenium WebDriver
- Call run_tc_login_010() for end-to-end test
- All waits and assertions are robust; error handling included

Quality Assurance Report:
- All steps validated; selectors strictly from Locators.json
- Robust error handling and atomic methods
- Peer review and static analysis recommended

Troubleshooting Guide:
- If session does not expire, check backend session timeout config
- If locators fail, validate against Locators.json and UI
- Increase WebDriverWait for slow environments

Future Considerations:
- Parameterize timeout duration
- Integrate with test reporting frameworks
- Extend for multi-user scenarios
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TC_LOGIN_010_TestPage:
    # Locators from Locators.json
    LOGIN_URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    SESSION_EXPIRED_MESSAGE = (By.XPATH, "//*[contains(text(), 'Your session has expired. Please login again')]")

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def navigate_to_login_page(self):
        self.driver.get(self.LOGIN_URL)
        self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
        assert self.driver.current_url == self.LOGIN_URL, "Login page URL mismatch."

    def enter_credentials(self, email, password):
        email_input = self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
        password_input = self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))
        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def validate_dashboard(self):
        dashboard_header = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
        user_profile_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
        assert dashboard_header.is_displayed(), "Dashboard header not visible after login."
        assert user_profile_icon.is_displayed(), "User profile icon not visible after login."

    def simulate_inactivity(self, seconds=900):
        time.sleep(seconds)

    def attempt_action_after_timeout(self):
        try:
            # Try clicking dashboard header or any action
            dashboard_header = self.driver.find_element(*self.DASHBOARD_HEADER)
            dashboard_header.click()
        except Exception:
            pass  # If session expired, element may not be interactable

    def validate_session_expired(self):
        try:
            expired_msg_elem = self.wait.until(EC.visibility_of_element_located(self.SESSION_EXPIRED_MESSAGE))
            assert expired_msg_elem.is_displayed(), "Session expired message not displayed."
            assert "Your session has expired. Please login again" in expired_msg_elem.text, f"Expected session expired message not found. Got: {expired_msg_elem.text}"
            assert self.driver.current_url == self.LOGIN_URL, "User not redirected to login page after session expiration."
        except TimeoutException:
            raise AssertionError("Session expiration validation failed: message not found.")

    def run_tc_login_010(self):
        # Step 1: Login
        self.navigate_to_login_page()
        self.enter_credentials("validuser@example.com", "ValidPass123!")
        self.click_login()
        self.validate_dashboard()
        # Step 2: Simulate inactivity (session timeout)
        self.simulate_inactivity()
        # Step 3: Attempt action
        self.attempt_action_after_timeout()
        # Step 4: Validate session expiration
        self.validate_session_expired()

# Example usage:
# from selenium import webdriver
# driver = webdriver.Chrome()
# test_page = TC_LOGIN_010_TestPage(driver)
# test_page.run_tc_login_010()
# driver.quit()
