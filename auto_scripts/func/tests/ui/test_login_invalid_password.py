# tests/ui/test_login_invalid_password.py
# Test case: UI_TC_02 - Login with invalid password
# Feature: Login

from core.driver_factory import get_driver
from pages.login_page import LoginPage


def test_login_invalid_password():
 """
 Test login functionality with invalid password.
 Verifies that:
 - User cannot login with wrong password
 - Error message is displayed
 - User remains on login page
 """
 # Test data
 username = "standard_user"
 password = "wrong_password"
 
 # Initialize driver and page object
 driver = get_driver()
 login_page = LoginPage(driver)
 
 try:
 # Execute test flow
 login_page.navigate_to_login_page()
 login_page.enter_username(username)
 login_page.enter_password(password)
 login_page.click_login_button()
 
 # Assertions
 assert login_page.is_not_logged_in(), "User should not be logged in with invalid password"
 assert login_page.is_error_message_displayed(), "Error message should be displayed for invalid login"
 
 finally:
 driver.quit()
