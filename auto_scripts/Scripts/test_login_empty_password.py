# Test Script for TC_LOGIN_005: Login with valid email and empty password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.mark.usefixtures("driver_init")
class TestLoginEmptyPassword:
    def test_login_with_empty_password(self, driver):
        """
        TC_LOGIN_005: Attempt login with valid email and empty password, expect 'Password is required' validation error.
        Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Leave password field empty
        4. Click on the Login button
        5. Assert validation error 'Password is required' is displayed below password field
        """
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        assert driver.current_url == LoginPage.LOGIN_URL, "Login page did not load correctly."

        # Enter valid email
        email_entered = login_page.enter_email("testuser@example.com")
        assert email_entered, "Email was not entered correctly."

        # Leave password empty and assert field is empty
        password_entered = login_page.enter_password("")
        assert password_entered, "Password field is not present or not masked."
        password_field = driver.find_element(*LoginPage.PASSWORD_FIELD)
        assert password_field.get_attribute("value") == "", "Password field is not empty."

        # Click login
        login_page.click_login()
        time.sleep(1)  # Wait for validation error to appear

        # Assert validation error is displayed
        try:
            validation_error = driver.find_element(*LoginPage.VALIDATION_ERROR)
            assert validation_error.is_displayed(), "Validation error is not displayed."
            assert "Password is required" in validation_error.text, f"Unexpected validation error text: {validation_error.text}"
        except Exception as e:
            pytest.fail(f"Validation error not found or not displayed: {e}")

# Pytest fixture for webdriver initialization
def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode.")

import pytest
@pytest.fixture(scope="class")
def driver_init(request):
    options = Options()
    options.add_argument('--window-size=1920,1080')
    if request.config.getoption("--headless"):
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield driver
    driver.quit()
