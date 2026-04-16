# TC_LOGIN_002_TestScript.py
"""
Selenium Automation Test Script for TC-LOGIN-002: Negative Login Workflow
Validates login with invalid/unregistered email and asserts error message and page state.
"""
import pytest
from selenium import webdriver
from auto_scripts.Pages.TC_LOGIN_002_TestPage import TC_LOGIN_002_TestPage

@pytest.mark.login
class TestTCLogin002:
    @pytest.fixture(scope="class")
    def driver(self, request):
        # Setup WebDriver (Chrome, can be parameterized)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)
        request.addfinalizer(driver.quit)
        return driver

    def test_invalid_login_shows_error(self, driver):
        """
        Test: Attempt login with invalid email, validate error message and page state.
        """
        # Test Data
        invalid_email = "invaliduser@example.com"
        password = "SomePassword123"
        # Instantiate PageClass
        test_page = TC_LOGIN_002_TestPage(driver, timeout=10)
        # Execute test workflow
        results = test_page.run_tc_login_002(invalid_email, password)
        # Stepwise assertions
        assert results["step_1_navigate_login"], "Login page was not displayed."
        assert results["step_2_enter_email"], "Email could not be entered."
        assert results["step_3_enter_password"], "Password could not be entered."
        assert results["step_4_click_login"], "Login button could not be clicked."
        assert results["step_5_error_message"] is not None, "Error message not displayed."
        assert "invalid email or password" in results["step_5_error_message"].lower(), (
            f"Unexpected error message: {results['step_5_error_message']}"
        )
        assert results["step_6_on_login_page"], "User is not on login page after failed login."
        assert results["overall_pass"], f"Test failed: {results.get('exception', 'Unknown error')}"
