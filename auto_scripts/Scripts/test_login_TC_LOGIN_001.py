# Selenium Test Script for TC_LOGIN_001 - LoginPage
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_001_successful_login(driver):
    """
    Test Case ID: TC_LOGIN_001
    Description: End-to-end login workflow with valid credentials.
    Acceptance Criteria:
      - Login page is displayed with username and password fields
      - Username is entered successfully in the field
      - Password is masked and entered successfully
      - User is authenticated and redirected to the dashboard/home page
      - User session is active and user details are displayed
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    # Step 2: Enter valid username
    assert login_page.enter_email("testuser@example.com"), "Username was not entered correctly!"
    # Step 3: Enter valid password
    assert login_page.enter_password("Test@1234"), "Password was not entered/masked correctly!"
    # Step 4: Click on the Login button
    login_page.click_login()
    # Step 5: Verify user is redirected to dashboard
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard!"
    # Step 6: Verify user session is created and user details are displayed
    assert login_page.is_session_token_created(), "User session was not created!"
