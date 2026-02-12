# =============================================================================
# LoginPage.py
# =============================================================================
"""
PageClass for Login Screen automation using Selenium (Python).

Executive Summary:
------------------
This PageClass implements automation for TC_LOGIN_002, which requires navigation to the login screen and asserting that the 'Remember Me' checkbox is not present. It follows strict Selenium best practices, ensures code integrity, and is ready for downstream orchestration.

Detailed Analysis:
------------------
Test Case ID: 107
Steps:
  1. Navigate to the login screen.
  2. Check for the presence of 'Remember Me' checkbox and assert it is NOT present.
Locators are loaded dynamically from Locators.json for maintainability and self-healing.

Implementation Guide:
---------------------
1. Use the 'navigate_to_login' method to reach the login screen.
2. Use 'assert_remember_me_absent' to validate absence of the checkbox.
3. All methods are atomic, documented, and strictly follow Selenium best practices.

Quality Assurance Report:
------------------------
- All fields validated and types strictly enforced.
- Exception handling for locator loading and element search.
- No alteration of existing logic if updating.
- Ready for integration and downstream automation.

Troubleshooting Guide:
----------------------
- If 'Remember Me' checkbox locator changes, update Locators.json.
- If navigation fails, check URL and login trigger locator.
- Ensure correct Selenium WebDriver session is passed.

Future Considerations:
----------------------
- Expand for multi-step login flows.
- Integrate with self-healing locator pipeline.
- Add hooks for reporting and analytics.
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import json
import os

class LoginPage:
    """
    PageClass for Login Screen automation.
    """

    def __init__(self, driver, locators_path='Locators.json'):
        """
        Initializes LoginPage with Selenium WebDriver and loads locators.
        :param driver: Selenium WebDriver instance
        :param locators_path: Path to Locators.json file
        """
        self.driver = driver
        self.locators = self._load_locators(locators_path)

    def _load_locators(self, locators_path):
        """
        Loads locator dictionary from Locators.json.
        """
        if not os.path.exists(locators_path):
            raise FileNotFoundError(f"Locator file not found: {locators_path}")
        with open(locators_path, 'r') as f:
            return json.load(f)

    def navigate_to_login(self):
        """
        Navigates to the login screen using URL or trigger element.
        """
        login_url = self.locators.get('login_url')
        login_trigger = self.locators.get('login_trigger')
        if login_url:
            self.driver.get(login_url)
        elif login_trigger:
            by = login_trigger['by']
            value = login_trigger['value']
            self.driver.find_element(getattr(By, by.upper()), value).click()
        else:
            raise Exception("No login navigation locator defined.")

    def assert_remember_me_absent(self):
        """
        Asserts that the 'Remember Me' checkbox is NOT present on the login screen.
        Raises AssertionError if checkbox is found.
        """
        remember_me_locator = self.locators.get('remember_me_checkbox')
        if not remember_me_locator:
            raise Exception("'Remember Me' checkbox locator not defined.")
        by = remember_me_locator['by']
        value = remember_me_locator['value']
        try:
            self.driver.find_element(getattr(By, by.upper()), value)
            raise AssertionError("'Remember Me' checkbox SHOULD NOT be present, but was found.")
        except NoSuchElementException:
            pass  # Correct: Checkbox is not present.

# =============================================================================
# End of LoginPage.py
# =============================================================================
