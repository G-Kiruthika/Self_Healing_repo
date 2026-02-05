# test_login_invalid_password.py
"""
Selenium Test Script for TC_SCRUM74_004: Invalid Password Login
Covers the workflow:
 1. Navigate to login page
 2. Enter valid email
 3. Enter incorrect password
 4. Click login
 5. Verify error message 'Invalid password'

Test Data:
- Email: testuser@example.com
- Password: WrongPassword123

Acceptance Criteria:
- Login page is displayed
- Email is accepted
- Password is masked and accepted
- Login fails with error message 'Invalid password'

Traceability:
- Page Object: LoginPage (auto_scripts/Pages/LoginPage.py)
- Test Case ID: TC_SCRUM74_004
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_scrum74_004_login_invalid_password(driver):
    """
    Test Case TC_SCRUM74_004
    Steps:
      1. Navigate to login page
      2. Enter valid registered email
      3. Enter incorrect password
      4. Click Login
      5. Verify error message 'Invalid password'
    """
    # Test Data
    email = "testuser@example.com"
    wrong_password = "WrongPassword123"

    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.load()
    assert login_page.is_displayed(), "Login page is not displayed (Step 1 failed)"

    # Step 2: Enter valid registered email
    login_page.enter_email(email)
    email_elem = driver.find_element(*LoginPage.EMAIL_FIELD)
    assert email_elem.get_attribute("value") == email, "Email not accepted in field (Step 2 failed)"

    # Step 3: Enter incorrect password
    login_page.enter_password(wrong_password)
    password_elem = driver.find_element(*LoginPage.PASSWORD_FIELD)
    # Check password field type is 'password' (masked)
    assert password_elem.get_attribute("type") == "password", "Password field is not masked (Step 3 failed)"
    assert password_elem.get_attribute("value") == wrong_password, "Password not accepted in field (Step 3 failed)"

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Verify error message 'Invalid password'
    error_text = login_page.get_error_message()
    assert error_text is not None, "No error message displayed after invalid login (Step 5 failed)"
    assert "Invalid password" in error_text, f"Expected 'Invalid password' message, got: {error_text} (Step 5 failed)"

    # Optionally, verify method return value
    assert login_page.tc_scrum74_004_login_invalid_password(email, wrong_password) is True, "tc_scrum74_004_login_invalid_password method did not return True"
