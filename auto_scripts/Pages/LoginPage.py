from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import jwt
import datetime
from typing import Optional, Dict, Any
import requests

class LoginPage:
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to_login_page(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

    def enter_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def check_remember_me(self):
        checkbox = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
        if not checkbox.is_selected():
            checkbox.click()

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_btn.click()

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return None

    def is_on_login_page(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            return True
        except Exception:
            return False

    def login_with_remember_me(self, email, password):
        """
        Performs login with 'Remember Me' checked.
        """
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.check_remember_me()
        self.click_login()

    def verify_successful_login(self):
        """
        Verifies that dashboard header and user profile icon are displayed after login.
        """
        try:
            dashboard_header = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            user_profile_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return dashboard_header.is_displayed() and user_profile_icon.is_displayed()
        except Exception:
            return False

    def validate_remember_me_persistence(self, email, password):
        """
        TC_LOGIN_002 Step 5: Validates that the user remains logged in after closing and reopening the browser with 'Remember Me' checked.
        Steps:
            1. Perform login with 'Remember Me' checked.
            2. Verify successful login.
            3. Close browser.
            4. Reopen browser, navigate to the website.
            5. Validate user remains logged in (dashboard header and profile icon are visible).
        Returns:
            bool: True if user session persists after browser restart, False otherwise.
        """
        # Step 1-2: Login and verify
        self.login_with_remember_me(email, password)
        login_success = self.verify_successful_login()
        if not login_success:
            return False

        # Step 3: Close browser
        self.driver.quit()

        # Step 4: Reopen browser
        from selenium import webdriver
        driver_new = webdriver.Chrome()
        self.driver = driver_new
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(self.URL)

        # Step 5: Validate session persistence
        try:
            dashboard_header = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            user_profile_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return dashboard_header.is_displayed() and user_profile_icon.is_displayed()
        except Exception:
            return False

    # ... (rest of original methods preserved)
