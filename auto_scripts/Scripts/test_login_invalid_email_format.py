# Test Script for TC_LOGIN_020: Invalid Email Format on Login Page
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage

class TestLoginInvalidEmailFormat(unittest.TestCase):
    """
    TestCase ID: TC_LOGIN_020
    Title: Attempt login with invalid email format and verify validation error
    Acceptance Criteria: SCRUM-91
    """

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(5)
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_invalid_email_format(self):
        """
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter email in invalid format (missing @ symbol) [Test Data: Email: testuserexample.com]
        3. Enter valid password [Test Data: Password: ValidPass123!]
        4. Click on the Login button
        5. Validation error 'Please enter a valid email address' is displayed
        """
        # Step 1: Navigate to login page
        self.login_page.go_to_login_page()
        self.assertTrue(self.login_page.is_login_fields_visible(), "Login fields are not visible!")
        self.assertEqual(self.login_page.driver.current_url, self.login_page.LOGIN_URL, "Did not navigate to login page!")

        # Step 2: Enter email in invalid format
        email_entered = self.login_page.enter_email("testuserexample.com")
        self.assertTrue(email_entered, "Email was not entered correctly!")
        email_field = self.login_page.driver.find_element(*self.login_page.EMAIL_FIELD)
        self.assertEqual(email_field.get_attribute("value"), "testuserexample.com", "Email field value mismatch!")

        # Step 3: Enter valid password
        password_entered = self.login_page.enter_password("ValidPass123!")
        self.assertTrue(password_entered, "Password was not entered/masked correctly!")
        password_field = self.login_page.driver.find_element(*self.login_page.PASSWORD_FIELD)
        self.assertEqual(password_field.get_attribute("type"), "password", "Password field is not masked!")

        # Step 4: Click Login button
        self.login_page.click_login()
        time.sleep(1)

        # Step 5: Assert validation error is displayed
        validation_error = None
        try:
            validation_elem = self.login_page.driver.find_element(*self.login_page.VALIDATION_ERROR)
            if validation_elem.is_displayed():
                validation_error = validation_elem.text.strip()
        except NoSuchElementException:
            pass
        self.assertEqual(validation_error, "Please enter a valid email address", f"Expected validation error 'Please enter a valid email address', got: '{validation_error}'")

if __name__ == "__main__":
    unittest.main()
