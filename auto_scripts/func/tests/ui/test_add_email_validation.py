"""Test suite for Add Email Validation feature."""

from pages.hpx_app_launch_page import HpxAppLaunchPage
from pages.printer_details_page import PrinterDetailsPage
from pages.add_shortcuts_page import AddShortcutsPage
from pages.add_email_page import AddEmailPage
from core.driver_factory import get_driver


def test_invalid_email_in_add_email_screen():
    """Test Case 66: Verify error message is displayed when invalid email is entered in Add Email screen."""
    driver = get_driver()
    
    try:
        # Initialize page objects
        hpx_launch_page = HpxAppLaunchPage(driver)
        printer_details_page = PrinterDetailsPage(driver)
        add_shortcuts_page = AddShortcutsPage(driver)
        add_email_page = AddEmailPage(driver)
        
        # Test data
        invalid_email = "invalid@example"
        
        # Test flow
        hpx_launch_page.launch_app()
        printer_details_page.navigate_to_printer_details()
        add_shortcuts_page.navigate_to_add_shortcuts()
        add_shortcuts_page.enable_email_destination()
        add_shortcuts_page.click_continue()
        add_email_page.enter_email_address(invalid_email)
        add_email_page.click_add_to_shortcut()
        
        # Assertion
        assert add_email_page.verify_error_message(), "Error message should be displayed for invalid email"
        
    finally:
        driver.quit()


def test_multiple_emails_in_add_email_screen():
    """Test Case 67: Verify shortcut is saved successfully when multiple valid emails are entered in Add Email screen."""
    driver = get_driver()
    
    try:
        # Initialize page objects
        hpx_launch_page = HpxAppLaunchPage(driver)
        printer_details_page = PrinterDetailsPage(driver)
        add_shortcuts_page = AddShortcutsPage(driver)
        add_email_page = AddEmailPage(driver)
        
        # Test data
        multiple_emails = "user1@example.com,user2@example.com"
        
        # Test flow
        hpx_launch_page.launch_app()
        printer_details_page.navigate_to_printer_details()
        add_shortcuts_page.navigate_to_add_shortcuts()
        add_shortcuts_page.enable_email_destination()
        add_shortcuts_page.click_continue()
        add_email_page.enter_email_address(multiple_emails)
        add_email_page.click_add_to_shortcut()
        
        # Assertion
        assert add_email_page.verify_shortcut_saved(), "Shortcut should be saved successfully for multiple valid emails"
        
    finally:
        driver.quit()
