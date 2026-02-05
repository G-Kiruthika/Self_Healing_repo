# Selenium Test Script for TC_LOGIN_001
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
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
    Test Case ID: TC_LOGIN_001
    Description: Verify successful login with valid credentials and session creation.
    Steps:
        1. Navigate to the login page
        2. Enter valid registered email
        3. Enter correct password
        4. Click on the Login button
        5. Verify user session is created
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page is not displayed with email and password fields."

    # Step 2: Enter valid registered email
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Email '{email}' was not accepted or not displayed in the field."

    # Step 3: Enter correct password
    password = "ValidPass123!"
    assert login_page.enter_password(password), "Password was not masked or not accepted."

    # Step 4: Click on the Login button
    assert login_page.click_login(), "User was not redirected to dashboard after login."

    # Step 5: Verify user session is created (proxy: user profile is displayed)
    assert login_page.verify_user_session(), "User session token was not generated or user profile is not displayed."

    # Additional: Sanity check - dashboard elements
    assert driver.find_element(By.CSS_SELECTOR, "h1.dashboard-title").is_displayed(), "Dashboard header not visible."
    assert driver.find_element(By.CSS_SELECTOR, ".user-profile-name").is_displayed(), "User profile icon not visible."
