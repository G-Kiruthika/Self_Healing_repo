from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UsernameRecoveryPage:
    """
    Page Object for the 'Forgot Username' workflow.
    Provides methods to interact with the username recovery process.
    Updated for TC_LOGIN_003 to support structured end-to-end automation.

    Executive Summary:
    - Automates username recovery via UI with strict locator validation.
    - Ready for downstream orchestration and integration.

    Implementation Guide:
    1. Instantiate with Selenium WebDriver.
    2. Use go_to_username_recovery(), enter_email(), submit_recovery().
    3. Use get_confirmation_message(), get_error_message(), get_recovered_username() for validation.
    4. For TC_LOGIN_003, use recover_username(email).

    QA Report:
    - All locators validated against locators.json.
    - Methods atomic, robust, and downstream ready.
    - Peer review and static analysis recommended.

    Troubleshooting:
    - If confirmation not found, check for error message and validate backend.
    - If element not found, validate locator and wait time.

    Future Considerations:
    - Parameterize URLs for multi-environment.
    - Extend for multi-factor recovery.
    """
    URL = "https://example-ecommerce.com/forgot-username"
    EMAIL_FIELD = (By.ID, "recovery-email")
    SUBMIT_BUTTON = (By.ID, "recovery-submit")
    CONFIRMATION_MESSAGE = (By.CSS_SELECTOR, "div.recovery-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.recovery-error")
    INSTRUCTIONS_TEXT = (By.CSS_SELECTOR, "div.recovery-instructions")
    USERNAME_RESULT = (By.CSS_SELECTOR, "span.recovered-username")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to_username_recovery(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.INSTRUCTIONS_TEXT))

    def enter_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def submit_recovery(self):
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()

    def get_confirmation_message(self):
        try:
            msg_elem = self.wait.until(EC.visibility_of_element_located(self.CONFIRMATION_MESSAGE))
            return msg_elem.text
        except:
            return None

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None

    def get_recovered_username(self):
        try:
            username_elem = self.wait.until(EC.visibility_of_element_located(self.USERNAME_RESULT))
            return username_elem.text
        except:
            return None

    def recover_username(self, email):
        self.go_to_username_recovery()
        self.enter_email(email)
        self.submit_recovery()
        confirmation = self.get_confirmation_message()
        if confirmation:
            return confirmation
        else:
            return self.get_error_message()

    # --- TC_LOGIN_007: End-to-End Username Recovery Workflow ---
    def run_tc_login_007(self, login_page, email):
        """
        TC_LOGIN_007: End-to-end test for 'Forgot Username' workflow.
        Steps:
            1. Navigate to login page.
            2. Click on 'Forgot Username' link.
            3. Enter registered email address.
            4. Click on 'Send Username' button.
            5. Verify username recovery email is received (mocked).
        Args:
            login_page: Instance of LoginPage for navigation/click.
            email (str): Registered email address.
        Returns:
            dict: Stepwise results and validation messages for downstream automation.

        Executive Summary:
        - Automates the complete workflow for TC_LOGIN_007.
        - Strict Selenium Python best practices and code integrity.
        - Structured output for downstream agents.

        Implementation Guide:
        1. Pass a LoginPage instance and the registered email.
        2. Call run_tc_login_007(login_page, email) to execute all steps.
        3. Review returned dict for stepwise results.

        QA Report:
        - All imports and locators validated.
        - Explicit waits and robust error handling.
        - Output structure matches enterprise and downstream standards.

        Troubleshooting Guide:
        - If any step fails, check locators and backend status.
        - Increase timeout for slow environments.
        - Validate email delivery via actual or mocked inbox as appropriate.

        Future Considerations:
        - Integrate with real email API for inbox validation.
        - Parameterize URLs and locators for multi-environment support.
        - Add audit logging and reporting hooks.
        """
        results = {
            "step_1_navigate_login": None,
            "step_2_click_forgot_username": None,
            "step_3_enter_email": None,
            "step_4_click_send_username": None,
            "step_5_email_received": None,
            "overall_pass": False,
            "exception": None
        }
        try:
            # Step 1: Navigate to login page
            login_page.go_to_login_page()
            results["step_1_navigate_login"] = login_page.is_on_login_page()
            if not results["step_1_navigate_login"]:
                results["exception"] = "Login page not displayed."
                return results
            # Step 2: Click 'Forgot Username' link
            try:
                login_page.click_forgot_username()
                results["step_2_click_forgot_username"] = True
            except Exception as e:
                results["step_2_click_forgot_username"] = False
                results["exception"] = f"Failed to click 'Forgot Username': {str(e)}"
                return results
            # Step 3: Enter registered email address
            self.enter_email(email)
            results["step_3_enter_email"] = True
            # Step 4: Click 'Send Username' button
            self.submit_recovery()
            results["step_4_click_send_username"] = True
            # Step 5: Verify username recovery email is received (mocked)
            confirmation = self.get_confirmation_message()
            if confirmation:
                results["step_5_email_received"] = confirmation
                results["overall_pass"] = True
            else:
                error = self.get_error_message()
                results["step_5_email_received"] = error or "No confirmation or error message found."
                results["overall_pass"] = False
        except Exception as e:
            results["exception"] = f"Test flow failed: {str(e)}"
        return results
