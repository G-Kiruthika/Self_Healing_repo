from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.LoginPage import LoginPage

class TC_LOGIN_101_TestPage:
    """
    PageClass for Test Case TC-101 (testCaseId: 1298): Basic Login Flow Validation
    This test performs a standard login using valid credentials and verifies successful navigation to dashboard.
    """
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.login_page = LoginPage(driver, timeout)

    def perform_login_test(self, email, password):
        """
        Steps:
            1. Navigate to Login Page.
            2. Enter valid email and password.
            3. Click Login button.
            4. Validate dashboard header and user profile icon are visible after login.
        Args:
            email (str): Valid user email.
            password (str): Valid user password.
        Returns:
            None
        Raises:
            AssertionError: If login fails or dashboard/profile is not visible.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email(email)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        # Validate dashboard header
        dashboard_header = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.dashboard-title"))
        )
        assert dashboard_header is not None, "Dashboard header not found after login."
        # Validate user profile icon
        user_profile_icon = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".user-profile-name"))
        )
        assert user_profile_icon is not None, "User profile icon not found after login."

    def validate_login_error_on_empty_fields(self):
        """
        Steps:
            1. Navigate to Login Page.
            2. Leave email and password fields empty.
            3. Click Login button.
            4. Validate prompt for mandatory fields is displayed.
        Returns:
            None
        Raises:
            AssertionError: If empty field prompt is not shown.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email("")
        self.login_page.enter_password("")
        self.login_page.click_login()
        empty_field_prompt = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()='Mandatory fields are required']"))
        )
        assert empty_field_prompt is not None, "Mandatory fields prompt not displayed for empty login fields."

    def validate_login_error_on_invalid_credentials(self, email, invalid_password):
        """
        Steps:
            1. Navigate to Login Page.
            2. Enter valid email and invalid password.
            3. Click Login button.
            4. Validate error message is displayed.
        Args:
            email (str): Valid user email.
            invalid_password (str): Invalid password.
        Returns:
            None
        Raises:
            AssertionError: If error message is not shown or login is successful with invalid credentials.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email(email)
        self.login_page.enter_password(invalid_password)
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        assert error_message is not None, "Error message not displayed for invalid credentials."
        assert "Invalid username or password" in error_message, f"Unexpected error message: {error_message}"
        assert self.login_page.is_on_login_page(), "User is not on login page after invalid login attempt."
