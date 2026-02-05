# Selenium Test Script for TC_SCRUM-74_003: Login with special characters in username
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_special_characters_username(driver):
    """
    TC_SCRUM-74_003: Login with username containing special characters (dots, underscores, hyphens)
    Steps:
        1. Navigate to the login page
        2. Enter valid username containing special characters
        3. Enter valid password
        4. Click on the Login button
        5. Verify successful login and redirection to dashboard
    """
    login_page = LoginPage(driver)
    special_username = "test.user_name-123@example.com"
    valid_password = "ValidPass123!"
    # Step 1-5: End-to-end test with assertions inside the method
    assert login_page.login_special_characters_username(special_username, valid_password), (
        "Login with special characters in username failed or dashboard not displayed!"
    )
    # Additional explicit checks for traceability
    assert driver.current_url != login_page.LOGIN_URL, "User is still on login page after supposed successful login!"
    # Optionally, check presence of dashboard elements
    dashboard_header = driver.find_element(*login_page.DASHBOARD_HEADER)
    user_icon = driver.find_element(*login_page.USER_PROFILE_ICON)
    assert dashboard_header.is_displayed(), "Dashboard header is not visible after login!"
    assert user_icon.is_displayed(), "User profile icon is not visible after login!"
