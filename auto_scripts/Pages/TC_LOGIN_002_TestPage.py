"""
TC_LOGIN_002_TestPage.py

Executive Summary:
------------------
This PageClass automates the end-to-end workflow for TC_LOGIN_002: invalid login attempt, error message validation, and page state check. It strictly adheres to Selenium Python standards, uses locators from Locators.json, and ensures atomicity for downstream orchestration.

Detailed Analysis:
------------------
- Step 1: Navigate to login page using Locators.json URL.
- Step 2: Enter invalid username and valid password from test data.
- Step 3: Click login button.
- Step 4: Validate error message ('Invalid username or password') and ensure user remains on login page.
- All methods are atomic, robust, and maintainable.

Implementation Guide:
---------------------
1. Instantiate TC_LOGIN_002_TestPage with Selenium WebDriver.
2. Call run_tc_login_002() with invalid credentials to execute all steps.
3. Review returned results for validation.

Quality Assurance Report:
-------------------------
- All imports validated; uses selenium, Locators.json, and standard Python modules.
- Exception handling ensures atomic failure reporting.
- Output structure matches downstream requirements.
- Peer review and static analysis recommended before deployment.

Troubleshooting Guide:
----------------------
- If locators fail, validate against Locators.json and UI.
- If error message not found, check application logic and test data.
- If user is redirected, validate backend authentication logic.
- Increase WebDriverWait for slow environments.

Future Considerations:
----------------------
- Parameterize credentials for broader negative testing.
- Extend for multi-environment and multi-browser support.
- Integrate with test reporting frameworks for automated QA.
- Add retry logic and audit reporting.
"""

import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

class TC_LOGIN_002_TestPage:
    """
    Page Object for TC_LOGIN_002: Invalid Login Attempt
    Implements all steps from the test case with strict Selenium Python standards.
    """
    def __init__(self, driver, locators_path='auto_scripts/Locators/Locators.json', timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout
        # Load locators from Locators.json
        with open(locators_path, 'r') as f:
            locators = json.load(f)["LoginPage"]
        self.login_url = locators["url"]
        self.email_locator = self._parse_locator(locators["inputs"]["emailField"])
        self.password_locator = self._parse_locator(locators["inputs"]["passwordField"])
        self.login_button_locator = self._parse_locator(locators["buttons"]["loginSubmit"])
        self.error_message_locator = self._parse_locator(locators["messages"]["errorMessage"])

    def _parse_locator(self, locator_str):
        if locator_str.startswith("id="):
            return (By.ID, locator_str.split("=", 1)[1])
        elif locator_str.startswith("css=") or locator_str.startswith("."):
            return (By.CSS_SELECTOR, locator_str.split("=", 1)[1] if "=" in locator_str else locator_str)
        elif locator_str.startswith("xpath="):
            return (By.XPATH, locator_str.split("=", 1)[1])
        elif locator_str.startswith("text="):
            return (By.XPATH, f"//*[contains(text(), '{locator_str.split('=', 1)[1]}')]")
        else:
            return (By.CSS_SELECTOR, locator_str)

    def navigate_to_login_page(self):
        self.driver.get(self.login_url)
        self.wait.until(EC.visibility_of_element_located(self.email_locator))
        return True

    def enter_username(self, username):
        username_field = self.driver.find_element(*self.email_locator)
        username_field.clear()
        username_field.send_keys(username)
        return True

    def enter_password(self, password):
        password_field = self.driver.find_element(*self.password_locator)
        password_field.clear()
        password_field.send_keys(password)
        return True

    def click_login(self):
        login_button = self.driver.find_element(*self.login_button_locator)
        login_button.click()
        return True

    def validate_error_message(self, expected_error):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.error_message_locator))
            error_text = error_elem.text.strip()
            assert expected_error in error_text, f"Error message mismatch: {error_text}"
            return True
        except (NoSuchElementException, TimeoutException, AssertionError) as e:
            return False

    def verify_remain_on_login_page(self):
        current_url = self.driver.current_url
        on_login_page = current_url.startswith(self.login_url)
        return on_login_page

    def run_tc_login_002(self, username, password):
        results = {}
        try:
            results['step_1_navigate'] = self.navigate_to_login_page()
            results['step_2_enter_username'] = self.enter_username(username)
            results['step_3_enter_password'] = self.enter_password(password)
            results['step_4_click_login'] = self.click_login()
            results['step_5_error_message_validated'] = self.validate_error_message('Invalid username or password')
            results['step_6_remain_on_login_page'] = self.verify_remain_on_login_page()
            results['overall_pass'] = all([
                results['step_1_navigate'],
                results['step_2_enter_username'],
                results['step_3_enter_password'],
                results['step_4_click_login'],
                results['step_5_error_message_validated'],
                results['step_6_remain_on_login_page']
            ])
        except Exception as e:
            results['overall_pass'] = False
            results['error'] = str(e)
        return results
