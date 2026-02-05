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