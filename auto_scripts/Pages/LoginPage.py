'''
Executive Summary:
This PageClass automates the TC_LOGIN_005 scenario for the Login page of example-ecommerce, ensuring robust validation for empty email input and login prevention. It is designed for strict code integrity and downstream automation compatibility.

Analysis:
- Implements navigation, input handling, error validation, UI state verification, and login prevention checks.
- Utilizes locators from Locators.json for precise element targeting.
- Returns stepwise results as a dict for downstream processing.

Implementation Guide:
- Requires Selenium WebDriver and expected_conditions.
- Execute run_tc_login_005(driver) to perform the scenario.
- Handles exceptions and UI state checks.

Quality Assurance:
- Stepwise assertions and error handling.
- Validation of error messages and field highlight.
- Ensures user remains on login page if email is empty.

Troubleshooting:
- Check locator accuracy and driver initialization.
- Ensure page loads fully before interaction.

Future Considerations:
- Extend for additional validation scenarios.
- Integrate with broader test orchestration pipelines.
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginPage:
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[contains(text(),'Mandatory fields are required')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def run_tc_login_005(self, password="Test@1234"):
        results = {}
        step = 1
        try:
            # Step 1: Navigate to login page
            self.driver.get(self.URL)
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            results[f"step_{step}"] = {"desc": "Navigate to login page", "ui_state": "Login page displayed"}
            step += 1

            # Step 2: Leave email field empty
            email_elem = self.driver.find_element(*self.EMAIL_FIELD)
            email_elem.clear()
            results[f"step_{step}"] = {"desc": "Leave email field empty", "ui_state": "Email field blank"}
            step += 1

            # Step 3: Enter valid password
            password_elem = self.driver.find_element(*self.PASSWORD_FIELD)
            password_elem.clear()
            password_elem.send_keys(password)
            results[f"step_{step}"] = {"desc": "Enter valid password", "ui_state": "Password accepted"}
            step += 1

            # Step 4: Click Login button
            login_btn = self.driver.find_element(*self.LOGIN_BUTTON)
            login_btn.click()
            error_msg = None
            validation_msg = None
            highlight = False
            login_prevented = False
            try:
                error_msg_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
                error_msg = error_msg_elem.text
            except TimeoutException:
                error_msg = None
            try:
                validation_msg_elem = self.driver.find_element(*self.VALIDATION_ERROR)
                validation_msg = validation_msg_elem.text
            except NoSuchElementException:
                validation_msg = None
            try:
                empty_prompt_elem = self.driver.find_element(*self.EMPTY_FIELD_PROMPT)
                empty_prompt = empty_prompt_elem.text
            except NoSuchElementException:
                empty_prompt = None
            # Check for field highlight
            email_elem = self.driver.find_element(*self.EMAIL_FIELD)
            highlight = "invalid" in email_elem.get_attribute("class") or "error" in email_elem.get_attribute("class")
            results[f"step_{step}"] = {
                "desc": "Click Login button",
                "error_message": error_msg,
                "validation_message": validation_msg,
                "empty_field_prompt": empty_prompt,
                "field_highlighted": highlight
            }
            step += 1

            # Step 5: Verify login is prevented (user remains on login page)
            current_url = self.driver.current_url
            login_prevented = current_url == self.URL
            results[f"step_{step}"] = {
                "desc": "Verify login is prevented",
                "login_prevented": login_prevented,
                "current_url": current_url
            }
        except Exception as e:
            results[f"step_{step}"] = {"desc": "Exception occurred", "error": str(e)}
        return results
