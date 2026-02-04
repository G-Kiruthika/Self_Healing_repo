# Test Script: Verify successful login with valid credentials (LGN-01)
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

def test_login_valid_credentials(driver):
    """
    TestCase ID: LGN-01
    Description: Verify successful login with valid credentials
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page."

    # Step 2: Enter valid email and password
    valid_email = "test.user@example.com"  # Replace with a valid email for the test environment
    valid_password = "SecurePass123!"      # Replace with a valid password for the test environment
    login_page.enter_credentials(valid_email, valid_password)
    # No assert needed here: field input is implicit unless an exception is raised

    # Step 3: Click Login button
    login_page.click_login()
    # Optionally wait for dashboard to load (could use explicit wait in real-world)
    time.sleep(2)
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard after login."
