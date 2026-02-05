# Test Case: TC_SCRUM74_006 - Login attempt with valid email and empty password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_valid_email_and_empty_password(driver):
    """
    TC_SCRUM74_006 Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
       - Assert login page is displayed
    2. Enter valid email [Test Data: Email: testuser@example.com]
       - Assert email is accepted
    3. Leave password field empty [Test Data: Password: '']
       - Assert password field remains empty
    4. Click on the Login button
       - Assert validation error displayed: 'Password is required'
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.LOGIN_URL = "https://app.example.com/login"  # override if different
    assert login_page.navigate_to_login(), "Login page was not displayed."

    # Step 2: Enter valid email
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Email '{email}' was not accepted."

    # Step 3: Leave password field empty
    assert login_page.enter_password("") is False or driver.find_element(*login_page.PASSWORD_INPUT).get_attribute("value") == "", "Password field is not empty."

    # Step 4: Click Login button
    login_page.click_login()
    assert login_page.is_validation_error_displayed("Password is required"), "Validation error 'Password is required' was not displayed."
