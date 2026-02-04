# test_loginpage.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data
LOGIN_URL = "https://example-ecommerce.com/login"
VALID_EMAIL = "testuser@example.com"
VALID_PASSWORD = "ValidPass123!"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def login_page(driver):
    return LoginPage(driver)

def test_TC_LOGIN_001(login_page, driver):
    """
    Test Case ID: 115
    Description: Test Case TC_LOGIN_001
    Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Enter valid password
        4. Click on the Login button
        5. Verify user session is created
    Acceptance Criteria: SCRUM-91
    """
    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://example-ecommerce.com/login"), "Login page URL did not match."
    # Step 2: Assert login fields are visible
    assert login_page.is_login_fields_visible(), "Email or Password field not visible."
    # Step 3: Enter valid email
    login_page.enter_email(VALID_EMAIL)
    email_field = driver.find_element(By.ID, "login-email")
    assert email_field.get_attribute("value") == VALID_EMAIL, "Email not accepted or displayed in field."
    # Step 4: Enter valid password
    login_page.enter_password(VALID_PASSWORD)
    password_field = driver.find_element(By.ID, "login-password")
    password_type = password_field.get_attribute("type")
    assert password_type == "password", "Password field is not masked."
    # Step 5: Click Login button
    login_page.click_login()
    # Step 6: Assert redirected to dashboard
    assert login_page.is_redirected_to_dashboard(), "User not redirected to dashboard or dashboard not loaded."
    # Step 7: Verify user session is created
    assert login_page.verify_user_session(), "User session not created or user profile not displayed."
