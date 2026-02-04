# Auto-generated Selenium Test Script for LoginPage - TC_LOGIN_001
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_001_successful_login(driver):
    """
    Test Case TC_LOGIN_001: Verify user can login successfully with valid credentials
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter valid password
    4. Click on the Login button
    5. Verify user is logged in and dashboard is displayed
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.navigate_to_login()
    assert driver.current_url.startswith("https://app.example.com/login"), "Login page URL mismatch."
    assert driver.find_element(*LoginPage.EMAIL_FIELD).is_displayed(), "Email field not displayed."
    assert driver.find_element(*LoginPage.PASSWORD_FIELD).is_displayed(), "Password field not displayed."

    # Step 2: Enter valid email address
    test_email = "testuser@example.com"
    login_page.enter_email(test_email)
    email_value = driver.find_element(*LoginPage.EMAIL_FIELD).get_attribute('value')
    assert email_value == test_email, f"Email input value mismatch. Expected: {test_email}, Got: {email_value}"

    # Step 3: Enter valid password
    test_password = "ValidPass123!"
    login_page.enter_password(test_password)
    password_type = driver.find_element(*LoginPage.PASSWORD_FIELD).get_attribute('type')
    assert password_type == 'password', "Password field is not masked."

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Verify user is logged in
    assert login_page.is_logged_in(), "Login failed or dashboard not displayed."
    assert driver.find_element(*LoginPage.DASHBOARD_HEADER).is_displayed(), "Dashboard header not displayed."
    assert driver.find_element(*LoginPage.USER_PROFILE_ICON).is_displayed(), "User profile icon not displayed."
