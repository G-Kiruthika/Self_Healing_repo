# Test Script for TC_LOGIN_001: Successful Login Workflow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_tc_login_001_successful_login(driver):
    """
    TC_LOGIN_001: End-to-end login workflow with valid credentials.
    Steps:
        1. Navigate to the login page
        2. Enter valid username
        3. Enter valid password
        4. Click Login button
        5. Verify user session is created and user is redirected to dashboard
    Acceptance Criteria: AC_001_Successful_Login
    """
    # Test Data
    email = "testuser@example.com"
    password = "Test@1234"

    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    assert login_page.enter_email(email), "Username was not entered correctly!"
    assert login_page.enter_password(password), "Password was not entered/masked correctly!"
    login_page.click_login()
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard!"
    assert login_page.is_session_token_created(), "User session was not created!"
    # If all assertions pass, login is successful
