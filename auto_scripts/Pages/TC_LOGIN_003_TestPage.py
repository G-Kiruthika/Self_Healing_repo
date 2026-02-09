from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage

class TC_LOGIN_003_TestPage:
    """
    Comprehensive PageClass for TC_LOGIN_003.
    Orchestrates the end-to-end test flow:
      1. Navigate to login screen
      2. Click on 'Forgot Username' link
      3. Recover username using UsernameRecoveryPage
    Returns structured results for downstream automation.
    """
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.login_page = LoginPage(driver, timeout)
        self.username_recovery_page = UsernameRecoveryPage(driver, timeout)

    def execute_tc_login_003(self, email):
        """
        Executes TC_LOGIN_003 end-to-end workflow.
        Args:
            email (str): Email address for username recovery
        Returns:
            dict: Structured results with step details, confirmation/error, and overall status
        """
        results = {
            "step_1_navigate_login": None,
            "step_2_forgot_username_clicked": None,
            "step_3_recovery_success": None,
            "confirmation_message": None,
            "error_message": None,
            "overall_pass": False,
            "exception": None
        }
        try:
            # Step 1: Navigate to login screen
            self.login_page.go_to_login_page()
            results["step_1_navigate_login"] = self.login_page.is_on_login_page()
            if not results["step_1_navigate_login"]:
                results["exception"] = "Login screen not displayed."
                return results

            # Step 2: Click 'Forgot Username' link
            try:
                self.login_page.click_forgot_username()
                results["step_2_forgot_username_clicked"] = True
            except Exception as e:
                results["step_2_forgot_username_clicked"] = False
                results["exception"] = f"Failed to click 'Forgot Username': {str(e)}"
                return results

            # Step 3: Recover username
            try:
                # UsernameRecoveryPage expects to be on the recovery page
                self.username_recovery_page.enter_email(email)
                self.username_recovery_page.submit_recovery()
                confirmation = self.username_recovery_page.get_confirmation_message()
                error = self.username_recovery_page.get_error_message()
                if confirmation:
                    results["step_3_recovery_success"] = True
                    results["confirmation_message"] = confirmation
                    results["overall_pass"] = True
                else:
                    results["step_3_recovery_success"] = False
                    results["error_message"] = error
                    results["overall_pass"] = False
            except Exception as e:
                results["step_3_recovery_success"] = False
                results["exception"] = f"Recovery workflow failed: {str(e)}"
                return results

        except Exception as e:
            results["exception"] = f"Test flow failed: {str(e)}"
        return results