# Selenium Test Script for TC_SCRUM74_004: Invalid Password Error
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.mark.usefixtures("driver_init")
class TestLoginInvalidPassword:
    """
    Test Case: TC_SCRUM74_004
    Steps:
      1. Navigate to the login page
      2. Enter valid registered email
      3. Enter incorrect password
      4. Click on the Login button
    Acceptance Criteria:
      - Login fails with error message 'Invalid password'
    """

    def test_invalid_password_error(self, driver):
        # Step 1: Navigate to the login page
        login_page = LoginPage(driver)
        assert login_page.navigate_to_login(), "Login page should be displayed with email and password fields."

        # Step 2: Enter valid registered email
        email = "testuser@example.com"
        assert login_page.enter_email(email), f"Email '{email}' should be accepted in the email field."

        # Step 3: Enter incorrect password
        incorrect_password = "WrongPassword123"
        assert login_page.enter_incorrect_password(incorrect_password), "Password should be masked and accepted for submission."

        # Step 4: Click on the Login button and check for 'Invalid password' error
        assert login_page.click_login_and_check_invalid_password_error(), "Error message 'Invalid password' should be displayed."


# Pytest fixture for driver initialization (for local test run)
@pytest.fixture(scope="class")
def driver_init(request):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield driver
    driver.quit()
