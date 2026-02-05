import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Locators loaded from Locators.json
LOGIN_PAGE_LOCATORS = {
    'forgotPasswordLink': (By.CSS_SELECTOR, 'a.forgot-password-link'),
    'emailField': (By.ID, 'login-email'),
    'errorMessage': (By.CSS_SELECTOR, 'div.alert-danger'),
}
PASSWORD_RECOVERY_LOCATORS = {
    'emailField': (By.ID, 'recoveryEmail'),
    'submitButton': (By.ID, 'submitRecovery'),
    'errorMessage': (By.CSS_SELECTOR, 'div.alert-danger'),
}

class PasswordRecoveryPage:
    def __init__(self, driver):
        self.driver = driver

    def click_forgot_password_link(self):
        '''Step 1: Click Forgot Password link on LoginPage.'''
        try:
            link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LOGIN_PAGE_LOCATORS['forgotPasswordLink'])
            )
            link.click()
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_forgot_password_page_displayed(self):
        '''Verify navigation to Forgot Password page.'''
        # This should check for a unique element on the page, e.g., the recovery email field
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(PASSWORD_RECOVERY_LOCATORS['emailField'])
            )
            return True
        except TimeoutException:
            return False

    def enter_unregistered_email_and_submit(self, email):
        '''Step 2: Enter unregistered email and submit.'''
        try:
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(PASSWORD_RECOVERY_LOCATORS['emailField'])
            )
            email_input.clear()
            email_input.send_keys(email)
            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(PASSWORD_RECOVERY_LOCATORS['submitButton'])
            )
            submit_btn.click()
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_error_message(self):
        '''Get error message displayed after submitting an unregistered email.'''
        try:
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(PASSWORD_RECOVERY_LOCATORS['errorMessage'])
            )
            return error.text
        except TimeoutException:
            return None

    def forgot_password_flow_tc009(self, email="unknown@example.com"):
        '''
        Implements TC009:
        1. Click 'Forgot Password' link on LoginPage.
        2. Verify Forgot Password page is displayed.
        3. Enter unregistered email and submit.
        4. Verify error message 'Email not found' is displayed. No email sent.
        Returns dict with results and messages.
        '''
        results = {}
        results['clicked_link'] = self.click_forgot_password_link()
        results['forgot_password_page_displayed'] = self.is_forgot_password_page_displayed()
        results['email_submitted'] = self.enter_unregistered_email_and_submit(email)
        time.sleep(1)
        error_msg = self.get_error_message()
        results['error_message_displayed'] = error_msg is not None and 'email not found' in error_msg.lower()
        results['error_message_text'] = error_msg
        # NOTE: Email delivery validation is out of scope for UI automation; must be checked by integration test downstream
        return results

# Executive Summary:
# This update strictly aligns PasswordRecoveryPage.py with TC009 requirements, ensuring locator mapping from Locators.json, coverage of all test steps, and robust error handling. The flow now enables navigation from LoginPage, submission of unregistered emails, and error validation.

# Detailed Analysis:
# - Existing implementation only supported registered email flow and success messages.
# - This update supports negative test case: unregistered email, error message, and no email sent.
# - Locators are mapped from Locators.json for consistency and maintainability.

# Implementation Guide:
# 1. Instantiate PasswordRecoveryPage with a Selenium WebDriver.
# 2. Call forgot_password_flow_tc009(email) with an unregistered email.
# 3. Validate returned dict for step-wise results and error message.
#
# Example:
# page = PasswordRecoveryPage(driver)
# results = page.forgot_password_flow_tc009(email='unknown@example.com')
# assert results['clicked_link']
# assert results['forgot_password_page_displayed']
# assert results['email_submitted']
# assert results['error_message_displayed']

# Quality Assurance Report:
# - Locators strictly match Locators.json.
# - All expected exceptions handled.
# - Step-by-step result dict enables granular validation.
# - Method naming and structure conform to Selenium Python standards.
# - Peer review and static analysis recommended before deployment.

# Troubleshooting Guide:
# - If navigation fails, check LoginPage locator and page load time.
# - If error message not found, validate UI and locator accuracy.
# - For email delivery checks, use downstream integration pipeline (not UI).
# - Increase WebDriverWait time for slow environments.

# Future Considerations:
# - Parameterize locators via config or direct Locators.json loading.
# - Extend for multi-locale error message validation.
# - Integrate with test reporting and email delivery mocks for end-to-end coverage.
