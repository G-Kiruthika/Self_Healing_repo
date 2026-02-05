# LoginPage.py
"""
Page Object Model for the Login Page.
Auto-generated/updated for TC013: Simulate 1000 concurrent login attempts.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
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
