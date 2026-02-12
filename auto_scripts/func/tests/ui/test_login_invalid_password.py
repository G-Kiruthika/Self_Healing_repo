from core.driver_factory import get_driver
from pages.login_page import LoginPage

def test_login_invalid_password():
 """
 Test Case: UI_TC_02 - Login with Invalid Password
 Feature: Login
 Description: Verify that login fails with invalid password and error message is displayed
 """
 # Test data
 username = "standard_user"
 password = "wrong_password"
 
 # Initialize driver and page object
 driver = get_driver()
 login_page = LoginPage(driver)
 
 try:
 # Step 1: Navigate to login page
 login_page.navigate_to_login_page()
 
 # Step 2: Enter username
 login_page.enter_username(username)
 
 # Step 3: Enter password
 login_page.enter_password(password)
 
 # Step 4: Click login button
 login_page.click_login_button()
 
 # Step 5: Assert user is not logged in
 assert login_page.is_not_logged_in(), "User should not be logged in with invalid password"
 
 # Step 6: Assert error message is displayed
 assert login_page.is_error_message_displayed(), "Error message should be displayed for invalid password"
 
 finally:
 # Cleanup
 driver.quit()
