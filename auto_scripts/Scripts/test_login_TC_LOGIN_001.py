# Selenium Test Script for TC_LOGIN_001
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto-scripts.Pages.LoginPage import LoginPage
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

def test_TC_LOGIN_001(driver):
    """
    Test Case TC_LOGIN_001: Valid login with correct credentials
    Steps:
    1. Navigate to the login page
    2. Assert login page is displayed with email and password fields
    3. Enter valid email address
    4. Assert email is accepted and displayed in the field
    5. Enter valid password
    6. Assert password is masked and accepted
    7. Click on the Login button
    8. Assert user is authenticated and redirected to dashboard
    9. Assert user session token is generated and user profile is displayed
    """
    login_page = LoginPage(driver)

    # Step 2: Navigate to login page
    login_page.navigate_to_login_page()
    
    # Step 3: Assert login page is displayed
    assert login_page.is_login_page_displayed(), "Login page is not displayed with email and password fields."

    # Step 4: Enter valid email address
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Email '{email}' was not accepted or displayed correctly."

    # Step 5: Enter valid password
    password = "ValidPass123!"
    assert login_page.enter_password(password), "Password field did not accept input or is not masked."

    # Step 6: Click Login button
    login_page.click_login()
    time.sleep(2)  # Wait for possible redirect

    # Step 7: Assert user is authenticated and redirected
    assert login_page.is_authenticated_and_redirected(), "User was not redirected to dashboard after login."

    # Step 8: Assert user session is created (profile icon displayed)
    assert login_page.is_user_session_created(), "User session/profile icon not displayed after login."
