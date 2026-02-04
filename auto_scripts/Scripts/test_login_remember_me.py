# Test Case: TC_LOGIN_007 - Remember Me session persistence after browser restart
import pytest
from selenium import webdriver
from auto_scripts.Pages.LoginPage import LoginPage

# Adjust as needed for your environment
LOGIN_URL = "https://app.example.com/login"
VALID_EMAIL = "testuser@example.com"
VALID_PASSWORD = "ValidPass123!"


def driver_factory():
    """
    Factory method to instantiate a new Selenium WebDriver instance.
    Adjust options as needed for your environment/CI.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver


@pytest.mark.login
@pytest.mark.remember_me
def test_remember_me_session_persistence():
    """
    TC_LOGIN_007: End-to-end test for 'Remember Me' session persistence after browser restart.
    Steps:
    1. Navigate to the login page
    2. Enter valid email and password
    3. Check the 'Remember Me' checkbox
    4. Click Login button
    5. Verify user is logged in and redirected to dashboard
    6. Save session cookies, quit browser, start new browser
    7. Load cookies, navigate to app, verify user is still logged in (no login prompt)
    """
    driver = driver_factory()
    try:
        login_page = LoginPage(driver)
        session_persistent = login_page.remember_me_session_persistence(
            email=VALID_EMAIL,
            password=VALID_PASSWORD,
            driver_factory=driver_factory
        )
        assert session_persistent, "Session did NOT persist after browser restart with Remember Me checked!"
    finally:
        try:
            driver.quit()
        except Exception:
            pass
