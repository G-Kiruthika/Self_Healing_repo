# test_login_negative_tc_scrum74_004.py
"""
Automated Selenium Test Script for TC_SCRUM74_004: Negative Login - Invalid Password

This script validates that an invalid password triggers the correct error message on the login page.
Test Data:
    - Email: testuser@example.com
    - Password: WrongPassword123

Author: Enterprise Automation Agent
"""
import sys
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

# Import the LoginPage Page Object
from auto_scripts.Pages.LoginPage import LoginPage

# --- Test Configuration ---
LOGIN_URL = "https://example-ecommerce.com/login"  # As per PageClass
EMAIL = "testuser@example.com"
WRONG_PASSWORD = "WrongPassword123"

# --- Test Script ---
def test_tc_scrum74_004_invalid_password():
    """
    Steps:
    1. Navigate to the login page
    2. Enter valid registered email
    3. Enter incorrect password
    4. Click on the Login button
    5. Validate error message 'Invalid password'
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        login_page = LoginPage(driver)
        print("[Step 1] Loading login page...")
        login_page.load()
        assert login_page.is_displayed(), "Login page did not load correctly."
        print("[Step 2] Entering email: {}".format(EMAIL))
        login_page.enter_email(EMAIL)
        print("[Step 3] Entering wrong password.")
        login_page.enter_password(WRONG_PASSWORD)
        print("[Step 4] Clicking Login button.")
        login_page.click_login()
        print("[Step 5] Validating error message...")
        error = login_page.get_error_message()
        assert error is not None, "No error message displayed after invalid login attempt."
        assert "Invalid password" in error, f"Expected 'Invalid password' error message, got: {error}"
        print("[PASS] TC_SCRUM74_004: Invalid password error message displayed as expected.")
    except AssertionError as ae:
        print("[FAIL] Assertion Error:", ae)
        traceback.print_exc()
        sys.exit(1)
    except WebDriverException as wde:
        print("[ERROR] WebDriver Exception:", wde)
        traceback.print_exc()
        sys.exit(2)
    except Exception as ex:
        print("[ERROR] Unexpected Exception:", ex)
        traceback.print_exc()
        sys.exit(3)
    finally:
        if driver:
            driver.quit()
            print("[INFO] WebDriver closed.")

if __name__ == "__main__":
    test_tc_scrum74_004_invalid_password()
