"""Test script for verifying cancel email shortcut removal functionality."""

from pages.hpx_app import HpxApp
from pages.printer_details_screen import PrinterDetailsScreen
from pages.shortcuts_screen import ShortcutsScreen
from core.driver_factory import get_driver


def test_verify_cancel_email_shortcut_removal():
    """Test case to verify canceling email shortcut removal."""
    driver = get_driver()
    
    try:
        # Initialize page objects
        hpx_app = HpxApp(driver)
        printer_details_screen = PrinterDetailsScreen(driver)
        shortcuts_screen = ShortcutsScreen(driver)
        
        # Test flow execution
        hpx_app.install_and_launch_app()
        printer_details_screen.navigate_to_printer_details_screen()
        shortcuts_screen.click_edit_link()
        shortcuts_screen.click_email_shortcut_edit_icon()
        shortcuts_screen.click_cancel_button()
        
        # Assertion
        assert shortcuts_screen.verify_screen(), "Shortcuts screen verification failed after cancel"
        
    finally:
        driver.quit()
