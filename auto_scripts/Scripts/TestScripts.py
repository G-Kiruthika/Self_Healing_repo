# Existing imports and test methods...
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PageClasses.LoginPage import LoginPage
from PageClasses.DashboardPage import DashboardPage

# Existing test methods...


def test_TC_SCRUM_115_001_valid_login_session_established(driver):
    """
    Test Case TC-SCRUM-115-001
    Steps:
    1. Navigate to the e-commerce website login page
    2. Enter valid username in the username field
    3. Enter valid password in the password field
    4. Click on the Login button
    5. Verify user session is established (user profile/name is displayed in the header, session cookie is created)
    """
    login_url = "https://ecommerce.example.com/login"
    valid_username = "validuser@example.com"
    valid_password = "ValidPass123!"

    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    # Step 1: Navigate to the login page
    driver.get(login_url)
    assert login_page.is_on_login_page(), "Login page did not load properly."

    # Step 2: Enter valid username
    login_page.enter_email(valid_username)

    # Step 3: Enter valid password
    login_page.enter_password(valid_password)

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Verify dashboard is displayed and user session is established
    assert dashboard_page.is_dashboard_displayed(), "Dashboard not displayed after login."

    # Verify user profile/name is displayed in the header
    profile_name_locator = (By.CSS_SELECTOR, "header .profile-name")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(profile_name_locator),
        message="User profile/name not visible in header."
    )
    profile_name_element = driver.find_element(*profile_name_locator)
    assert profile_name_element.text != "", "Profile name is empty or not displayed."

    # Verify session cookie is created
    session_cookie = driver.get_cookie("sessionid")
    assert session_cookie is not None, "Session cookie 'sessionid' was not created."
