# Test Case: TC_LOGIN_001 - Valid Login and Session Verification
# Acceptance Criteria: SCRUM-91
# Traceability: testCaseId=115

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

class TestLoginPageTCLOGIN001(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(5)
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_valid_login_and_session(self):
        # Step 2: Navigate to the login page
        self.login_page.go_to()
        email_field = self.login_page.wait.until(
            lambda d: d.find_element(*LoginPage.EMAIL_FIELD)
        )
        password_field = self.login_page.wait.until(
            lambda d: d.find_element(*LoginPage.PASSWORD_FIELD)
        )
        self.assertTrue(email_field.is_displayed(), "Email field should be displayed on login page.")
        self.assertTrue(password_field.is_displayed(), "Password field should be displayed on login page.")

        # Step 3: Enter valid email address
        test_email = "testuser@example.com"
        self.login_page.enter_email(test_email)
        self.assertEqual(email_field.get_attribute('value'), test_email, "Email input value should match test data.")

        # Step 4: Enter valid password
        test_password = "ValidPass123!"
        self.login_page.enter_password(test_password)
        # Password field should not reveal actual password (masked)
        password_type = password_field.get_attribute('type')
        self.assertEqual(password_type, 'password', "Password field should be of type 'password' (masked).")
        # (Cannot check actual text, but can ensure field is not empty)
        self.assertTrue(password_field.get_attribute('value'), "Password field should not be empty after input.")

        # Step 5: Click on the Login button
        self.login_page.click_login()

        # Step 6: Verify dashboard is loaded
        dashboard_loaded = self.login_page.is_dashboard_loaded()
        self.assertTrue(dashboard_loaded, "Dashboard should load after successful login.")

        # Step 7: Verify user session is created and profile is displayed
        profile_displayed = self.login_page.is_user_profile_displayed()
        self.assertTrue(profile_displayed, "User profile icon should be displayed after login (session created).")

if __name__ == "__main__":
    unittest.main()
