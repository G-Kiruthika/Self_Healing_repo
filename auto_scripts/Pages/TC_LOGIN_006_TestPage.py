"""
TC_LOGIN_006_TestPage.py

Executive Summary:
------------------
This PageClass automates the end-to-end negative login scenario for test case TC_LOGIN_006: entering a valid username, leaving the password field empty, clicking Login, and verifying that the error message 'Password is required' is displayed. The implementation strictly follows Selenium Python automation best practices, ensures code integrity, and produces structured output for downstream automation and CI/CD pipelines.

Detailed Analysis:
------------------
- Utilizes locators from Locators.json for strict mapping and maintainability.
- Implements explicit waits and robust error handling for each step.
- All methods are atomic, idempotent, and suitable for pipeline orchestration.
- Validates that the user remains on the login page after the failed login attempt.

Implementation Guide:
---------------------
1. Instantiate TC_LOGIN_006_TestPage with Selenium WebDriver.
2. Call run_tc_login_006(username, url) for end-to-end test.
3. Validate the returned dict for stepwise results and error messages.
4. Integrate into CI/CD or downstream pipeline as needed.

Quality Assurance Report:
------------------------
- All imports and locators validated.
- Exception handling ensures atomic failure reporting.
- Output structure matches downstream requirements.
- Peer review and static analysis recommended before deployment.

Troubleshooting Guide:
----------------------
- If validation error not found, validate locator and backend logic.
- If user is not on login page after failed login, check for UI or session handling changes.
- Increase WebDriverWait timeout for slow environments.
- Ensure browser drivers are up to date and compatible with Selenium version.

Future Considerations:
----------------------
- Parameterize URLs and error messages for multi-environment and multi-locale support.
- Extend for additional negative login scenarios (e.g., locked account, expired password).
- Integrate with test reporting frameworks for automated QA.
- Add retry logic and audit reporting for improved resilience.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

class TC_LOGIN_006_TestPage:
    """
    PageClass for Test Case TC_LOGIN_006: Leave password field empty and validate error handling.
    Implements all steps as per test case and validates error handling.
    """
    def __init__(self, driver, timeout=10, locators_path="auto_scripts/Locators/Locators.json"):
        """
        Initializes the PageClass for TC_LOGIN_006.
        Args:
            driver: Selenium WebDriver instance
            timeout: Explicit wait timeout (default: 10 seconds)
            locators_path: Path to Locators.json file
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        # Load locators strictly from Locators.json
        with open(locators_path, "r") as f:
            locators_data = json.load(f)
            self.locators = locators_data.get("LoginPage", {})
        self.url = "https://app.example.com/login"
        self.email_field = self.locators["inputs"].get("emailField", "id=login-email")
        self.password_field = self.locators["inputs"].get("passwordField", "id=login-password")
        self.login_button = self.locators["buttons"].get("loginSubmit", "id=login-submit")
        # Prefer validationError, fallback to errorMessage
        self.validation_error = self.locators["messages"].get("validationError", ".invalid-feedback")
        self.error_message = self.locators["messages"].get("errorMessage", "div.alert-danger")

    def go_to_login_page(self, url=None):
        """
        Navigates to the login page and waits for the email field to be visible.
        Args:
            url: Optional URL override
        """
        self.driver.get(url or self.url)
        self.wait.until(EC.visibility_of_element_located((By.ID, self.email_field.split("=",1)[1])))

    def enter_username(self, username):
        """
        Enters the username into the email/username field.
        Args:
            username: The username/email to enter
        """
        email_input = self.wait.until(EC.visibility_of_element_located((By.ID, self.email_field.split("=",1)[1])))
        email_input.clear()
        email_input.send_keys(username)

    def leave_password_empty(self):
        """
        Ensures the password field is empty (clears any value).
        """
        password_input = self.wait.until(EC.visibility_of_element_located((By.ID, self.password_field.split("=",1)[1])))
        password_input.clear()
        # Do not send any keys (leave empty)

    def click_login(self):
        """
        Clicks the Login button.
        """
        login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, self.login_button.split("=",1)[1])))
        login_btn.click()

    def get_validation_error(self):
        """
        Retrieves the validation error message displayed for empty password field.
        Returns:
            str or None: The error message text if found, else None
        """
        # Try validationError first (usually .invalid-feedback), fallback to errorMessage
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.validation_error)))
            return error_elem.text
        except TimeoutException:
            try:
                error_elem = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.error_message)))
                return error_elem.text
            except TimeoutException:
                return None

    def is_on_login_page(self):
        """
        Validates that the user is still on the login page by checking for presence of login fields.
        Returns:
            bool: True if login fields are present, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, self.email_field.split("=",1)[1])))
            self.wait.until(EC.visibility_of_element_located((By.ID, self.password_field.split("=",1)[1])))
            return True
        except Exception:
            return False

    def run_tc_login_006(self, username, url=None):
        """
        Executes the TC_LOGIN_006 workflow:
        1. Navigate to login page
        2. Enter valid username
        3. Leave password field empty
        4. Click Login button
        5. Validate error is displayed and login is prevented
        Args:
            username: Valid username/email to use
            url: Optional login page URL override
        Returns:
            dict: Stepwise results and validation messages for downstream automation
        """
        results = {
            "step_1_navigate_login": None,
            "step_2_enter_username": None,
            "step_3_leave_password_empty": None,
            "step_4_click_login": None,
            "step_5_validation_error": None,
            "step_6_login_prevented": None,
            "overall_pass": False,
            "exception": None
        }
        try:
            # Step 1: Navigate to login page
            self.go_to_login_page(url)
            results["step_1_navigate_login"] = self.is_on_login_page()
            if not results["step_1_navigate_login"]:
                results["exception"] = "Login page not displayed."
                return results
            # Step 2: Enter valid username
            self.enter_username(username)
            results["step_2_enter_username"] = True
            # Step 3: Leave password field empty
            self.leave_password_empty()
            results["step_3_leave_password_empty"] = True
            # Step 4: Click Login button
            self.click_login()
            results["step_4_click_login"] = True
            # Step 5: Validate error is displayed
            validation_error = self.get_validation_error()
            results["step_5_validation_error"] = validation_error
            # Step 6: Validate login is prevented (still on login page)
            results["step_6_login_prevented"] = self.is_on_login_page()
            # Overall pass: error present and login prevented
            results["overall_pass"] = (
                (validation_error is not None and 'password is required' in validation_error.lower())
                and results["step_6_login_prevented"]
            )
        except Exception as e:
            results["exception"] = f"Test flow failed: {str(e)}"
        return results
