# Test Case: TC_LOGIN_002 - Negative Login with Invalid Email
# Traceability: SCRUM-91 | testCaseId: 117
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_invalid_email(driver):
    """
    Test Case ID: 117
    Title: TC_LOGIN_002 - Negative Login with Invalid Email
    Acceptance Criteria: SCRUM-91
    Steps:
        1. Navigate to the login page [URL: https://app.example.com/login]
        2. Enter invalid email address [Email: invaliduser@example.com]
        3. Enter valid password [Password: ValidPass123!]
        4. Click on the Login button
    Expected Result:
        - Error message 'Invalid email or password' is displayed
        - User remains on login page (not redirected to dashboard)
    """
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible."
    assert login_page.enter_email("invaliduser@example.com"), "Email not entered correctly."
    assert login_page.enter_password("ValidPass123!"), "Password not entered or not masked."
    login_page.click_login()
    assert login_page.is_error_message_displayed("Invalid email or password"), (
        "Expected error message 'Invalid email or password' not displayed."
    )
    assert not login_page.is_redirected_to_dashboard(), "User should not be redirected to dashboard after invalid login."
