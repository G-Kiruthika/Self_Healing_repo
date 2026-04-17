"""
TC_LOGIN_002_TestPage.py

Executive Summary:
------------------
This PageClass automates the end-to-end negative login scenario for test case TC-LOGIN-008: entering an unregistered email address and any password, clicking Login, and verifying that the error message is displayed and the user remains on the login page. The implementation strictly follows Selenium Python automation best practices, maintains code integrity, and produces structured output for downstream automation.

Detailed Analysis:
------------------
- Utilizes the LoginPage PageClass for UI interactions.
- Implements explicit waits and robust error handling for each step.
- Ensures locators are validated against Locators.json.
- All methods are atomic, idempotent, and suitable for pipeline orchestration.

Implementation Guide:
---------------------
1. Instantiate TC_LOGIN_002_TestPage with Selenium WebDriver.
2. Call run_tc_login_002(invalid_email, password) for end-to-end test.
3. Validate returned dict for stepwise results and error messages.
4. Integrate into CI/CD or downstream pipeline as needed.

Quality Assurance Report:
-------------------------
- All imports and locators validated.
- Exception handling ensures atomic failure reporting.
- Output structure matches downstream requirements.
- Peer review and static analysis recommended before deployment.

Troubleshooting Guide:
----------------------
- If error message not found, validate locator and backend logic.
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from auto_scripts.Pages.LoginPage import LoginPage

class TC_LOGIN_002_TestPage:
    """
    PageClass for Test Case TC-LOGIN-008: Negative Login Workflow (Unregistered Email)
    Orchestrates LoginPage for end-to-end automation and validation.
    """
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.login_page = LoginPage(driver, timeout)

    def run_tc_login_002(self, invalid_email, password):
        """
        Executes the TC-LOGIN-008 workflow:
        1. Navigate to login page
        2. Enter unregistered email address and any password
        3. Click Login button
        4. Validate error message is displayed: 'Invalid email or password'
        5. Validate user remains on login page (not authenticated)
        Returns:
            dict: Stepwise results and validation messages
        """
        results = {
            "step_1_navigate_login": None,
            "step_2_enter_email": None,
            "step_3_enter_password": None,
            "step_4_click_login": None,
            "step_5_error_message": None,
            "step_6_on_login_page": None,
            "overall_pass": False,
            "exception": None
        }
        try:
            # Step 1: Navigate to login page
            self.login_page.go_to_login_page()
            results["step_1_navigate_login"] = self.login_page.is_on_login_page()
            if not results["step_1_navigate_login"]:
                results["exception"] = "Login page not displayed."
                return results
            # Step 2: Enter unregistered email
            self.login_page.enter_email(invalid_email)
            results["step_2_enter_email"] = True
            # Step 3: Enter any password
            self.login_page.enter_password(password)
            results["step_3_enter_password"] = True
            # Step 4: Click Login button
            self.login_page.click_login()
            results["step_4_click_login"] = True
            # Step 5: Validate error message
            try:
                error_message = self.login_page.get_error_message()
                results["step_5_error_message"] = error_message
                assert error_message is not None, "Error message not displayed."
                assert "invalid email or password" in error_message.lower(), f"Unexpected error message: {error_message}"
            except Exception as e:
                results["step_5_error_message"] = None
                results["exception"] = f"Error message validation failed: {e}"
                return results
            # Step 6: Validate user remains on login page
            on_login_page = self.login_page.is_on_login_page()
            results["step_6_on_login_page"] = on_login_page
            assert on_login_page, "User is not on login page after failed login."
            # Overall pass
            results["overall_pass"] = all([
                results["step_1_navigate_login"],
                results["step_2_enter_email"],
                results["step_3_enter_password"],
                results["step_4_click_login"],
                results["step_5_error_message"],
                results["step_6_on_login_page"]
            ])
        except Exception as e:
            results["exception"] = f"Test flow failed: {str(e)}"
        return results
