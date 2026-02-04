# Test script for TC_LOGIN_012: Login with 128-character password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_128_char_password(driver):
    """
    TC_LOGIN_012: Enter valid email and 128-char password, click Login, verify acceptance and masking.
    Acceptance Criteria (SCRUM-91):
    - Login page is displayed
    - Email is entered
    - Password is masked and accepted
    - System processes the login attempt appropriately
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    password = "Aa1!Bb2@Cc3#Dd4$Ee5%Ff6^Gg7&Hh8*Ii9(Jj0)Kk1!Ll2@Mm3#Nn4$Oo5%Pp6^Qq7&Rr8*Ss9(Tt0)Uu1!Vv2@Ww3#Xx4$Yy5%Zz6^Aa7&Bb8*Cc9(Dd0)Ee1!Ff2@Gg3#Hh4$"
    assert len(password) == 128, f"Password is not 128 characters, got {len(password)}"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login page is not displayed"

    # Step 2: Enter valid email address
    assert login_page.enter_email(email), "Email was not entered correctly"

    # Step 3: Enter 128-character password
    assert login_page.enter_password(password), "Password was not entered or masked correctly"
    pw_field = driver.find_element(By.ID, "login-password")
    assert pw_field.get_attribute("type") == "password", "Password field is not masked!"
    entered_pw = pw_field.get_attribute("value")
    assert entered_pw == password, "Password input did not match expected value!"

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Optionally verify acceptance and/or error handling
    time.sleep(1)
    error_message = login_page.get_error_message()
    if error_message:
        assert "invalid" not in error_message.lower(), f"Unexpected error message: {error_message}"
    # If no error, test passes acceptance and masking
