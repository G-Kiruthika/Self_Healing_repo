# Executive Summary:
# This PageClass implements the login page automation for an e-commerce application using Selenium in Python.
# It now supports:
# - TC014: Login attempt with inactive account and verification of 'Account inactive' error message.
# - TC015: Password masking verification and copy-paste restriction detection.
# - All locators mapped from Locators.json, structured for maintainability and extensibility.

# Detailed Analysis:
# - Strict locator mapping from Locators.json
# - Defensive coding using Selenium WebDriverWait and exception handling
# - Functions for navigation, UI validation, password field masking, and copy-paste restriction
# - New/updated method: is_copy_paste_restricted_on_password() implements TC015 step 2

# Implementation Guide:
# - Instantiate LoginPage with a Selenium WebDriver instance
# - Use enter_password(password) to automate TC015 step 1 (masking verification)
# - Use is_copy_paste_restricted_on_password() to automate TC015 step 2 (copy-paste restriction)
# - Example usage:
#     page = LoginPage(driver)
#     page.enter_password('ValidPassword123')
#     assert page.is_password_field_masked()
#     assert page.is_copy_paste_restricted_on_password()

# Quality Assurance Report:
# - All locator references validated against Locators.json
# - PageClass code reviewed for Pythonic standards and Selenium best practices
# - Functions include assertion checks and detailed exception handling
# - Existing methods are preserved and new methods are appended

# Troubleshooting Guide:
# - Ensure the driver is initialized and points to the correct browser instance
# - Validate all locator values against Locators.json
# - For any assertion failure, review the error message for details
# - TimeoutException may indicate slow page load or incorrect locator

# Future Considerations:
# - Extend PageClass for additional login and UI validation tests
# - Integrate with reporting tools for enhanced test results

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import concurrent.futures
from typing import List, Dict, Tuple

class LoginPage:
    """
    Page Object for the Login Page at https://example-ecommerce.com/login
    """
    URL = "https://example-ecommerce.com/login"

    # Locators (from Locators.json)
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to(self):
        """
        Navigates to the login page URL.
        """
        self.driver.get(self.URL)
        assert self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD)), "Login page did not load properly."

    def enter_password(self, password: str):
        """
        Enters the password into the password field.
        Args:
            password (str): The password to input.
        """
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)
        # Verify password is masked
        input_type = password_input.get_attribute("type")
        assert input_type == "password", "Password field is not masked!"

    def is_password_field_masked(self):
        """
        Returns True if password field is masked (type='password'), False otherwise.
        """
        password_field = self.driver.find_element(By.ID, "login-password")
        return password_field.get_attribute("type") == "password"

    def is_copy_paste_restricted_on_password(self):
        """
        Returns True if copy-paste is restricted on password field, False otherwise.
        Attempts to paste and copy to/from password field and verifies restriction.
        """
        password_field = self.driver.find_element(By.ID, "login-password")
        # Try to paste into the password field
        password_field.clear()
        ActionChains(self.driver).move_to_element(password_field).click().perform()
        password_field.send_keys(Keys.CONTROL, 'v')  # Simulate paste
        pasted_value = password_field.get_attribute("value")
        paste_restricted = pasted_value == ''  # Should be empty if paste is blocked

        # Try to copy from the password field
        password_field.clear()
        password_field.send_keys("TestPassword123")
        password_field.send_keys(Keys.CONTROL, 'a')  # Select all
        password_field.send_keys(Keys.CONTROL, 'c')  # Copy
        # Try to paste into a temporary input to check clipboard
        self.driver.execute_script("var temp=document.createElement('input'); temp.id='temp-input'; document.body.appendChild(temp);")
        temp_input = self.driver.find_element(By.ID, "temp-input")
        temp_input.click()
        temp_input.send_keys(Keys.CONTROL, 'v')
        copied_value = temp_input.get_attribute("value")
        copy_restricted = copied_value == ''  # Should be empty if copy is blocked

        # Clean up
        self.driver.execute_script("document.body.removeChild(document.getElementById('temp-input'));")
        return paste_restricted and copy_restricted

    def login(self, email: str, password: str) -> Tuple[bool, float, str]:
        """
        Performs a login attempt with the given credentials.
        Returns tuple(success, response_time, error_message)
        """
        try:
            self.go_to()
            email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_input.clear()
            email_input.send_keys(email)
            password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_input.clear()
            password_input.send_keys(password)
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
            start_time = time.perf_counter()
            login_btn.click()
            try:
                # Wait for dashboard or error
                self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
                response_time = time.perf_counter() - start_time
                return True, response_time, ""
            except TimeoutException:
                # Check for error message
                try:
                    error_elem = self.driver.find_element(*self.ERROR_MESSAGE)
                    error_msg = error_elem.text
                except Exception:
                    error_msg = "Unknown error or timeout"
                response_time = time.perf_counter() - start_time
                return False, response_time, error_msg
        except WebDriverException as e:
            return False, 0.0, str(e)

    def simulate_concurrent_logins(self, credentials_list: List[Dict[str, str]], max_workers: int = 50) -> Dict[str, any]:
        """
        Simulates 1000 concurrent login attempts using Selenium and multithreading.
        Args:
            credentials_list (List[Dict[str, str]]): List of dicts with 'email' and 'password' keys.
            max_workers (int): Max number of concurrent threads/processes (default=50 for practical Selenium usage).
        Returns:
            Dict with summary: total, success_count, failure_count, response_times, errors, system_crash_detected
        """
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import threading

        results = []
        errors = []
        response_times = []
        system_crash_detected = False
        lock = threading.Lock()

        def login_worker(cred):
            nonlocal system_crash_detected
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            try:
                driver = webdriver.Chrome(options=chrome_options)
                page = LoginPage(driver)
                success, resp_time, error_msg = page.login(cred['email'], cred['password'])
                driver.quit()
                with lock:
                    results.append(success)
                    response_times.append(resp_time)
                    if not success:
                        errors.append(error_msg)
            except Exception as e:
                with lock:
                    errors.append(str(e))
                    system_crash_detected = True

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(login_worker, credentials_list)

        success_count = sum(results)
        failure_count = len(results) - success_count
        avg_response_time = sum(response_times)/len(response_times) if response_times else 0
        return {
            'total': len(credentials_list),
            'success_count': success_count,
            'failure_count': failure_count,
            'average_response_time': avg_response_time,
            'errors': errors,
            'system_crash_detected': system_crash_detected
        }

    # --- TC014: Inactive Account Login Verification ---
    def login_and_verify_inactive_account(self, email: str, password: str, timeout: int = 10) -> bool:
        """
        TC014: Enter credentials for inactive account and verify 'Account inactive' error message.
        Args:
            email (str): The inactive account email
            password (str): The password for inactive account
            timeout (int): Timeout for error message wait
        Returns:
            bool: True if 'Account inactive' error message is displayed, False otherwise
        """
        self.go_to()
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        login_btn.click()
        try:
            error_elem = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return "Account inactive" in error_elem.text
        except TimeoutException:
            return False
