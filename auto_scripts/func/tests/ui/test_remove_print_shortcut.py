"""Test cases for removing Print destination shortcut."""

from core.driver_factory import get_driver
from pages.hpx_app_launch_page import HPXAppLaunchPage
from pages.printer_details_page import PrinterDetailsPage
from pages.shortcuts_page import ShortcutsPage
from pages.remove_popup_page import RemovePopupPage


def test_verify_remove_popup_displayed():
    """Test Case 76: Verify the screen, when user removes the 'Print' destination shortcut."""
    driver = get_driver()
    
    try:
        # Initialize page objects
        hpx_app_launch_page = HPXAppLaunchPage(driver)
        printer_details_page = PrinterDetailsPage(driver)
        shortcuts_page = ShortcutsPage(driver)
        remove_popup_page = RemovePopupPage(driver)
        
        # Test flow
        hpx_app_launch_page.launch_app()
        assert hpx_app_launch_page.is_remove_popup_displayed(), "App launch popup should be displayed"
        
        printer_details_page.navigate_to_printer_details()
        
        shortcuts_page.navigate_to_shortcuts()
        shortcuts_page.click_edit_link()
        shortcuts_page.click_edit_icon_print_shortcut()
        
        # Validation: 'Remove this destination?' pop up should be displayed
        assert remove_popup_page.is_remove_popup_displayed(), "'Remove this destination?' pop up should be displayed"
        
    finally:
        driver.quit()


def test_verify_print_shortcut_removed():
    """Test Case 77: Verify the screen, when user clicks on the remove button of 'Print' destination shortcut."""
    driver = get_driver()
    
    try:
        # Initialize page objects
        hpx_app_launch_page = HPXAppLaunchPage(driver)
        printer_details_page = PrinterDetailsPage(driver)
        shortcuts_page = ShortcutsPage(driver)
        remove_popup_page = RemovePopupPage(driver)
        
        # Test flow
        hpx_app_launch_page.launch_app()
        
        printer_details_page.navigate_to_printer_details()
        
        shortcuts_page.navigate_to_shortcuts()
        shortcuts_page.click_edit_link()
        shortcuts_page.click_edit_icon_print_shortcut()
        
        remove_popup_page.click_remove_button()
        
        # Validation: User should be redirected to the 'Shortcuts' screen and selected 'Print' destination should be removed
        assert remove_popup_page.is_print_shortcut_removed(), "User should be redirected to the 'Shortcuts' screen and selected 'Print' destination should be removed"
        
    finally:
        driver.quit()
