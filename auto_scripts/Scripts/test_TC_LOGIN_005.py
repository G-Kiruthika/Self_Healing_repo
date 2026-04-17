import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import sys
import time

# Ensure Pages folder is in sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from TC_LOGIN_005_TestPage import TC_LOGIN_005_TestPage

# Test Data (can be parameterized later)
LOGIN_URL = "https://ecommerce.example.com/login"
VALID_EMAIL = "testuser@example.com"
EXPECTED_VALIDATION_ERROR = "password is required"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1440, 900)
    yield driver
    driver.quit()

def test_tc_login_005_negative_password_required(driver):
    """
    TC-LOGIN-005: Valid email, empty password, expect validation error 'Password is required', and user remains on login page.
    """
    test_page = TC_LOGIN_005_TestPage(driver)

    # Step 1: Navigate to login page
    test_page.go_to_login_page(LOGIN_URL)
    assert test_page.is_on_login_page(), "Step 1 Failed: Login page not displayed."

    # Step 2: Enter valid email
    test_page.enter_email(VALID_EMAIL)
    # Validate email field is populated (optional, but robust)
    email_field_id = test_page.email_field.split('=',1)[1]
    email_value = driver.find_element(By.ID, email_field_id).get_attribute('value')
    assert email_value == VALID_EMAIL, f"Step 2 Failed: Email field value mismatch. Expected: {VALID_EMAIL}, Got: {email_value}"

    # Step 3: Leave password field empty
    test_page.leave_password_empty()
    password_field_id = test_page.password_field.split('=',1)[1]
    password_value = driver.find_element(By.ID, password_field_id).get_attribute('value')
    assert password_value == '', "Step 3 Failed: Password field is not empty."

    # Step 4: Click Login button
    test_page.click_login()

    # Step 5: Validate error is displayed
    validation_error = test_page.get_validation_error()
    assert validation_error is not None, "Step 4 Failed: Validation error not displayed."
    assert EXPECTED_VALIDATION_ERROR in validation_error.lower(), f"Step 4 Failed: Validation error text mismatch. Expected to contain: '{EXPECTED_VALIDATION_ERROR}', Got: '{validation_error}'"

    # Step 6: Validate login is prevented (still on login page)
    assert test_page.is_on_login_page(), "Step 5 Failed: User did not remain on login page after failed login."

    # Overall test pass
    print("TC-LOGIN-005: Passed. Validation error correctly displayed and login prevented.")
