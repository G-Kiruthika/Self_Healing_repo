# Selenium Test Script for TC_SCRUM74_006: Login with Empty Password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from auto_scripts.Pages.LoginPage import LoginPage
import time

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

def test_tc_scrum74_006_login_with_empty_password(driver):
    """
    Test Case: TC_SCRUM74_006
    1. Navigate to the login page
    2. Enter valid email
    3. Leave password field empty
    4. Click on the Login button
    5. Validation error displayed: 'Password is required'
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    assert login_page.navigate_to_login(), "Login page did not load as expected."
    # Step 2: Enter valid email
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Email '{email}' was not accepted in the field."
    # Step 3: Leave password field empty
    password_field = driver.find_element(By.ID, "login-password")
    password_field.clear()
    assert password_field.get_attribute("value") == "", "Password field is not empty."
    # Step 4: Click on the Login button
    driver.find_element(By.ID, "login-submit").click()
    # Step 5: Validate error message
    assert login_page.is_validation_error_displayed("Password is required"), "Expected 'Password is required' validation error was not displayed."
    # Extra: Ensure user remains on login page and dashboard is NOT visible
    current_url = driver.current_url
    assert current_url.startswith(login_page.LOGIN_URL), f"User did not stay on login page, current URL: {current_url}"
    assert not login_page.is_dashboard_displayed(), "Dashboard should not be visible when login fails."
