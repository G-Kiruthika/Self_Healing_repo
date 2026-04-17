# Existing imports and code...
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PasswordRecoveryPage import PasswordRecoveryPage

# ... (existing test methods remain unchanged)

def test_TC_LOGIN_010_password_recovery_link_and_page_elements(driver, base_url):
    """
    TC_LOGIN_010: Verify 'Forgot Password' link and Password Recovery page elements.
    Steps:
    1. Navigate to login page
    2. Verify Forgot Password link is present and visible
    3. Click Forgot Password link
    4. Verify redirection to Password Recovery page
    5. Verify Password Recovery page elements (email field, submit button, etc.)
    Acceptance:
    - Forgot Password link is present and clickable
    - Redirection to correct Password Recovery page
    - All required elements are visible and enabled
    """
    # Step 1: Navigate to login page
    login_url = f"{base_url}/login"
    driver.get(login_url)

    # Step 2: Verify Forgot Password link
    forgot_link_locator = (By.LINK_TEXT, "Forgot Password?")
    forgot_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(forgot_link_locator)
    )
    assert forgot_link.is_displayed(), "Forgot Password link is not visible"
    assert forgot_link.is_enabled(), "Forgot Password link is not enabled"

    # Step 3: Click Forgot Password
    forgot_link.click()

    # Step 4: Verify redirection to Password Recovery page
    recovery_url_part = "/password-recovery"
    WebDriverWait(driver, 10).until(
        EC.url_contains(recovery_url_part)
    )
    assert recovery_url_part in driver.current_url, "Did not redirect to Password Recovery page"

    # Step 5: Verify password recovery page elements
    recovery_page = PasswordRecoveryPage(driver)
    assert recovery_page.is_email_field_present(), "Email field is not present on Password Recovery page"
    assert recovery_page.is_submit_button_present(), "Submit button is not present on Password Recovery page"
    assert recovery_page.is_email_field_enabled(), "Email field is not enabled"
    assert recovery_page.is_submit_button_enabled(), "Submit button is not enabled"
    # Optionally check for additional elements if defined in PasswordRecoveryPage
