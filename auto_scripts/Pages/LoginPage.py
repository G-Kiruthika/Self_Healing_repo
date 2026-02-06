from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators from Locators.json
        self.url = "https://example-ecommerce.com/login"
        self.email_field = (By.ID, "login-email")
        self.password_field = (By.ID, "login-password")
        self.remember_me_checkbox = (By.ID, "remember-me")
        self.login_submit = (By.ID, "login-submit")
        self.forgot_password_link = (By.CSS_SELECTOR, "a.forgot-password-link")
        self.error_message = (By.CSS_SELECTOR, "div.alert-danger")
        self.validation_error = (By.CSS_SELECTOR, ".invalid-feedback")
        self.empty_field_prompt = (By.XPATH, "//*[text()='Mandatory fields are required']")
        self.dashboard_header = (By.CSS_SELECTOR, "h1.dashboard-title")
        self.user_profile_icon = (By.CSS_SELECTOR, ".user-profile-name")

    def navigate_to_login_screen(self):
        self.driver.get(self.url)
        assert self.driver.find_element(*self.email_field).is_displayed(), "Login screen is not displayed."

    def login_with_invalid_credentials(self, username, password):
        self.driver.find_element(*self.email_field).clear()
        self.driver.find_element(*self.email_field).send_keys(username)
        self.driver.find_element(*self.password_field).clear()
        self.driver.find_element(*self.password_field).send_keys(password)
        self.driver.find_element(*self.login_submit).click()

    def verify_invalid_login_error(self, expected_message="Invalid username or password. Please try again."):
        error_elem = self.driver.find_element(*self.error_message)
        assert error_elem.is_displayed(), "Error message is not displayed."
        actual_message = error_elem.text
        assert expected_message in actual_message, f"Expected error message '{expected_message}' but got '{actual_message}'."

    # Optional: Additional validation methods
    def verify_empty_field_prompt(self):
        prompt_elem = self.driver.find_element(*self.empty_field_prompt)
        assert prompt_elem.is_displayed(), "Empty field prompt is not displayed."

    def verify_validation_error(self):
        validation_elem = self.driver.find_element(*self.validation_error)
        assert validation_elem.is_displayed(), "Validation error is not displayed."

# Example usage for TC_LOGIN_001:
# driver = webdriver.Chrome()
# login_page = LoginPage(driver)
# login_page.navigate_to_login_screen()
# login_page.login_with_invalid_credentials("invalid_user", "invalid_pass")
# login_page.verify_invalid_login_error()
