# LoginPage.py
# Automated PageClass for TC_LOGIN_001: End-to-end login workflow
# Covers navigation, input, login action, and post-login validation

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://example-ecommerce.com/login'
        self.email_field = (By.ID, 'login-email')
        self.password_field = (By.ID, 'login-password')
        self.remember_me_checkbox = (By.ID, 'remember-me')
        self.login_submit = (By.ID, 'login-submit')
        self.forgot_password_link = (By.CSS_SELECTOR, 'a.forgot-password-link')
        self.error_message = (By.CSS_SELECTOR, 'div.alert-danger')
        self.validation_error = (By.CSS_SELECTOR, '.invalid-feedback')
        self.empty_field_prompt = (By.XPATH, "//*[text()='Mandatory fields are required']")
        self.dashboard_header = (By.CSS_SELECTOR, 'h1.dashboard-title')
        self.user_profile_icon = (By.CSS_SELECTOR, '.user-profile-name')

    def navigate(self):
        """
        Step 1: Navigate to the login page
        """
        self.driver.get(self.url)
        assert self.driver.find_element(*self.email_field).is_displayed(), 'Email field not displayed'
        assert self.driver.find_element(*self.password_field).is_displayed(), 'Password field not displayed'

    def enter_email(self, email):
        """
        Step 2: Enter valid username
        """
        email_input = self.driver.find_element(*self.email_field)
        email_input.clear()
        email_input.send_keys(email)
        assert email_input.get_attribute('value') == email, 'Email not entered correctly'

    def enter_password(self, password):
        """
        Step 3: Enter valid password
        """
        password_input = self.driver.find_element(*self.password_field)
        password_input.clear()
        password_input.send_keys(password)
        # Password field should be masked
        assert password_input.get_attribute('type') == 'password', 'Password field is not masked'
        assert password_input.get_attribute('value') == password, 'Password not entered correctly'

    def click_login(self):
        """
        Step 4: Click on the Login button
        """
        self.driver.find_element(*self.login_submit).click()

    def validate_post_login(self):
        """
        Validate successful login: dashboard and session
        """
        # Wait for dashboard header
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.dashboard_header)
        )
        assert self.driver.find_element(*self.dashboard_header).is_displayed(), 'Dashboard header not visible'
        assert self.driver.find_element(*self.user_profile_icon).is_displayed(), 'User profile icon not visible'

    def login(self, email, password):
        """
        Complete login workflow for TC_LOGIN_001
        """
        self.navigate()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        self.validate_post_login()

    # Additional validation methods for negative scenarios
    def get_error_message(self):
        try:
            return self.driver.find_element(*self.error_message).text
        except NoSuchElementException:
            return None

    def get_validation_error(self):
        try:
            return self.driver.find_element(*self.validation_error).text
        except NoSuchElementException:
            return None

    def is_empty_field_prompt_displayed(self):
        try:
            return self.driver.find_element(*self.empty_field_prompt).is_displayed()
        except NoSuchElementException:
            return False

# Example usage:
# from selenium import webdriver
# driver = webdriver.Chrome()
# login_page = LoginPage(driver)
# login_page.login('validuser@example.com', 'ValidPass123!')
# print('TC_LOGIN_001: PASSED - User redirected to dashboard and session established')
