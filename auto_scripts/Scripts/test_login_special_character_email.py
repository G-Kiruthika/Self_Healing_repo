# Selenium Test Script for TC_LOGIN_019: Login with special character email
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

def test_login_with_special_character_email(driver):
    """
    Test Case: TC_LOGIN_019
    Steps:
    1. Navigate to the login page
    2. Enter email with special characters in valid format
    3. Enter valid password
    4. Click Login button
    5. System processes login appropriately based on whether email is registered
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    email = "test.user+tag@example.co.uk"
    password = "ValidPass123!"
    
    # Step 1: Navigate to login page and verify fields
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "[SCRUM-91][Step 1] Login fields are not visible!"
    
    # Step 2: Enter special character email and verify
    assert login_page.enter_email(email), "[SCRUM-91][Step 2] Email with special characters was not accepted!"
    
    # Step 3: Enter password and verify it is masked
    assert login_page.enter_password(password), "[SCRUM-91][Step 3] Password was not masked/entered!"
    
    # Step 4: Click Login
    login_page.click_login()
    
    # Step 5: Check for either dashboard redirect or error message
    import time
    time.sleep(2)  # Allow page to process
    redirected = login_page.is_redirected_to_dashboard()
    error_displayed = False
    try:
        error_elem = driver.find_element(*LoginPage.ERROR_MESSAGE)
        error_displayed = error_elem.is_displayed()
    except Exception:
        pass
    
    assert redirected or error_displayed, "[SCRUM-91][Step 4] Neither dashboard nor error message displayed after login attempt!"
    if redirected:
        print("[SCRUM-91][Step 4] Login successful, redirected to dashboard.")
    else:
        print("[SCRUM-91][Step 4] Login failed, error message displayed.")
