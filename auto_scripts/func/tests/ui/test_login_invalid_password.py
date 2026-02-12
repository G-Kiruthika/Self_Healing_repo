from core.driver_factory import get_driver
from pages.login_page import LoginPage


def test_login_invalid_password():
 """Test login functionality with invalid password.
 
 This test verifies that:
 1. User can navigate to login page
 2. User can enter username and password
 3. User remains on login page after invalid credentials
 4. Error message is displayed for invalid login
 """
 driver = get_driver()
 login_page = LoginPage(driver)
 
 # Test data
 username = "standard_user"
 password = "wrong_password"
 
 # Execute test flow
 login_page.navigate_to_login_page()
 login_page.enter_username(username)
 login_page.enter_password(password)
 login_page.click_login_button()
 
 # Assertions
 assert login_page.is_not_logged_in(), "User should not be logged in with invalid credentials"
 assert login_page.is_error_message_displayed(), "Error message should be displayed for invalid login"
 
 driver.quit()
