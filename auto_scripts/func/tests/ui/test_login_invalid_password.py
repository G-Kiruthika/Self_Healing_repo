# tests/ui/test_login_invalid_password.py

from core.driver_factory import get_driver
from pages.LoginPage import LoginPage


def test_login_invalid_password():
 """
 Test Case: UI_TC_02 - Login with Invalid Password
 Feature: Login
 Validates that login fails with incorrect password and error message is displayed.
 """
 driver = get_driver()
 login_page = LoginPage(driver)
 
 # Test data
 username = "standard_user"
 password = "wrong_password"
 
 # Flow execution
 login_page.navigate_to_login_page()
 login_page.enter_username(username)
 login_page.enter_password(password)
 login_page.click_login_button()
 
 # Assertions
 assert login_page.is_not_logged_in(), "User should not be logged in with invalid password"
 assert login_page.is_error_message_displayed(), "Error message should be displayed for invalid login"
 
 driver.quit()
