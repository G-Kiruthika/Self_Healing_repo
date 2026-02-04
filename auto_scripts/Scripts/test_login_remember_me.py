# Selenium Automation Test Script for TC_LOGIN_007: Remember Me Session Persistence
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
from auto_scripts.Pages.LoginPage import LoginPage

def driver_factory():
    '''Factory method to create a new Chrome WebDriver instance.'''
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Remove if you want to see the browser
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        return driver
    except WebDriverException as e:
        pytest.fail(f'WebDriver could not be started: {e}')

@pytest.mark.login
@pytest.mark.remember_me
@pytest.mark.usefixtures('setup')
def test_remember_me_session_persistence():
    '''
    TC_LOGIN_007: End-to-end test for 'Remember Me' session persistence after browser restart.
    Steps:
    1. Navigate to the login page
    2. Enter valid email and password
    3. Check the 'Remember Me' checkbox
    4. Click Login button
    5. Verify user is logged in and redirected to dashboard
    6. Save session cookies, quit browser, start new browser
    7. Load cookies, navigate to app, verify user is still logged in (no login prompt)
    '''
    email = 'testuser@example.com'
    password = 'ValidPass123!'
    driver = driver_factory()
    login_page = LoginPage(driver)
    try:
        session_persistent = login_page.remember_me_session_persistence(email, password, driver_factory)
        assert session_persistent, 'Session was not persisted after browser restart with Remember Me checked.'
    finally:
        try:
            driver.quit()
        except Exception:
            pass
