import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PageClasses.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

class TestTC_LOGIN_001:
    """
    Test Case TC_LOGIN_001: Invalid Login Attempt
    Steps:
        1. Navigate to the login screen.
        2. Enter an invalid username and/or password.
        3. Click Login button.
        4. Validate error message 'Invalid username or password. Please try again.' is displayed.
        5. Assert user remains on login page after failed login.
    """

    @pytest.mark.parametrize("email, invalid_password", [
        ("invaliduser@example.com", "wrongpassword"),
        ("", "wrongpassword"),
        ("invaliduser@example.com", "")
    ])
    def test_invalid_login(self, driver, email, invalid_password):
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.enter_email(email)
        login_page.enter_password(invalid_password)
        login_page.click_login()
        expected_error = "Invalid username or password. Please try again."
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "Error message not found after invalid login."
        assert error_msg.strip() == expected_error, f"Expected error '{expected_error}', got '{error_msg.strip()}""
        assert login_page.is_on_login_page(), "User is not on the login page after failed login."
