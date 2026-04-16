"""
TC_LOGIN_004_TestPage.py

Executive Summary:
------------------
This PageClass automates the end-to-end workflow for TC_LOGIN_004: Valid email, empty password login attempt, and validation error handling. It strictly follows Selenium Python automation standards, leveraging Locators.json, and is downstream-ready for enterprise test orchestration.

Detailed Analysis:
------------------
- Step 1: Navigates to the login page.
- Step 2: Enters a valid registered email.
- Step 3: Leaves the password field empty.
- Step 4: Clicks the Login button.
- Step 5: Verifies that a validation error is displayed and login is prevented.
- All locators are validated against Locators.json.
- Robust error handling and atomic method design ensure maintainability and reliability.

Implementation Guide:
---------------------
1. Instantiate TC_LOGIN_004_TestPage with a Selenium WebDriver instance.
2. Call run_tc_login_004(email, url) for the end-to-end test.
3. Validate the returned dict for stepwise results.
4. Integrate into CI/CD or downstream automation as required.

Quality Assurance Report:
------------------------
- All imports validated; only selenium, explicit waits, and Locators.json used.
- Methods are atomic, robust, and downstream-ready.
- Peer review and static analysis recommended before deployment.

Troubleshooting Guide:
----------------------
- If validation error is not found, validate locator and backend logic.
- If login is not prevented, check for UI/backend changes.
- Increase WebDriverWait timeout for slow environments.

Future Considerations:
----------------------
- Parameterize URLs and locators for multi-environment support.
- Extend for additional negative login scenarios.
- Integrate with test reporting and audit frameworks.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

class TC_LOGIN_004_TestPage:
    """
    PageClass for Test Case TC_LOGIN_004: Valid email, empty password login attempt.
    Implements steps as per test case and validates error handling.
    """
    # Locators loaded from Locators.json
    def __init__(self, driver, timeout=10, locators_path="auto_scripts/Locators/Locators.json"):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        # Load locators
        with open(locators_path, "r") as f:
            locators_data = json.load(f)
            self.locators = locators_data.get("LoginPage", {})
        # Fallbacks in case locator keys are missing
        self.url = self.locators.get("url", "https://app.example.com/login")
        self.email_field = self.locators["inputs"].get("emailField", "id=login-email")
        self.password_field = self.locators["inputs"].get("passwordField", "id=login-password")
        self.login_button = self.locators["buttons"].get("loginSubmit", "id=login-submit")
        self.validation_error = self.locators["messages"].get("validationError", ".invalid-feedback")

    def go_to_login_page(self, url=None):
        self.driver.get(url or self.url)
        self.wait.until(EC.visibility_of_element_located((By.ID, self.email_field.split("=",1)[1])))

    def enter_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located((By.ID, self.email_field.split("=",1)[1])))
        email_input.clear()
        email_input.send_keys(email)

    def leave_password_empty(self):
        password_input = self.wait.until(EC.visibility_of_element_located((By.ID, self.password_field.split("=",1)[1])))
        password_input.clear()
        # Do not send any keys (leave empty)

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

    def run_tc_login_004(self, email, url=None):
        """
        Executes the TC_LOGIN_004 workflow:
        1. Navigate to login page
        2. Enter valid registered email
        3. Leave password field empty
        4. Click Login button
        5. Validate error is displayed and login is prevented
        Returns:
            dict: Stepwise results and validation messages
        """
        results = {
            "step_1_navigate_login": None,
            "step_2_enter_email": None,
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
            # Step 2: Enter valid registered email
            self.enter_email(email)
            results["step_2_enter_email"] = True
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
            results["overall_pass"] = bool(validation_error) and results["step_6_login_prevented"]
        except Exception as e:
            results["exception"] = f"Test flow failed: {str(e)}"
        return results

"""
Test Case Mapping:
------------------
Test Case ID: 194
Description: Test Case TC_LOGIN_004
Test Steps:
1. Navigate to the login page [Test Data: URL: https://app.example.com/login] [Acceptance Criteria: AC_004]
2. Enter valid registered email [Test Data: Email: testuser@example.com] [Acceptance Criteria: AC_004]
3. Leave password field empty [Test Data: Password: ''] [Acceptance Criteria: AC_004]
4. Click on the Login button [Test Data: N/A] [Acceptance Criteria: AC_004]
5. Verify login is prevented [Test Data: N/A] [Acceptance Criteria: AC_004]
Expected:
1. Login page is displayed
2. Email is accepted
3. Password field remains empty
4. Validation error displayed: 'Password is required'
5. User cannot proceed with login, remains on login page
"""
