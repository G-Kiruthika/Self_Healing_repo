from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PageClasses.LoginPage import LoginPage
from PageClasses.UsernameRecoveryPage import UsernameRecoveryPage

class TC_102_TestPage:
    '''
    Test Case TC-102 (testCaseId: 1443): End-to-end Login and Username Recovery scenario.
    This PageClass implements a comprehensive test scenario based on available locators and workflow patterns.
    '''

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.login_page = LoginPage(driver, timeout)
        self.username_recovery_page = UsernameRecoveryPage(driver, timeout)

    def run_tc_102(self, valid_email, valid_password, recovery_email):
        '''
        Executes the following scenario:
        1. Navigate to login page.
        2. Attempt login with valid credentials and verify dashboard.
        3. Log out (if possible) and return to login page.
        4. Click 'Forgot Username' and recover username.
        5. Validate recovery success message.
        6. Attempt login with empty fields and validate prompt.
        7. Attempt login with invalid credentials and validate error.
        '''
        results = {}

        # Step 1: Navigate to login page
        self.login_page.go_to_login_page()
        results['on_login_page'] = self.login_page.is_on_login_page()

        # Step 2: Attempt login with valid credentials
        self.login_page.enter_email(valid_email)
        self.login_page.enter_password(valid_password)
        self.login_page.click_login()
        try:
            dashboard_header = self.wait.until(
                EC.visibility_of_element_located(LoginPage.DASHBOARD_HEADER)
            )
            results['dashboard_header'] = dashboard_header.text
            results['login_success'] = True
        except Exception:
            results['login_success'] = False

        # Step 3: Log out and return to login page (if log out implemented, else skip)
        # For demonstration, navigate back to login page
        self.login_page.go_to_login_page()

        # Step 4: Click 'Forgot Username' and recover username
        self.login_page.click_forgot_username()
        recovery_result = self.username_recovery_page.recover_username(recovery_email)
        results['recovery_result'] = recovery_result

        # Step 5: Validate recovery success message
        if 'success' in recovery_result.lower():
            results['recovery_success'] = True
        else:
            results['recovery_success'] = False

        # Step 6: Attempt login with empty fields and validate prompt
        self.login_page.go_to_login_page()
        self.login_page.enter_email('')
        self.login_page.enter_password('')
        self.login_page.click_login()
        try:
            empty_prompt = self.wait.until(
                EC.visibility_of_element_located(LoginPage.EMPTY_FIELD_PROMPT)
            )
            results['empty_field_prompt'] = empty_prompt.text
        except Exception:
            results['empty_field_prompt'] = None

        # Step 7: Attempt login with invalid credentials and validate error
        invalid_email = "invalid@example.com"
        invalid_password = "wrongpass"
        self.login_page.login_with_credentials(invalid_email, invalid_password)
        error_msg = self.login_page.get_error_message()
        results['invalid_login_error'] = error_msg

        return results

    def validate_tc_102(self, valid_email, valid_password, recovery_email):
        '''
        High-level validation method for TC-102 workflow.
        Returns True if all steps pass, else False.
        '''
        results = self.run_tc_102(valid_email, valid_password, recovery_email)
        assert results['on_login_page'], "Not on login page initially"
        assert results['login_success'], "Valid login failed"
        assert results['recovery_success'], "Username recovery failed"
        assert results['empty_field_prompt'] is not None, "Empty field prompt missing"
        assert results['invalid_login_error'] is not None, "Invalid login error missing"
        return True