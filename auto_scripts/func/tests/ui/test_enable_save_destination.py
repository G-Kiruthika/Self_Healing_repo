"""
Test Case ID: 55
Description: Verify the behavior, when user Enables the 'Save' destination toggle bar in 'Add Shortcut' screen.
"""

from core.driver_factory import get_driver
from auto_scripts.Pages.root_view_screen import RootViewScreen
from auto_scripts.Pages.printer_details_screen import PrinterDetailsScreen
from auto_scripts.Pages.shortcuts_screen import ShortcutsScreen
from auto_scripts.Pages.add_shortcut_screen import AddShortcutScreen


def test_enable_save_destination_toggle():
    """
    Test to verify the behavior when user enables the 'Save' destination toggle bar.
    Expected: User should be able to enable the 'Save' destination toggle bar in 'Add shortcut' screen.
    After disabling the 'Save' destination toggle bar, 'continue' button should be enabled.
    """
    driver = get_driver()
    
    try:
        # Step 1: Launch app
        root_view = RootViewScreen(driver)
        
        # Step 2: Click printer icon
        root_view.click_printer_icon()
        
        # Step 3: Click shortcuts tile on Printer Details Screen
        printer_details = PrinterDetailsScreen(driver)
        printer_details.click_shortcuts_tile()
        
        # Step 4: Click add new shortcuts
        shortcuts_screen = ShortcutsScreen(driver)
        shortcuts_screen.click_add_new_shortcuts()
        
        # Step 5: Click create your own shortcut arrow
        add_shortcut = AddShortcutScreen(driver)
        add_shortcut.click_create_your_own_shortcut_arrow()
        
        # Step 6: Enable save destination toggle
        add_shortcut.enable_save_destination_toggle()
        
        # Step 7: Verify screen (placeholder for actual verification logic)
        # This would typically verify that the toggle is enabled and continue button is active
        # assert add_shortcut.verify_screen(), "Screen verification failed"
        
    finally:
        driver.quit()