"""
TC_LOGIN_004_TestPage.py

Executive Summary:
------------------
This PageClass automates the end-to-end negative login scenario for test case TC-LOGIN-004: leaving the email field empty, entering a valid password, clicking Login, and verifying that the validation error is displayed and the user remains on the login page. The implementation strictly follows Selenium Python automation best practices, maintains code integrity, and produces structured output for downstream automation.

Detailed Analysis:
------------------
- Utilizes locators from Locators.json for strict mapping.
- Implements explicit waits and robust error handling for each step.
- Ensures all steps are atomic, idempotent, and suitable for pipeline orchestration.

Implementation Guide:
---------------------
1. Instantiate TC_LOGIN_004_TestPage with Selenium WebDriver.
2. Call run_tc_login_004(valid_password, url) for end-to-end test.
3. Validate returned dict for stepwise results and error messages.
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

Future Considerations:
----------------------
- Parameterize URLs and error messages for multi-environment and multi-locale support.
- Extend for additional negative login scenarios (e.g., locked account, expired password).
- Integrate with test reporting frameworks for automated QA.
- Add retry logic and audit reporting.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

class TC_LOGIN_004_TestPage:
    """
    PageClass for Test Case TC-LOGIN-004: Empty email field, valid password.
    Implements steps as per test case and validates error handling.
    """
    def __init__(self, driver, timeout=10, locators_path="auto_scripts/Locators/Locators.json"):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        # Load locators
        with open(locators_path, "r") as f:
            locators_data = json.load(f)
            self.locators = locators_data.get("LoginPage", {})
        self.url = self.locators.get("url", "https://ecommerce.example.com/login")
        self.email_field = self.locators["inputs"].get("emailField", "id=login-email")
        self.password_field = self.locators["inputs"].get("passwordField", "id=login-password")
        self.login_button = self.locators["buttons"].get("loginSubmit", "id=login-submit")
        self.validation_error = self.locators["messages"].get("validationError", ".invalid-feedback")

    def go_to_login_page(self, url=None):
        self.driver.get(url or self.url)
        self.wait.until(EC.visibility_of_element_located((By.ID, self.email_field.split("=",1)[1])))

    def leave_email_empty(self):
        email_input = self.wait.until(EC.visibility_of_element_located((By.ID, self.email_field.split("=",1)[1])))
        email_input.clear()
        # Do not send any keys (leave empty)

    def enter_password(self, password):
        password_input = self.wait.until(EC.visibility_of_element_located((By.ID, self.password_field.split("=",1)[1])))
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, self.login_button.split("=",1)[1])))
        login_btn.click()

    def get_validation_error(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.validation_error)))
            return error_elem.text
        except TimeoutException:
            return None

    def is_on_login_page(self):
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, self.email_field.split("=",1)[1])))
            self.wait.until(EC.visibility_of_element_located((By.ID, self.password_field.split("=",1)[1])))
            return True
        except Exception:
            return False

    def run_tc_login_004(self, password, url=None):
        """
        Executes the TC-LOGIN-004 workflow:
        1. Navigate to login page
        2. Leave email field empty
        3. Enter valid password
        4. Click Login button
        5. Validate error is displayed and login is prevented
        Returns:
            dict: Stepwise results and validation messages
        """
        results = {
            "step_1_navigate_login": None,
            "step_2_leave_email_empty": None,
            "step_3_enter_password": None,
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
            # Step 2: Leave email field empty
            self.leave_email_empty()
            results["step_2_leave_email_empty"] = True
            # Step 3: Enter valid password
            self.enter_password(password)
            results["step_3_enter_password"] = True
            # Step 4: Click Login button
            self.click_login()
            results["step_4_click_login"] = True
            # Step 5: Validate error is displayed
            validation_error = self.get_validation_error()
            results["step_5_validation_error"] = validation_error
            # Step 6: Validate login is prevented (still on login page)
            results["step_6_login_prevented"] = self.is_on_login_page()
            results["overall_pass"] = bool(validation_error) and results["step_6_login_prevented"]
        except Exception as e:
            results["exception"] = f"Test flow failed: {str(e)}"
        return results
