# Test Script for TC_LOGIN_014: XSS in Password Field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException
import time

from auto_scripts.Pages.LoginPage import LoginPage

def get_webdriver():
    # You may configure WebDriver as needed
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver

@pytest.mark.security
@pytest.mark.login
@pytest.mark.tc_login_014
class TestLoginXSSPasswordField:
    def setup_method(self):
        self.driver = get_webdriver()
        self.login_page = LoginPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_xss_in_password_field(self):
        """
        TC_LOGIN_014: Attempt login with XSS script payload in password field and verify that:
        - Password is masked
        - Login fails safely
        - Script is NOT executed (no alert popup)
        - XSS attack is prevented
        """
        email = "testuser@example.com"
        xss_payload = "<script>alert('XSS')</script>"

        # Step 1: Navigate to login page
        self.login_page.go_to_login_page()
        assert self.login_page.is_login_fields_visible(), "Login fields not visible."

        # Step 2: Enter valid email
        assert self.login_page.enter_email(email), "Email not accepted in field."

        # Step 3: Enter XSS payload in password field
        assert self.login_page.enter_password(xss_payload), "Password field is not masked or input failed."

        # Step 4: Click Login
        self.login_page.click_login()
        time.sleep(1)

        # Assert: Error message is displayed (login fails)
        assert self.login_page.is_error_message_displayed(), "Error message not displayed after XSS attempt."
        assert self.driver.current_url == self.login_page.LOGIN_URL, "Did not remain on login page after XSS attempt."

        # Assert: Password field remains masked
        password_field = self.driver.find_element(*self.login_page.PASSWORD_FIELD)
        assert password_field.get_attribute("type") == "password", "Password input is not masked."

        # Assert: No alert is triggered (XSS not executed)
        alert_triggered = False
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if "XSS" in alert_text:
                alert_triggered = True
                alert.dismiss()
        except NoAlertPresentException:
            pass
        except Exception:
            pass
        assert not alert_triggered, "XSS alert was triggered! Vulnerability present."

        # Final: Use PageClass method for full coverage
        assert self.login_page.login_with_xss_in_password_field(email, xss_payload), "PageClass XSS login method did not pass all checks."
