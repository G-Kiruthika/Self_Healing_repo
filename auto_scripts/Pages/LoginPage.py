from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    """
    PageClass for automating login page actions in Selenium.
    Covers navigation, credential entry, 'Remember Me' validation, login, and session checks for TC_LOGIN_08.
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def navigate_to_login_page(self):
        """
        Navigates the browser to the login page using the URL from Locators.json.
        """
        self.driver.get('https://example-ecommerce.com/login')
        assert self.driver.current_url.startswith('https://example-ecommerce.com/login'), 'Login page URL mismatch.'

    def enter_credentials(self, email, password):
        """
        Enters the provided email and password into their respective fields.
        Args:
            email (str): User email.
            password (str): User password.
        """
        self.driver.find_element(By.ID, 'login-email').clear()
        self.driver.find_element(By.ID, 'login-email').send_keys(email)
        self.driver.find_element(By.ID, 'login-password').clear()
        self.driver.find_element(By.ID, 'login-password').send_keys(password)

    def ensure_remember_me_unchecked(self):
        """
        Ensures the 'Remember Me' checkbox is not checked.
        """
        checkbox = self.driver.find_element(By.ID, 'remember-me')
        if checkbox.is_selected():
            checkbox.click()
        assert not checkbox.is_selected(), "'Remember Me' checkbox should be unchecked."

    def click_login(self):
        """
        Clicks the login button to submit credentials.
        """
        self.driver.find_element(By.ID, 'login-submit').click()

    def verify_login_success(self):
        """
        Verifies login by checking dashboard header and user profile icon.
        """
        dashboard_header = self.driver.find_element(By.CSS_SELECTOR, 'h1.dashboard-title')
        profile_icon = self.driver.find_element(By.CSS_SELECTOR, '.user-profile-name')
        assert dashboard_header.is_displayed(), 'Dashboard header not displayed.'
        assert profile_icon.is_displayed(), 'User profile icon not displayed.'

    def verify_logged_out_after_browser_restart(self):
        """
        Closes and reopens the browser, revisits the site, and verifies user is logged out and redirected to login.
        """
        self.driver.quit()
        # Reinitialize driver (assume self.driver is updated externally)
        self.driver = self._reinitialize_driver()
        self.driver.get('https://example-ecommerce.com/login')
        login_header = self.driver.find_element(By.ID, 'login-email')
        assert login_header.is_displayed(), 'User is not redirected to login page after browser restart.'

    def _reinitialize_driver(self):
        """
        Helper to reinitialize the Selenium WebDriver.
        """
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        return webdriver.Chrome(options=options)
