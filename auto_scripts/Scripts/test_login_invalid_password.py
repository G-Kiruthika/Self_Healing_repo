# Selenium Test Script for TC_LOGIN_003: Login with valid email and invalid password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.login
@pytest.mark.negative
@pytest.mark.usefixtures('driver')
def test_tc_login_003_valid_email_invalid_password(driver):
    """
    Test Case ID: TC_LOGIN_003
    Description: Attempt login with valid email and invalid password; verify error message and user remains on login page.
    Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter valid email address [Test Data: Email: testuser@example.com]
        3. Enter invalid password [Test Data: Password: WrongPassword123]
        4. Click on the Login button
        5. Verify error message displayed: 'Invalid email or password'
        6. Verify user remains on login page (not authenticated)
    Acceptance Criteria: AC_002
    Traceability: PageClass=LoginPage, testCaseId=120
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), 'Login page URL is not loaded!'
    assert login_page.is_login_fields_visible(), 'Login fields are not visible!'

    # Step 2: Enter valid email address
    email = 'testuser@example.com'
    assert login_page.enter_email(email), f'Email "{email}" was not entered correctly!'

    # Step 3: Enter invalid password
    invalid_password = 'WrongPassword123'
    assert login_page.enter_password(invalid_password), 'Password was not entered/masked correctly!'

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(1)  # Wait for error message to appear

    # Step 5: Verify error message is displayed
    error_message = login_page.get_error_message()
    assert error_message is not None, 'No error message displayed!'
    assert 'invalid email or password' in error_message.lower(), f'Unexpected error message: {error_message}'

    # Step 6: Verify user remains on login page (not authenticated)
    assert driver.current_url == LoginPage.LOGIN_URL, 'User is not on login page after failed login!'
    # Optionally, check that dashboard is NOT displayed
    assert not login_page.is_redirected_to_dashboard(), 'User should NOT be redirected to dashboard!'
