# test_tc_scrum74_005_empty_username_valid_password.py
"""
Selenium Automation Test for TC_SCRUM74_005: Empty Username with Valid Password
Traceability:
- TestCaseId: 197
- TestCaseDescription: TC_SCRUM74_005
- Related PageClass: LoginPage (auto_scripts/Pages/LoginPage.py)
- Validates: Error handling, field validation, and UI feedback for empty username scenario
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.mark.usefixtures("driver")
class TestLoginPage:
    def test_tc_scrum74_005_empty_username_valid_password(self, driver):
        """
        Test Steps:
        1. Navigate to the login page (https://app.example.com/login)
        2. Leave email/username field empty
        3. Enter valid password (ValidPass123!)
        4. Click on the Login button
        5. Verify validation error: 'Email/Username is required'
        """
        login_page = LoginPage(driver)
        login_page.load()
        assert login_page.is_displayed(), "Login page is not displayed"
        # Leave email/username field empty
        email_elem = driver.find_element(*LoginPage.EMAIL_FIELD)
        email_elem.clear()
        # Enter valid password
        login_page.enter_password("ValidPass123!")
        # Ensure password is masked (type='password')
        assert email_elem.get_attribute("type") == "email", "Email field type should be 'email'"
        password_elem = driver.find_element(*LoginPage.PASSWORD_FIELD)
        assert password_elem.get_attribute("type") == "password", "Password field should be masked"
        # Click login
        login_page.click_login()
        # Check for validation error for empty email/username
        validation_errors = driver.find_elements_by_css_selector(".invalid-feedback")
        error_texts = [e.text for e in validation_errors if e.is_displayed()]
        assert any("Email/Username is required" in t for t in error_texts), "'Email/Username is required' validation error not displayed"
        # Ensure user remains on login page
        current_url = driver.current_url
        assert LoginPage.URL in current_url, f"User did not remain on login page, current URL: {current_url}"
        print("TC_SCRUM74_005 passed: Empty username validation error displayed and login prevented.")

# Pytest fixture for WebDriver
@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
