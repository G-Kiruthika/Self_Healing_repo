"""
Test Case ID: 82
Description: Verify the screen, when user removes the 'Save' destination shortcut.
"""

from core.driver_factory import get_driver
from auto_scripts.Pages.root_view_screen import RootViewScreen
from auto_scripts.Pages.printer_details_screen import PrinterDetailsScreen
from auto_scripts.Pages.shortcuts_screen import ShortcutsScreen
from auto_scripts.Pages.remove_destination_popup import RemoveDestinationPopup


def test_remove_save_destination_shortcut():
    """
    Test to verify the screen when user removes the 'Save' destination shortcut.
    Expected: 'Remove this destination?' pop up should be displayed.
    """
    driver = get_driver()
    
    try:
        # Step 1: Launch app
        root_view = RootViewScreen(driver)
        
        # Step 2: Navigate to Printer Details Screen
        printer_details = PrinterDetailsScreen(driver)
        
        # Step 3: Navigate to Shortcuts Screen
        shortcuts_screen = ShortcutsScreen(driver)
        
        # Step 4: Click edit link on Printer Details Screen
        printer_details.click_edit_link()
        
        # Step 5: Click edit icon for save shortcut
        shortcuts_screen.click_edit_icon_save_shortcut()
        
        # Step 6: Verify popup is displayed
        remove_popup = RemoveDestinationPopup(driver)
        assert remove_popup.verify_popup_displayed(), "Remove destination popup should be displayed"
        
    finally:
        driver.quit()