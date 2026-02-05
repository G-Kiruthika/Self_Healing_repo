# Test Script for TC-LOGIN-001: Valid Login Happy Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_001_valid_login(driver):
    """
    TC-LOGIN-001: Valid Login Happy Path
    Steps:
    1. Navigate to login page
    2. Assert email and password fields are displayed
    3. Enter valid email
    4. Enter valid password
    5. Click Login
    6. Assert dashboard is displayed
    7. Assert user session is established
    """
    # Test Data
    login_url = "https://example-ecommerce.com/login"
    valid_email = "testuser@example.com"
    valid_password = "ValidPass123!"

    # Step 1: Navigate to login page
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    assert driver.current_url.startswith(login_url), f"Expected URL to start with {login_url}, got {driver.current_url}"

    # Step 2: Assert login page displayed (email & password fields)
    assert login_page.is_login_page_displayed(), "Login page fields not visible"

    # Step 3: Enter valid email
    assert login_page.enter_email(valid_email), f"Email '{valid_email}' not accepted in email field"

    # Step 4: Enter valid password
    assert login_page.enter_password(valid_password), "Password not masked or not accepted in password field"

    # Step 5: Click Login
    assert login_page.click_login(), "Login button click did not navigate to dashboard"

    # Step 6: Assert dashboard displayed
    assert login_page.is_dashboard_displayed(), "Dashboard not displayed after login"

    # Step 7: Verify user session is established (user profile icon and session cookie)
    assert login_page.verify_user_session(), "User session not established (profile icon/session cookie missing)"

    # Extra: Assert user name is displayed (if applicable)
    try:
        user_profile = driver.find_element(By.CSS_SELECTOR, ".user-profile-name")
        assert user_profile.is_displayed(), "User profile name not displayed in header"
    except Exception as e:
        pytest.fail(f"User profile name element not found: {e}")
