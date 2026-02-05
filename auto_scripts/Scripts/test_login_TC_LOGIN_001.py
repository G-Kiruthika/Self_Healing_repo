# Selenium Automation Test Script for TC_LOGIN_001
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")  # Run headless for CI/CD
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_001(driver):
    """
    Test Case ID: TC_LOGIN_001
    Description: Valid login with correct credentials.
    Steps:
      1. Navigate to the login page
      2. Enter valid registered email in the email field
      3. Enter correct password in the password field
      4. Click on the Login button
      5. Verify user session is created
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page should be displayed with email and password fields."

    # Step 2: Enter valid registered email
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Email '{email}' should be accepted and displayed in the field."

    # Step 3: Enter correct password
    password = "ValidPass123!"
    assert login_page.enter_password(password), "Password should be masked and accepted."

    # Step 4: Click on the Login button
    assert login_page.click_login(), "User should be authenticated and redirected to dashboard."

    # Step 5: Verify user session is created (proxy by user profile icon)
    assert login_page.verify_user_session(), "User session should be created and user profile displayed."
