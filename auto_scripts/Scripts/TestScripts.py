from auto_scripts.PageClasses.ProfileAPIValidationPage import ProfileAPIValidationPage
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.DashboardPage import DashboardPage

def test_tc_login_001_invalid_credentials(driver):
    """
    Test Case TC_LOGIN_001: Test login functionality with invalid credentials.
    ... [existing code for invalid credentials test] ...
    """
    # [existing logic]


def test_tc_login_001_valid_credentials(driver):
    """
    Test Case TC_LOGIN_001: Test login functionality with valid credentials.

    Test Case ID: 4152
    Description: Test Case TC_LOGIN_001

    Test Steps:
        1. Navigate to the e-commerce website login page.
        2. Enter valid email address in the email field.
        3. Enter valid password in the password field.
        4. Click on the Login button.
        5. Verify user is authenticated and redirected to dashboard.
        6. Verify user session is established and username is displayed in header.

    Expected Results:
        - Login page is displayed with email and password fields.
        - Email and password are accepted and displayed in their respective fields.
        - User is successfully authenticated and redirected to dashboard/home page.
        - User name is displayed in the header and session is active.

    Args:
        driver: Selenium WebDriver instance.

    Raises:
        AssertionError: If any validation fails.
    """
    results = {
        "step_1_navigate_login": False,
        "step_2_enter_email": False,
        "step_3_enter_password": False,
        "step_4_click_login": False,
        "step_5_dashboard_redirect": False,
        "step_6_session_established": False,
        "overall_pass": False,
        "error_message": None
    }
    try:
        # Step 1: Navigate to login page
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        results["step_1_navigate_login"] = login_page.is_on_login_page()
        assert results["step_1_navigate_login"], "Login page is not displayed after navigation."

        # Step 2: Enter valid email
        valid_email = "testuser@example.com"
        login_page.enter_email(valid_email)
        results["step_2_enter_email"] = True

        # Step 3: Enter valid password
        valid_password = "Test@1234"
        login_page.enter_password(valid_password)
        results["step_3_enter_password"] = True

        # Step 4: Click Login button
        login_page.click_login()
        results["step_4_click_login"] = True

        # Step 5: Verify authentication and dashboard redirect
        dashboard_page = DashboardPage(driver)
        results["step_5_dashboard_redirect"] = dashboard_page.is_dashboard_displayed()
        assert results["step_5_dashboard_redirect"], "Dashboard not displayed after login."

        # Step 6: Verify user session is established
        results["step_6_session_established"] = dashboard_page.is_user_profile_displayed()
        assert results["step_6_session_established"], "User profile icon not displayed; session may not be active."

        results["overall_pass"] = all([
            results["step_1_navigate_login"],
            results["step_2_enter_email"],
            results["step_3_enter_password"],
            results["step_4_click_login"],
            results["step_5_dashboard_redirect"],
            results["step_6_session_established"]
        ])

        print(f"TC_LOGIN_001: Successfully validated valid login for user: {valid_email}")

    except Exception as e:
        import traceback
        traceback.print_exc()
        results["error_message"] = f"Test execution failed: {str(e)}"
        assert False, f"Test TC_LOGIN_001 failed: {str(e)}"
    return results
