# TC-LOGIN-001: Valid User Login Test (Selenium)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_valid_user_login(driver):
    """
    TC-LOGIN-001: End-to-end login test for valid user.
    Steps:
        1. Navigate to login page
        2. Enter valid email
        3. Enter correct password
        4. Click Login
        5. Verify user session
    Acceptance Criteria:
        - Login page displays email/password fields
        - Email is accepted/displayed
        - Password is masked and accepted
        - User is redirected to dashboard
        - User profile icon is visible (session established)
    """
    # Test Data
    LOGIN_URL = "https://app.example.com/login"  # As per PageClass
    TEST_EMAIL = "testuser@example.com"
    TEST_PASSWORD = "ValidPass123!"

    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    assert login_page.navigate_to_login(), "Login page did not display email/password fields."

    # Step 2: Enter valid email
    assert login_page.enter_email(TEST_EMAIL), f"Email '{TEST_EMAIL}' not accepted/displayed in field."

    # Step 3: Enter correct password
    assert login_page.enter_password(TEST_PASSWORD), "Password not masked or not accepted."

    # Step 4: Click Login
    assert login_page.click_login(), "User not authenticated or not redirected to dashboard."

    # Step 5: Verify user session
    assert login_page.verify_user_session(), "User session not established; profile icon not visible."
