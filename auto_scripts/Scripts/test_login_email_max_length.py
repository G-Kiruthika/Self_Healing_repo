# Selenium Test Script for TC_LOGIN_012: Email Exceeding Max Length
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
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_with_email_exceeding_max_length(driver):
    """
    TC_LOGIN_012: Attempt to enter email address exceeding maximum length (255+ characters) and verify validation/truncation.
    Steps:
    1. Navigate to the login page
    2. Attempt to enter email address exceeding maximum length (255+ characters)
    3. Verify validation message or truncation
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://app.example.com/login"), "Login page URL mismatch!"
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Attempt to enter email exceeding max length
    long_email = (
        "a123456789012345678901234567890123456789012345678901234567890123@"
        "b123456789012345678901234567890123456789012345678901234567890123."
        "c123456789012345678901234567890123456789012345678901234567890123."
        "d123456789012345678901234567890123456789012345678.comextra"
    )
    result = login_page.login_with_email_exceeding_max_length(long_email)

    # Step 3: Assert on result
    if result == 'truncated':
        # Input was truncated by the field
        entered_email = driver.find_element(*LoginPage.EMAIL_FIELD).get_attribute("value")
        assert len(entered_email) < len(long_email), (
            f"Expected input to be truncated, but field value is not: {entered_email}"
        )
    elif isinstance(result, str):
        # Validation error message was shown
        assert (
            "maximum" in result.lower() or "length" in result.lower() or "exceeds" in result.lower()
        ), f"Unexpected validation error message: {result}"
    else:
        pytest.fail(
            "Neither input truncation nor validation error detected for email exceeding max length!"
        )
