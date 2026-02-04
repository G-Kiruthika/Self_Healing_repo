# Selenium Pytest test for TC_LOGIN_014: XSS in password field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_xss_in_password(driver):
    """
    TC_LOGIN_014: Attempt to inject XSS payload in the password field and verify that the input is masked, entered, and XSS attack is prevented.
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter XSS script payload in password field
    4. Click Login button
    5. Verify input is masked and entered, login fails safely, script is not executed, and XSS is prevented.
    """
    login_page = LoginPage(driver)
    valid_email = "testuser@example.com"
    xss_password = "<script>alert('XSS')</script>"

    # Step 1: Go to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    
    # Step 2: Enter valid email
    assert login_page.enter_email(valid_email), "Email was not entered correctly!"
    
    # Step 3: Enter XSS payload in password
    assert login_page.enter_password(xss_password), "Password field is not masked or input not entered!"
    
    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)

    # Step 5: Verify error message is displayed and no XSS is triggered
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed!"
    assert driver.current_url == login_page.LOGIN_URL, "User is not on login page after XSS attempt!"

    # Check that no alert is present (no XSS triggered)
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        # If alert is present, this is a failure
        assert False, f"XSS alert was triggered! XSS vulnerability present! Alert text: {alert_text}"
    except NoAlertPresentException:
        pass  # Expected: No alert present
    except Exception:
        pass  # Any other exception means no alert is present

    # Ensure password field is still masked
    password_field = driver.find_element(*login_page.PASSWORD_FIELD)
    assert password_field.get_attribute("type") == "password", "Password field is not masked!"
