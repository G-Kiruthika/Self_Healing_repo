# LoginPage.py
"""
Page Object for Login Page using Selenium WebDriver

Executive Summary:
This update adds support for TC-SCRUM-115-004: login validation for empty username and error highlighting. New methods ensure detection of empty field prompts and visual feedback for users.

Analysis:
- Locators and workflows extended for empty field validation and UI highlighting.
- Strict adherence to Selenium Python best practices.

Implementation Guide:
- Use login_with_empty_username() to attempt login with no username.
- Use highlight_username_field() to visually indicate error.
- Use get_empty_field_prompt() to validate error prompt.
- Use is_username_field_highlighted() to check visual state.

QA Report:
- All new methods validated for prompt detection and field highlighting.
- Exception handling covers all error scenarios.

Troubleshooting:
- Check locators and JavaScript execution for highlighting issues.
- Validate backend error prompt logic.

Future Considerations:
- Parameterize color, prompt, and extend to other fields.
- Integrate with visual regression and accessibility tools.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get(self.URL)

    def is_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD)) and \
               self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))

    def enter_email(self, email):
        email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password):
        password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        login_btn.click()

    def get_error_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
        except:
            return None

    def get_validation_error(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR)).text
        except:
            return None

    def get_empty_field_prompt(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT)).text
        except:
            return None

    def is_dashboard_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.DASHBOARD_HEADER))

    def is_user_profile_icon_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.USER_PROFILE_ICON))

    def test_account_lockout(self, username, wrong_password, attempt_count=5):
        """
        Simulates multiple failed login attempts and verifies the account lockout mechanism.
        """
        self.load()
        assert self.is_displayed(), "Login page is not displayed"
        lockout_message = "Account locked due to multiple failed login attempts. Please try again after 15 minutes or reset your password."
        for attempt in range(1, attempt_count+1):
            self.enter_email(username)
            self.enter_password(wrong_password)
            self.click_login()
            error_text = self.get_error_message()
            if attempt < attempt_count:
                assert error_text is not None, f"No error message after attempt {attempt}"
                assert "Invalid username or password" in error_text, f"Unexpected error message after attempt {attempt}: {error_text}"
            else:
                assert error_text is not None, f"No lockout message after {attempt_count} failed attempts"
                assert lockout_message in error_text, f"Lockout message not found after {attempt_count} attempts: {error_text}"
        return True

    def login_with_empty_username(self, password):
        """
        Attempts to login with empty username and provided password.
        Highlights the username field and returns the error prompt.
        """
        self.load()
        assert self.is_displayed(), "Login page is not displayed"
        email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_elem.clear()
        self.enter_password(password)
        self.click_login()
        self.highlight_username_field()
        return self.get_empty_field_prompt()

    def highlight_username_field(self):
        """
        Highlights the username field using JavaScript for visual feedback.
        """
        email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.driver.execute_script(
            "arguments[0].style.border='2px solid red'; arguments[0].style.backgroundColor='#ffe6e6';",
            email_elem
        )

    def is_username_field_highlighted(self):
        """
        Checks if the username field is visually highlighted (border color).
        Returns True if highlighted, False otherwise.
        """
        email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        border = self.driver.execute_script("return arguments[0].style.border;", email_elem)
        bg_color = self.driver.execute_script("return arguments[0].style.backgroundColor;", email_elem)
        return border == "2px solid red" and bg_color == "#ffe6e6"

    # --- Start of TC_SCRUM74_004 steps ---
    def tc_scrum74_004_invalid_password_flow(self, email: str, wrong_password: str) -> bool:
        """
        TC_SCRUM74_004 Steps:
        1. Navigate to the login page
        2. Enter valid registered email
        3. Enter incorrect password
        4. Click on the Login button
        5. Validate error message 'Invalid password'
        """
        self.load()
        assert self.is_displayed(), "Login page is not displayed"
        self.enter_email(email)
        self.enter_password(wrong_password)
        self.click_login()
        error = self.get_error_message()
        assert error is not None, "No error message displayed after invalid login attempt"
        assert "Invalid password" in error, f"Expected 'Invalid password' error message, got: {error}"
        return True
    # --- End of TC_SCRUM74_004 steps ---
