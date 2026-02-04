# Selenium Test Script for TC_LOGIN_019: Login with Special Character Email
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Add Pages directory to sys.path for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_special_email(driver):
    """
    Test Case ID: TC_LOGIN_019
    Description: Test login with email containing special characters in valid format.
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    special_email = "test.user+tag@example.co.uk"
    valid_password = "ValidPass123!"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Step 1 Failed: Login page is not displayed."

    # Step 2: Enter email with special characters
    assert login_page.enter_email(special_email), f"Step 2 Failed: Email '{special_email}' was not entered correctly."

    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Step 3 Failed: Password was not entered/masked correctly."

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(2)  # Wait for login processing

    # Step 5: System processes login appropriately based on whether email is registered
    try:
        if login_page.is_redirected_to_dashboard():
            assert True, "Step 4 Passed: Login successful, redirected to dashboard."
        elif driver.find_element(*LoginPage.ERROR_MESSAGE).is_displayed():
            assert True, "Step 4 Passed: Login failed, error message displayed."
        else:
            pytest.fail("Step 4 Indeterminate: Login processed, but outcome unclear.")
    except NoSuchElementException:
        pytest.fail("Step 4 Indeterminate: Login processed, but no error or dashboard detected.")
