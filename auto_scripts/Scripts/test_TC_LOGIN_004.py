# test_TC_LOGIN_004.py
"""
Automated Selenium Test Script for TC_LOGIN_004: Valid email, empty password login attempt.
This script uses the TC_LOGIN_004_TestPage PageClass and validates all steps as per enterprise standards.
"""
import sys
import os
import json
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# Ensure Pages directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))

from TC_LOGIN_004_TestPage import TC_LOGIN_004_TestPage

def main():
    # Test data
    email = "testuser@example.com"
    url = "https://app.example.com/login"
    locators_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Locators/Locators.json'))

    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        page = TC_LOGIN_004_TestPage(driver, timeout=15, locators_path=locators_path)
        results = page.run_tc_login_004(email, url)

        # Stepwise assertions
        assert results["step_1_navigate_login"], "Step 1 Failed: Login page not displayed."
        assert results["step_2_enter_email"], "Step 2 Failed: Email not entered correctly."
        assert results["step_3_leave_password_empty"], "Step 3 Failed: Password field not left empty."
        assert results["step_4_click_login"], "Step 4 Failed: Login button not clicked."
        assert results["step_5_validation_error"], "Step 5 Failed: Validation error not displayed."
        assert results["step_6_login_prevented"], "Step 6 Failed: Login not prevented, user did not remain on login page."
        assert results["overall_pass"], f"Test Failed: {results.get('exception', 'Unknown error')}"
        print("TC_LOGIN_004 PASSED. All steps validated.")
        print(json.dumps(results, indent=2))
    except AssertionError as ae:
        print("TC_LOGIN_004 FAILED.")
        print(str(ae))
        print(json.dumps(results, indent=2))
        sys.exit(1)
    except WebDriverException as wd:
        print("WebDriver error:", str(wd))
        sys.exit(2)
    except Exception as e:
        print("Unexpected error:", traceback.format_exc())
        sys.exit(3)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
