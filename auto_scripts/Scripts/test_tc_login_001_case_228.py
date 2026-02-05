# Selenium Pytest Automation for TC-LOGIN-001 (testCaseId 228)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError, NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage

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

def test_tc_login_001_case_228(driver):
    """
    TC-LOGIN-001: Valid Login Happy Path (testCaseId 228)
    Steps:
      1. Navigate to the login page
      2. Assert login fields are visible
      3. Enter valid email
      4. Enter valid password
      5. Click Login
      6. Assert dashboard is displayed
      7. Assert user session is established (profile icon and session cookie)
    """
    login_page = LoginPage(driver)
    valid_email = "testuser@example.com"
    valid_password = "ValidPass123!"

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Step 1 Failed: Login page is not displayed with email and password fields."

    # Step 2: Assert login fields are visible
    assert login_page.is_login_page_displayed(), "Step 2 Failed: Login fields are not visible."

    # Step 3: Enter valid email
    assert login_page.enter_email(valid_email), f"Step 3 Failed: Email '{valid_email}' was not accepted or displayed in the field."

    # Step 4: Enter valid password
    assert login_page.enter_password(valid_password), "Step 4 Failed: Password is not masked or not accepted."

    # Step 5: Click Login
    assert login_page.click_login(), "Step 5 Failed: User was not authenticated or not redirected to dashboard/home page."

    # Step 6: Assert dashboard is displayed
    assert login_page.is_dashboard_displayed(), "Step 6 Failed: Dashboard and user profile should be visible after login."

    # Step 7: Assert user session is established
    assert login_page.verify_user_session(), "Step 7 Failed: User session token is not generated or user profile is not displayed."

    # If all assertions pass, test is successful
    print("TC-LOGIN-001 (testCaseId 228): Login workflow completed successfully.")
