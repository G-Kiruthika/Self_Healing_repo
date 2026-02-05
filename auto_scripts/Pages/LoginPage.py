from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# New imports for cross-browser and mobile support
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
# For Safari, no options required for desktop
# For mobile emulation (Chrome), use ChromeOptions.mobile_emulation

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

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_btn.click()

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None

    def is_on_login_page(self):
        # Check for presence of login form elements
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            return True
        except:
            return False

    def login_with_credentials(self, email, password):
        self.go_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def perform_invalid_login_and_validate(self, email, invalid_password, expected_error):
        self.login_with_credentials(email, invalid_password)
        error_msg = self.get_error_message()
        assert error_msg == expected_error, f"Expected error '{expected_error}', got '{error_msg}'"
        assert self.is_on_login_page(), "User is not on the login page after failed login."

    def login_with_unicode_and_special_characters(self, email="üser+name@example.com", password="P@sswørd!🔒"):
        """
        Test Case TC019: Enter valid email and password containing special characters and Unicode.
        - Inputs: email (default: üser+name@example.com), password (default: P@sswørd!🔒)
        - Verifies that input fields accept Unicode and special characters
        - Submits login and verifies successful login via dashboard header and user profile icon
        """
        self.go_to_login_page()

        # Enter email and validate input value
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)
        actual_email_value = email_input.get_attribute("value")
        assert actual_email_value == email, f"Email field did not accept Unicode/special characters. Expected: {email}, Got: {actual_email_value}"

        # Enter password and validate input value
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)
        actual_password_value = password_input.get_attribute("value")
        assert actual_password_value == password, f"Password field did not accept Unicode/special characters. Expected: {password}, Got: {actual_password_value}"

        # Submit login
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON))
        login_btn.click()

        # Verify successful login via dashboard header and user profile icon
        dashboard_header = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
        user_profile_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
        assert dashboard_header.is_displayed(), "Dashboard header is not displayed after login."
        assert user_profile_icon.is_displayed(), "User profile icon is not displayed after login."

    # --- NEW METHOD FOR CROSS-BROWSER AND MOBILE LOGIN ---
    @staticmethod
    def get_webdriver(browser_type):
        """
        Returns a Selenium WebDriver instance for the specified browser.
        Supported browser_type: 'chrome', 'firefox', 'safari', 'edge', 'mobile_chrome'
        """
        if browser_type == "chrome":
            options = ChromeOptions()
            options.add_argument("--window-size=1920,1080")
            return webdriver.Chrome(options=options)
        elif browser_type == "firefox":
            options = FirefoxOptions()
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            return webdriver.Firefox(options=options)
        elif browser_type == "edge":
            options = EdgeOptions()
            options.add_argument("--window-size=1920,1080")
            return webdriver.Edge(options=options)
        elif browser_type == "safari":
            # Safari driver must be enabled and running on MacOS
            return webdriver.Safari()
        elif browser_type == "mobile_chrome":
            options = ChromeOptions()
            mobile_emulation = {
                "deviceName": "iPhone X"
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            return webdriver.Chrome(options=options)
        else:
            raise ValueError(f"Unsupported browser_type: {browser_type}")

    @classmethod
    def login_on_multiple_browsers(cls, browsers, email, password, timeout=10):
        """
        Attempts login on multiple browsers/devices.
        Args:
            browsers (list): List of browser types ['chrome', 'firefox', 'safari', 'edge', 'mobile_chrome']
            email (str): Login email
            password (str): Login password
            timeout (int): WebDriverWait timeout
        Returns:
            dict: Results for each browser/device
        """
        results = {}
        for browser in browsers:
            driver = None
            try:
                driver = cls.get_webdriver(browser)
                login_page = cls(driver, timeout)
                login_page.login_with_credentials(email, password)
                # Check for dashboard header and user profile icon
                dashboard_header = login_page.wait.until(EC.visibility_of_element_located(cls.DASHBOARD_HEADER))
                user_profile_icon = login_page.wait.until(EC.visibility_of_element_located(cls.USER_PROFILE_ICON))
                success = dashboard_header.is_displayed() and user_profile_icon.is_displayed()
                results[browser] = {
                    "success": success,
                    "error": None if success else "Dashboard or user profile not visible after login"
                }
            except Exception as e:
                results[browser] = {
                    "success": False,
                    "error": str(e)
                }
            finally:
                if driver is not None:
                    driver.quit()
        return results
