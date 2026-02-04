# Selenium Automation Test Script for TC_LOGIN_001 (LoginPage)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.mark.usefixtures("setup")
class TestLoginPage:
    def test_TC_LOGIN_001_valid_login(self):
        """
        Test Case ID: 115
        Description: Test Case TC_LOGIN_001 - Valid login and user session verification
        Acceptance Criteria: SCRUM-91
        """
        # Test Data
        login_url = "https://example-ecommerce.com/login"
        email = "testuser@example.com"
        password = "ValidPass123!"

        # Setup WebDriver
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)

        try:
            # Step 1: Navigate to the login page
            login_page = LoginPage(driver)
            login_page.go_to()
            assert driver.current_url.startswith(login_url), "Login page URL mismatch"

            # Step 2: Verify email and password fields are displayed
            assert driver.find_element(*LoginPage.EMAIL_FIELD).is_displayed(), "Email field not displayed"
            assert driver.find_element(*LoginPage.PASSWORD_FIELD).is_displayed(), "Password field not displayed"

            # Step 3: Enter valid email
            login_page.enter_email(email)
            entered_email = driver.find_element(*LoginPage.EMAIL_FIELD).get_attribute("value")
            assert entered_email == email, f"Email field value mismatch: expected {email}, got {entered_email}"

            # Step 4: Enter valid password
            login_page.enter_password(password)
            password_type = driver.find_element(*LoginPage.PASSWORD_FIELD).get_attribute("type")
            assert password_type == "password", "Password field is not masked"
            entered_password = driver.find_element(*LoginPage.PASSWORD_FIELD).get_attribute("value")
            assert entered_password == password, "Password field value mismatch"

            # Step 5: Click on the Login button
            login_page.click_login()

            # Step 6: Verify dashboard is loaded
            assert login_page.is_dashboard_loaded(), "Dashboard header not loaded after login"

            # Step 7: Verify user session is created (user profile icon visible)
            assert login_page.is_user_profile_displayed(), "User profile icon not displayed; session not created"

        finally:
            driver.quit()
