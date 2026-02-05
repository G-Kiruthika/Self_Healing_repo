# Selenium Test Script for TC_LOGIN_002: Negative Login Scenario
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_002_negative_login(driver):
    """
    Test Case TC_LOGIN_002: Negative login attempt with incorrect password.
    Steps:
      1. Navigate to the login page
      2. Enter valid registered email
      3. Enter incorrect password
      4. Click on the Login button
      5. Verify error message and user remains on login page
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    assert login_page.navigate_to_login(), "Login page should be displayed."

    # Step 2: Enter valid registered email
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Email '{email}' should be accepted in the field."

    # Step 3: Enter incorrect password
    wrong_password = "WrongPass456!"
    assert login_page.enter_incorrect_password(wrong_password), "Incorrect password should be masked and accepted."

    # Step 4: Click Login and check error message
    assert login_page.click_login_and_check_error(), "Error message 'Invalid email or password' should be displayed."
    assert login_page.is_error_message_displayed("Invalid email or password"), "Error message text should match."

    # Step 5: Verify user remains on login page
    assert login_page.verify_user_stays_on_login_page(), "User should remain on login page after failed login."
