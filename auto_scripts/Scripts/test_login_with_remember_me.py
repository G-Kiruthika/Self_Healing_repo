# Selenium test script for TC_LOGIN_002: Login with Remember Me
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_remember_me(driver):
    """
    Test Case: TC_LOGIN_002
    Description: End-to-end login workflow with Remember Me checked.
    Steps:
      1. Navigate to the login page
      2. Enter valid username
      3. Enter valid password
      4. Check the Remember Me checkbox
      5. Click on the Login button
      6. Verify user is authenticated, redirected to dashboard, and session is persisted
    """
    login_page = LoginPage(driver)
    email = 'testuser@example.com'
    password = 'Test@1234'

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter valid username
    assert login_page.enter_email(email), "Username was not entered correctly!"

    # Step 3: Enter valid password
    assert login_page.enter_password(password), "Password was not entered/masked correctly!"

    # Step 4: Check the Remember Me checkbox
    assert login_page.check_remember_me(), "Remember Me checkbox was not selected!"

    # Step 5: Click on the Login button
    login_page.click_login()

    # Step 6: Verify user is authenticated, redirected to dashboard, and session is persisted
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard!"
    assert login_page.is_session_token_created(), "User session was not created!"

    # (Optional) Pause to visually verify if running non-headless
    # time.sleep(2)

    print("TC_LOGIN_002: Login with Remember Me - PASSED")
