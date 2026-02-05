# Selenium Test Script for LGN-01: Verify successful login with valid credentials
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

def test_LGN_01_valid_login(driver):
    """
    LGN-01: Verify successful login with valid credentials
    Steps:
    1. Navigate to login page
    2. Enter valid email and password
    3. Click Login button
    4. Assert redirected to Dashboard
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    assert login_page.navigate_to_login(), "Login page is not displayed with email and password fields."
    # Step 2: Enter valid email and password
    valid_email = 'testuser@example.com'
    valid_password = 'ValidPass123!'
    assert login_page.enter_valid_credentials(valid_email, valid_password), "Failed to enter valid credentials."
    # Step 3: Click Login button
    assert login_page.click_login_button(), "Login button click did not redirect to dashboard."
    # Step 4: Assert redirected to Dashboard
    assert login_page.is_dashboard_visible(), "Dashboard is not visible after login."
