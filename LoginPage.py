# LoginPage.py
# Automated script for TC_LOGIN_002: Verify 'Remember Me' checkbox absence
# Automated script for TC_LOGIN_003: Forgot Username workflow

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.login_screen_locator = (By.ID, "login_screen")
        self.forgot_username_link_locator = (By.ID, "forgot_username_link")
        self.instructions_locator = (By.ID, "instructions")
        self.username_result_locator = (By.ID, "username_result")
        # Locator for 'Remember Me' checkbox (TC_LOGIN_002)
        self.remember_me_checkbox_locator = (By.ID, "remember_me_checkbox")

    def navigate_to_login_screen(self):
        """
        Navigate to the login screen
        Validates that the login screen is displayed
        Used by: TC_LOGIN_002 (Step 1), TC_LOGIN_003 (Step 1)
        """
        self.driver.get("https://example.com/login")
        assert self.driver.find_element(*self.login_screen_locator).is_displayed(), "Login screen is not displayed"

    def check_remember_me_not_present(self):
        """
        Check that the 'Remember Me' checkbox is NOT present on the login screen
        Used by: TC_LOGIN_002 (Step 2)
        Returns: True if checkbox is not present, False otherwise
        """
        try:
            self.driver.find_element(*self.remember_me_checkbox_locator)
            # If element is found, the checkbox is present (test should fail)
            raise AssertionError("'Remember Me' checkbox is present, but it should NOT be present")
        except NoSuchElementException:
            # Element not found - this is the expected behavior
            return True

    # TC_LOGIN_002 specific methods
    def verify_login_screen_displayed(self):
        """
        TC_LOGIN_002 - Step 1: Navigate to the login screen
        Expected: Login screen is displayed
        """
        self.navigate_to_login_screen()
        return self.driver.find_element(*self.login_screen_locator).is_displayed()

    def verify_remember_me_checkbox_not_present(self):
        """
        TC_LOGIN_002 - Step 2: Check for the presence of 'Remember Me' checkbox
        Expected: 'Remember Me' checkbox is NOT present
        """
        return self.check_remember_me_not_present()

    # TC_LOGIN_003 specific methods (preserved existing functionality)
    def click_forgot_username(self):
        """
        Click on 'Forgot Username' link
        Used by: TC_LOGIN_003 (Step 2)
        """
        self.driver.find_element(*self.forgot_username_link_locator).click()
        assert self.driver.find_element(*self.instructions_locator).is_displayed(), "'Forgot Username' workflow is not initiated"

    def follow_recovery_instructions(self):
        """
        Follow instructions to recover username
        Used by: TC_LOGIN_003 (Step 3)
        """
        instructions = self.driver.find_element(*self.instructions_locator).text
        # Simulate following instructions (actual steps depend on application logic)
        # For demonstration, assume submitting email or phone number
        self.driver.find_element(By.ID, "email_input").send_keys("user@example.com")
        self.driver.find_element(By.ID, "submit_button").click()
        assert self.driver.find_element(*self.username_result_locator).is_displayed(), "Username recovery instructions not followed or username not retrieved"


# Example test case execution for TC_LOGIN_002
# from selenium import webdriver
# driver = webdriver.Chrome()
# login_page = LoginPage(driver)
# 
# # TC_LOGIN_002: Verify 'Remember Me' checkbox absence
# login_page.verify_login_screen_displayed()
# login_page.verify_remember_me_checkbox_not_present()
# print("TC_LOGIN_002: PASSED - 'Remember Me' checkbox is not present")

# Example test case execution for TC_LOGIN_003
# from selenium import webdriver
# driver = webdriver.Chrome()
# login_page = LoginPage(driver)
# 
# # TC_LOGIN_003: Forgot Username workflow
# login_page.navigate_to_login_screen()
# login_page.click_forgot_username()
# login_page.follow_recovery_instructions()
# print("TC_LOGIN_003: PASSED - Username recovered successfully")