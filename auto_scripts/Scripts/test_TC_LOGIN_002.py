# test_TC_LOGIN_002.py
"""
Automated Selenium Test Script for TC-LOGIN-008 (Negative Login: Unregistered Email)
- Validates error message and user stays on login page.
- Production ready, pytest compatible, robust assertions.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.TC_LOGIN_002_TestPage import TC_LOGIN_002_TestPage

@pytest.mark.login
@pytest.mark.negative
class TestLoginNegative:
    @pytest.fixture(scope='class')
    def driver(self, request):
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)
        request.addfinalizer(lambda: driver.quit())
        return driver

    def test_tc_login_002_unregistered_email(self, driver):
        """
        Test Case TC-LOGIN-008:
        Steps:
        1. Navigate to login page
        2. Enter unregistered email
        3. Enter any password
        4. Click Login
        5. Validate error message and user remains on login page
        """
        invalid_email = "unregistered@example.com"
        password = "AnyPass123!"
        test_page = TC_LOGIN_002_TestPage(driver)
        results = test_page.run_tc_login_002(invalid_email, password)

        # Step 1: Login page displayed
        assert results["step_1_navigate_login"], "Step 1 failed: Login page not displayed."
        # Step 2: Email accepted
        assert results["step_2_enter_email"], "Step 2 failed: Unable to enter email."
        # Step 3: Password accepted
        assert results["step_3_enter_password"], "Step 3 failed: Unable to enter password."
        # Step 4: Login button clicked
        assert results["step_4_click_login"], "Step 4 failed: Unable to click login."
        # Step 5: Error message validation
        assert results["step_5_error_message"] is not None, "Step 5 failed: Error message not displayed."
        assert "invalid email or password" in results["step_5_error_message"].lower(), f"Step 5 failed: Unexpected error message: {results['step_5_error_message']}"
        # Step 6: User remains on login page
        assert results["step_6_on_login_page"], "Step 6 failed: User did not remain on login page after failed login."
        # Overall pass
        assert results["overall_pass"], f"Test failed: {results['exception']}"
