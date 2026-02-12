from core.driver_factory import get_driver
from pages.login_page import LoginPage


def test_login_invalid_password():
 """Test login functionality with invalid password."""
 driver = get_driver()
 login_page = LoginPage(driver)
 
 # Test data
 login_data = {
 'username': 'standard_user',
 'password': 'wrong_password'
 }
 
 # Test flow
 login_page.navigate_to_login_page()
 login_page.enter_username(login_data['username'])
 login_page.enter_password(login_data['password'])
 login_page.click_login_button()
 
 # Assertions
 assert login_page.is_not_logged_in(), "User should not be logged in with invalid password"
 assert login_page.is_error_message_displayed(), "Error message should be displayed for invalid login"
 
 driver.quit()
