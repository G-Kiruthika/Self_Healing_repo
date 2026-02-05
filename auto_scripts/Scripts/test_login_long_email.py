# Selenium Automation Test Script for TC-LOGIN-008: Login with extremely long email address
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data for TC-LOGIN-008
test_email = (
    "verylongemailaddress" * 12 + "@example.com"
)  # >255 chars
test_password = "ValidPass123!"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_008_long_email(driver):
    """
    Test Case TC-LOGIN-008:
    1. Navigate to the login page
    2. Enter an extremely long email address (255+ characters)
    3. Enter valid password
    4. Click on the Login button
    5. Verify system truncates input or shows validation error, and login fails gracefully
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.navigate()
    assert login_page.is_loaded(), "Login page is not loaded as expected."

    # Step 2: Enter an extremely long email address
    email_result = login_page.enter_email(test_email)
    assert email_result in ["truncated", "validation_error", "ok"], (
        f"Unexpected email input result: {email_result}"
    )

    # Step 3: Enter valid password
    password_entered = login_page.enter_password(test_password)
    assert password_entered, "Password was not entered correctly."

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Verify system truncates input or shows validation error, and login fails gracefully
    assert login_page.is_login_failed_gracefully(), (
        "Login did not fail gracefully or no error message/validation shown for long email."
    )
