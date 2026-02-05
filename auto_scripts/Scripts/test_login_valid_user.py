# Selenium test script for TC-LOGIN-001: Valid user login
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

def test_login_valid_user(driver):
    """
    Test Case ID: 228
    Test Case: TC-LOGIN-001
    Description: Verify successful login with valid credentials
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page is not displayed with email and password fields"

    # Step 2: Enter valid registered email address
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Email '{email}' was not accepted or displayed in the field"

    # Step 3: Enter correct password
    password = "ValidPass123!"
    assert login_page.enter_password(password), "Password is not masked or not accepted"

    # Step 4: Click on the Login button
    assert login_page.click_login(), "User was not authenticated or not redirected to dashboard/home page"

    # Step 5: Verify user session is established
    assert login_page.verify_user_session(), "User session is not established: username not displayed or session cookie missing"
