# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.password_recovery_page = PasswordRecoveryPage(driver)
        self.username_recovery_page = UsernameRecoveryPage(driver)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate_to_login()
        await self.login_page.leave_email_field_empty()
        await self.login_page.enter_valid_password('')
        await self.login_page.click_login_button()
        assert await self.login_page.is_validation_error_displayed('Mandatory fields are required')

    async def test_remember_me_functionality(self):
        await self.login_page.navigate_to_login()
        await self.login_page.enter_email('user@example.com')
        await self.login_page.enter_password('password')
        await self.login_page.click_login()
        assert await self.login_page.is_dashboard_displayed()

    def test_lgn_01_successful_login(self):
        email = 'valid_user@example.com'
        password = 'valid_password'
        result = self.login_page.tc_lgn_01_successful_login(email, password)
        assert result, 'Login failed or Dashboard not displayed.'

    def test_lgn_02_empty_field_submission(self):
        self.login_page.navigate_to_login()
        error_text = self.login_page.submit_empty_login_and_get_mandatory_field_error()
        assert error_text == 'Mandatory fields are required', f"Expected error not shown. Got: {error_text}"

    def test_tc_login_001_valid_login_flow(self):
        url = 'https://ecommerce.example.com/login'
        email = 'testuser@example.com'
        password = 'ValidPass123!'
        result = self.login_page.tc_login_001_valid_login_flow(url, email, password)
        assert result, 'Valid login flow failed: Dashboard/session not established.'

    def test_tc_login_002_invalid_login_flow(self):
        email = 'invaliduser@example.com'
        password = 'SomePassword123'
        result = self.login_page.tc_login_002_invalid_login_flow(email, password)
        assert result, 'Invalid login flow failed: error message or login page validation did not meet criteria.'

    def test_tc_login_003_valid_email_wrong_password(self):
        url = 'https://example-ecommerce.com/login'
        email = 'testuser@example.com'
        password = 'WrongPassword456'
        expected_error = 'Invalid email or password'
        result = self.login_page.tc_login_003_valid_email_wrong_password(url, email, password, expected_error)
        assert result, 'TC-LOGIN-003 failed: error message or login page validation did not meet criteria.'

    def test_tc_login_004_empty_email_valid_password(self):
        """
        TC-LOGIN-004: Attempt login with empty email and valid password
        Steps:
        1. Navigate to the login page [Test Data: URL]
        2. Leave the email field empty [Test Data: Email: (empty)]
        3. Enter valid password [Test Data: Password]
        4. Click on the Login button
        5. Verify validation error is displayed: 'Email is required' or 'Please fill in all required fields'
        6. Verify login is not processed; user remains on login page without authentication
        Acceptance Criteria: TS-003
        """
        url = 'https://ecommerce.example.com/login'
        password = 'ValidPass123!'
        expected_validation = 'Email is required'
        result = self.login_page.tc_login_004_empty_email_valid_password(url, password, expected_validation)
        assert result, 'TC-LOGIN-004 failed: validation error or login page validation did not meet criteria.'

    def test_tc_login_005_valid_email_empty_password(self):
        """
        TC-LOGIN-005: Attempt login with valid email and empty password
        Steps:
        1. Navigate to the login page [Test Data: URL]
        2. Enter valid email address [Test Data: Email: testuser@example.com]
        3. Leave the password field empty [Test Data: Password: (empty)]
        4. Click on the Login button
        5. Verify validation error is displayed: 'Password is required' or 'Please fill in all required fields'
        6. Verify login is not processed; user remains on login page without authentication
        Acceptance Criteria: TS-003
        """
        url = 'https://ecommerce.example.com/login'
        email = 'testuser@example.com'
        expected_validation = 'Password is required'
        result = self.login_page.tc_login_005_valid_email_empty_password(url, email, expected_validation)
        assert result, 'TC-LOGIN-005 failed: validation error or login page validation did not meet criteria.'

    def test_tc_login_006_password_recovery_flow(self):
        """
        TC-LOGIN-006: Password Recovery Flow
        Steps:
        1. Navigate to the login page [URL: https://ecommerce.example.com/login]
        2. Click on the 'Forgot Password' link
        3. Verify password recovery page is displayed with email input field and instructions
        """
        url = 'https://ecommerce.example.com/login'
        recovery_url = 'https://ecommerce.example.com/forgot-password'
        # Step 1: Navigate to login page
        login_page_displayed = self.login_page.navigate_to_login(url)
        assert login_page_displayed, 'Login page not displayed.'
        # Step 2: Click on the Forgot Password link
        forgot_clicked = self.login_page.click_forgot_password()
        assert forgot_clicked, "Could not click 'Forgot Password' link."
        # Step 3: Verify password recovery page is displayed
        is_loaded = self.password_recovery_page.is_loaded()
        assert is_loaded, 'Password recovery page not loaded correctly.'
        email_visible = self.password_recovery_page.is_email_input_visible()
        assert email_visible, 'Email input field not visible on recovery page.'
        instructions_visible = self.password_recovery_page.is_instructions_visible()
        assert instructions_visible, 'Instructions not visible on recovery page.'

    def test_tc_login_007_username_recovery_flow(self):
        """
        TC-LOGIN-007: Username Recovery Flow
        Steps:
        1. Navigate to the login page [URL: https://ecommerce.example.com/login]
        2. Click on the 'Forgot Username' link
        3. Verify username recovery page is displayed with appropriate input fields and instructions
        Acceptance Criteria: TS-005
        """
        login_url = 'https://ecommerce.example.com/login'
        username_recovery_url = 'https://ecommerce.example.com/forgot-username'
        # Step 1: Navigate to login page
        self.login_page.go_to()
        assert self.login_page.is_loaded(), "Login page not loaded or 'Forgot Username' link not visible."
        # Step 2: Click on 'Forgot Username' link
        self.login_page.click_forgot_password()  # Assuming click_forgot_password handles both username/password recovery links
        # Step 3: Verify username recovery page is displayed
        self.username_recovery_page.go_to()
        assert self.username_recovery_page.is_loaded(), "Username recovery page not loaded or instructions not visible."
