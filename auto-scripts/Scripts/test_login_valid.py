# Test script for LGN-01: Verify successful login with valid credentials
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os

# Import the LoginPage Page Object
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_valid_credentials(driver):
    """
    LGN-01: Verify successful login with valid credentials
    Steps:
    1. Navigate to login page
    2. Enter valid email and password
    3. Click Login button
    4. Assert redirected to Dashboard
    """
    # Step 1: Navigate to login page
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://example-ecommerce.com/login"), "Not on login page URL"

    # Step 2: Enter valid email and password
    valid_email = "test.user@example.com"  # Replace with a valid test account
    valid_password = "TestPassword123"     # Replace with the correct password
    login_page.enter_email(valid_email)
    login_page.enter_password(valid_password)

    # Step 3: Click Login button
    login_page.click_login()

    # Step 4: Assert redirected to Dashboard
    assert login_page.is_dashboard_displayed(), "Dashboard header not visible after login"
    # Optionally, assert URL changed to dashboard
    dashboard_url_prefix = "https://example-ecommerce.com/dashboard"
    WebDriverWait(driver, 10).until(lambda d: d.current_url.startswith(dashboard_url_prefix))
    assert driver.current_url.startswith(dashboard_url_prefix), f"Not redirected to dashboard, current url: {driver.current_url}"
