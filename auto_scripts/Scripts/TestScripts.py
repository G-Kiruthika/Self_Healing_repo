# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

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
        """
        LGN-01: Verify successful login with valid credentials
        Steps:
        1. Navigate to login page
        2. Enter valid email and password
        3. Click Login button
        4. Verify redirection to Dashboard
        """
        email = 'valid_user@example.com'  # Replace with actual valid test email
        password = 'valid_password'       # Replace with actual valid test password
        result = self.login_page.tc_lgn_01_successful_login(email, password)
        assert result, 'Login failed or Dashboard not displayed.'

    def test_lgn_02_empty_field_submission(self):
        """
        LGN-02: Verify error for empty field submission
        Steps:
        1. Navigate to login page
        2. Submit login with empty email and password fields
        3. Verify the error message 'Mandatory fields are required' is shown
        """
        self.login_page.navigate_to_login()
        error_text = self.login_page.submit_empty_login_and_get_mandatory_field_error()
        assert error_text == 'Mandatory fields are required', f"Expected error not shown. Got: {error_text}"

    def test_tc_login_001_valid_login_flow(self):
        """
        TC-LOGIN-001: Valid login flow
        Steps:
        1. Navigate to the e-commerce website login page [Test Data: URL]
        2. Enter valid registered email address [Test Data: Email]
        3. Enter correct password [Test Data: Password]
        4. Click on the Login button
        5. Verify user is successfully authenticated and redirected to the dashboard/home page
        6. Verify user session is established (username is displayed in the header and session cookie is set)
        """
        url = 'https://ecommerce.example.com/login'
        email = 'testuser@example.com'
        password = 'ValidPass123!'
        result = self.login_page.tc_login_001_valid_login_flow(url, email, password)
        assert result, 'Valid login flow failed: Dashboard/session not established.'

    def test_tc_login_002_invalid_login_flow(self):
        """
        TC-LOGIN-002: Invalid login flow
        Steps:
        1. Navigate to the login page
        2. Enter an unregistered or invalid email address
        3. Enter any password
        4. Click on the Login button
        5. Verify error message: 'Invalid email or password'
        6. Verify user remains on login page
        """
        email = 'invaliduser@example.com'
        password = 'SomePassword123'
        result = self.login_page.tc_login_002_invalid_login_flow(email, password)
        assert result, 'Invalid login flow failed: error message or login page validation did not meet criteria.'

    def test_tc_login_003_valid_email_wrong_password(self):
        """
        TC-LOGIN-003: Login attempt with valid registered email and incorrect password
        Steps:
        1. Navigate to the login page [Test Data: URL]
        2. Enter valid registered email address [Test Data: Email]
        3. Enter incorrect password [Test Data: Password]
        4. Click on the Login button
        5. Verify error message displayed: 'Invalid email or password'
        6. Verify user remains on login page without authentication
        Acceptance Criteria: TS-002
        """
        url = 'https://example-ecommerce.com/login'
        email = 'testuser@example.com'
        password = 'WrongPassword456'
        expected_error = 'Invalid email or password'
        result = self.login_page.tc_login_003_valid_email_wrong_password(url, email, password, expected_error)
        assert result, 'TC-LOGIN-003 failed: error message or login page validation did not meet criteria.'

    def test_tc_login_004_empty_email_valid_password(self):
        """
        TC-LOGIN-004: Login attempt with empty email field and valid password
        Steps:
        1. Navigate to login page [Test Data: URL]
        2. Leave email field empty [Test Data: Email: (empty)]
        3. Enter valid password [Test Data: Password: ValidPass123!]
        4. Click Login
        5. Verify validation error for empty email ('Email is required' or 'Mandatory fields are required')
        6. Ensure user remains unauthenticated (remains on login page)
        """
        url = 'https://example-ecommerce.com/login'
        password = 'ValidPass123!'
        expected_validation_error = 'Email is required'
        expected_empty_field_prompt = 'Mandatory fields are required'
        result = self.login_page.tc_login_004_empty_email_valid_password(
            url=url,
            password=password,
            expected_validation_error=expected_validation_error,
            expected_empty_field_prompt=expected_empty_field_prompt
        )
        assert result, 'TC-LOGIN-004 failed: validation error or login page validation did not meet criteria.'
