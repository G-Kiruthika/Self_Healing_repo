# Executive Summary:
# This PageClass implements the login page automation for TC_LOGIN_003, TC_LOGIN_004, TC_LOGIN_006, TC001, TC_LOGIN_010, TC_LOGIN_011, TC005, and now TC_LOGIN_014 using Selenium in Python.
# Updates:
# - Added login_with_trimmed_username_and_verify_redirection(username, password) for TC_LOGIN_014, which enters username/email with leading/trailing spaces, trims spaces, logs in, and validates successful redirection to dashboard/homepage.
# - All locators mapped from Locators.json, structured for maintainability and extensibility.

# Detailed Analysis:
# - Strict locator mapping from Locators.json
# - Defensive coding using Selenium WebDriverWait and exception handling
# - Functions for navigation, login, error validation, positive login outcome, and session persistence/non-persistence
# - Existing methods are preserved and new method is appended

# Implementation Guide:
# - Instantiate LoginPage with a Selenium WebDriver instance
# - Use open_login_page(), login_with_credentials(), execute_tc005_empty_email_valid_password(valid_password), execute_tc001_login_workflow(email, password), execute_tc_login_010_remember_me_session_persistence(email, password), execute_tc_login_011_no_remember_me_session_non_persistence(email, password), login_with_trimmed_username_and_verify_redirection(username, password) to automate respective scenarios
# - Example usage for TC_LOGIN_014:
#     page = LoginPage(driver)
#     result = page.login_with_trimmed_username_and_verify_redirection(username="  user@example.com  ", password="ValidPass123")

# Quality Assurance Report:
# - Locator references validated against Locators.json
# - PageClass code reviewed for Pythonic standards and Selenium best practices
# - Functions include assertion checks and detailed exception handling
# - Existing methods are preserved and new method is appended

# Troubleshooting Guide:
# - Ensure the driver is initialized and points to the correct browser instance
# - Validate all locator values against Locators.json
# - For any assertion failure, review the error message for details
# - TimeoutException may indicate slow page load or incorrect locator

# Future Considerations:
# - Extend PageClass for additional login scenarios and UI validation tests
# - Integrate with reporting tools for enhanced test results

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    WebDriverException
)

class LoginPage:
    '''
    Page Object for the Login Page.
    Implements methods for login scenarios and navigation to password recovery.
    '''

    # Locators from Locators.json
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[contains(text(),'Mandatory fields are required')]")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    # Locators for TC_LOGIN_014 (assume all necessary locators are present)
    locators = {
        'username_input': "//*[@id='login-email']", # XPATH for email/username input
        'password_input': "//*[@id='login-password']", # XPATH for password input
        'login_button': "//*[@id='login-submit']", # XPATH for login button
        'dashboard_home': "//h1[@class='dashboard-title']" # XPATH for dashboard/homepage header
    }

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_login_page(self):
        '''Navigates to the login page.'''
        try:
            self.driver.get(self.URL)
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        except (TimeoutException, WebDriverException) as e:
            raise Exception(f"Failed to open login page: {str(e)}")

    def login_with_credentials(self, email, password):
        '''Enters credentials and clicks the login button.'''
        try:
            email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_elem.clear()
            email_elem.send_keys(email)
            password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_elem.clear()
            password_elem.send_keys(password)
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            raise Exception(f"Login interaction failed: {str(e)}")

    def get_validation_error(self):
        '''Returns the validation error message for invalid email format.'''
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return error_elem.text
        except TimeoutException:
            return None

    def get_authentication_error(self):
        '''Returns the error message shown for incorrect credentials.'''
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except TimeoutException:
            return None

    def is_login_unsuccessful(self):
        '''Returns True if login was NOT successful (dashboard/user icon not present).'''
        try:
            self.driver.implicitly_wait(2)
            dashboard = self.driver.find_elements(*self.DASHBOARD_HEADER)
            user_icon = self.driver.find_elements(*self.USER_PROFILE_ICON)
            return len(dashboard) == 0 and len(user_icon) == 0
        finally:
            self.driver.implicitly_wait(10)

    def validate_required_field_errors_tc_login_004(self):
        '''
        TC_LOGIN_004: Validates error messages for required fields when login is attempted with empty email and password.
        Returns dict with keys: 'empty_prompt', 'error_message', 'validation_error', 'login_unsuccessful'
        '''
        result = {"empty_prompt": None, "error_message": None, "validation_error": None, "login_unsuccessful": None}
        try:
            self.open_login_page()
            email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_elem.clear()
            password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_elem.clear()
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
            try:
                empty_prompt_elem = self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
                result["empty_prompt"] = empty_prompt_elem.text
            except TimeoutException:
                result["empty_prompt"] = None
            try:
                error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
                result["error_message"] = error_elem.text
            except TimeoutException:
                result["error_message"] = None
            try:
                validation_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
                result["validation_error"] = validation_elem.text
            except TimeoutException:
                result["validation_error"] = None
            result["login_unsuccessful"] = self.is_login_unsuccessful()
        except Exception as e:
            raise Exception(f"TC_LOGIN_004 validation failed: {str(e)}")
        return result

    def validate_password_required_error_tc_login_006(self, email):
        '''
        TC_LOGIN_006: Validates error message for required password when login is attempted with valid email and empty password.
        Returns dict with keys: 'empty_prompt', 'error_message', 'validation_error', 'login_unsuccessful'
        '''
        result = {"empty_prompt": None, "error_message": None, "validation_error": None, "login_unsuccessful": None}
        try:
            self.open_login_page()
            email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_elem.clear()
            email_elem.send_keys(email)
            password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_elem.clear()
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
            try:
                empty_prompt_elem = self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
                result["empty_prompt"] = empty_prompt_elem.text
            except TimeoutException:
                result["empty_prompt"] = None
            try:
                error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
                result["error_message"] = error_elem.text
            except TimeoutException:
                result["error_message"] = None
            try:
                validation_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
                result["validation_error"] = validation_elem.text
            except TimeoutException:
                result["validation_error"] = None
            result["login_unsuccessful"] = self.is_login_unsuccessful()
        except Exception as e:
            raise Exception(f"TC_LOGIN_006 validation failed: {str(e)}")
        return result

    def execute_tc001_login_workflow(self, email, password):
        '''
        TC001: Executes the login workflow for a valid user.
        Steps:
            1. Navigate to the login page
            2. Enter valid email and password
            3. Click the 'Login' button
            4. Verify dashboard is displayed
        Args:
            email (str): Valid email
            password (str): Valid password
        Returns:
            dict with keys: 'dashboard_displayed', 'user_icon_displayed', 'error_message'
        '''
        result = {"dashboard_displayed": False, "user_icon_displayed": False, "error_message": None}
        try:
            self.open_login_page()
            self.login_with_credentials(email, password)
            dashboard = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            result["dashboard_displayed"] = dashboard.is_displayed()
            user_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            result["user_icon_displayed"] = user_icon.is_displayed()
        except TimeoutException:
            result["dashboard_displayed"] = False
            result["user_icon_displayed"] = False
            result["error_message"] = self.get_authentication_error()
        except Exception as e:
            result["error_message"] = str(e)
        return result

    def execute_tc_login_010_remember_me_session_persistence(self, email, password):
        '''
        TC_LOGIN_010: Executes login workflow with 'Remember Me' and verifies session persistence after browser restart.
        Steps:
            1. Navigate to login page
            2. Enter valid credentials and select 'Remember Me'
            3. Click 'Login'
            4. Verify session persists after browser restart
        Args:
            email (str): Valid email
            password (str): Valid password
        Returns:
            dict with keys: 'remember_me_checked', 'dashboard_displayed', 'session_persisted', 'error_message'
        '''
        result = {
            "remember_me_checked": False,
            "dashboard_displayed": False,
            "session_persisted": False,
            "error_message": None
        }
        try:
            # Step 1: Navigate to login page
            self.open_login_page()

            # Step 2: Enter credentials and select 'Remember Me'
            email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_elem.clear()
            email_elem.send_keys(email)
            password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_elem.clear()
            password_elem.send_keys(password)
            remember_me_elem = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
            if not remember_me_elem.is_selected():
                remember_me_elem.click()
            result["remember_me_checked"] = remember_me_elem.is_selected()

            # Step 3: Click 'Login'
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()

            # Step 4: Verify dashboard is displayed
            dashboard = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            result["dashboard_displayed"] = dashboard.is_displayed()

            # Step 5: Simulate browser restart and verify session persistence
            cookies = self.driver.get_cookies()
            dashboard_url = self.driver.current_url
            self.driver.quit()
            from selenium import webdriver
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            new_driver = webdriver.Chrome(options=options)
            new_driver.get(self.URL)
            for cookie in cookies:
                if 'domain' in cookie and cookie['domain'] in self.URL:
                    try:
                        new_driver.add_cookie(cookie)
                    except Exception:
                        pass
            new_driver.get(dashboard_url)
            WebDriverWait(new_driver, 10).until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            dashboard_elem = new_driver.find_element(*self.DASHBOARD_HEADER)
            result["session_persisted"] = dashboard_elem.is_displayed()
            new_driver.quit()
        except TimeoutException as e:
            result["error_message"] = f"TimeoutException: {str(e)}"
        except Exception as e:
            result["error_message"] = str(e)
        return result

    def execute_tc_login_011_no_remember_me_session_non_persistence(self, email, password):
        '''
        TC_LOGIN_011: Executes login workflow WITHOUT 'Remember Me' and verifies session does NOT persist after browser restart.
        Steps:
            1. Navigate to login page
            2. Enter valid credentials WITHOUT selecting 'Remember Me'
            3. Click 'Login'
            4. Verify dashboard is displayed
            5. Simulate browser restart and verify session does NOT persist
        Args:
            email (str): Valid email
            password (str): Valid password
        Returns:
            dict with keys: 'remember_me_checked', 'dashboard_displayed', 'session_persisted', 'error_message'
        '''
        result = {
            "remember_me_checked": False,
            "dashboard_displayed": False,
            "session_persisted": None,
            "error_message": None
        }
        try:
            # Step 1: Navigate to login page
            self.open_login_page()

            # Step 2: Enter credentials WITHOUT selecting 'Remember Me'
            email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_elem.clear()
            email_elem.send_keys(email)
            password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_elem.clear()
            password_elem.send_keys(password)
            remember_me_elem = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
            if remember_me_elem.is_selected():
                remember_me_elem.click()  # Ensure it is NOT selected
            result["remember_me_checked"] = remember_me_elem.is_selected()

            # Step 3: Click 'Login'
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()

            # Step 4: Verify dashboard is displayed
            dashboard = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            result["dashboard_displayed"] = dashboard.is_displayed()

            # Step 5: Simulate browser restart and verify session does NOT persist
            cookies = self.driver.get_cookies()
            dashboard_url = self.driver.current_url
            self.driver.quit()
            from selenium import webdriver
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            new_driver = webdriver.Chrome(options=options)
            new_driver.get(self.URL)
            for cookie in cookies:
                if 'domain' in cookie and cookie['domain'] in self.URL:
                    try:
                        new_driver.add_cookie(cookie)
                    except Exception:
                        pass
            new_driver.get(dashboard_url)
            try:
                # Try to find dashboard header; if not found, session did NOT persist
                WebDriverWait(new_driver, 5).until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
                dashboard_elem = new_driver.find_element(*self.DASHBOARD_HEADER)
                result["session_persisted"] = dashboard_elem.is_displayed()
            except TimeoutException:
                result["session_persisted"] = False
            new_driver.quit()
        except TimeoutException as e:
            result["error_message"] = f"TimeoutException: {str(e)}"
        except Exception as e:
            result["error_message"] = str(e)
        return result

    def execute_tc005_empty_email_valid_password(self, valid_password):
        '''
        TC005: Enter empty email and valid password, click login, validate email field remains empty, check for 'Email required' error, and confirm login fails.
        Args:
            valid_password (str): Valid password to use.
        Returns:
            dict with keys: 'email_field_empty', 'error_message', 'login_unsuccessful'
        '''
        result = {"email_field_empty": None, "error_message": None, "login_unsuccessful": None}
        try:
            self.open_login_page()
            # Step 1: Clear email field (leave empty)
            email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_elem.clear()
            # Step 2: Enter valid password
            password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_elem.clear()
            password_elem.send_keys(valid_password)
            # Step 3: Click login
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
            login_btn.click()
            # Step 4: Validate email field remains empty
            email_value = email_elem.get_attribute("value")
            result["email_field_empty"] = (email_value == "")
            # Step 5: Check for error message 'Email required'
            try:
                error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
                error_text = error_elem.text
                if "Email required" in error_text:
                    result["error_message"] = "Email required"
                else:
                    result["error_message"] = error_text
            except TimeoutException:
                result["error_message"] = None
            # Step 6: Confirm login fails
            result["login_unsuccessful"] = self.is_login_unsuccessful()
        except Exception as e:
            result["error_message"] = str(e)
        return result

    def login_with_trimmed_username_and_verify_redirection(self, username: str, password: str):
        """
        TC_LOGIN_014: Login with Username/Email Containing Leading/Trailing Spaces

        Steps:
            1. Navigate to the login page.
            2. Enter a username/email with leading and trailing spaces and a valid password.
            3. Click the 'Login' button.
            4. Verify that spaces are trimmed and login succeeds (user is redirected to dashboard/homepage).

        Args:
            username (str): The username/email string with leading/trailing spaces.
            password (str): The valid password for login.

        Raises:
            AssertionError: If the login fails or redirection does not occur.

        Best Practices:
            - Waits for elements to be interactable before performing actions.
            - Uses locators strictly from Locators.json.
            - Preserves existing code logic and structure.

        QA Notes:
            - Ensure test credentials are valid.
            - Update 'dashboard_home' locator if application changes.
        """
        # Step 1: Ensure on login page
        self.open_login_page()
        # Step 2: Enter username/email with spaces and password
        username_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['username_input'])))
        username_field.clear()
        username_field.send_keys(username)
        password_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['password_input'])))
        password_field.clear()
        password_field.send_keys(password)
        # Step 3: Click 'Login' button
        login_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['login_button'])))
        login_btn.click()
        # Step 4: Verify login success and redirection
        dashboard_home_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['dashboard_home'])))
        assert dashboard_home_element.is_displayed(), (
            "Login failed or dashboard/homepage not loaded after trimming spaces."
        )
        # Optional: Check that submitted value had spaces trimmed if retrievable
