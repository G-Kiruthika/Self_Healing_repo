# tests/ui/test_disable_email_destination_toggle.py

from pages.root_view_screen import RootViewScreen
from pages.device_details_page import DeviceDetailsPage
from pages.shortcuts_screen import ShortcutsScreen
from pages.create_shortcut_screen import CreateShortcutScreen
from pages.add_shortcut_screen import AddShortcutScreen
from core.driver_factory import get_driver


def test_disable_email_destination_toggle():
    """
    Test Case 54: Disable Email Destination Toggle
    
    This test verifies that disabling the email toggle on the Add Shortcut Screen
    disables the Continue button.
    
    Test Flow:
    1. Click printer icon on Root View Screen
    2. Click shortcuts tile on Device Details Page
    3. Click add new shortcut on Shortcuts Screen
    4. Click create own shortcut arrow on Create Shortcut Screen
    5. Disable email toggle on Add Shortcut Screen
    6. Assert that Continue button is disabled
    """
    driver = get_driver()
    
    try:
        # Initialize page objects
        root_view_screen = RootViewScreen(driver)
        device_details_page = DeviceDetailsPage(driver)
        shortcuts_screen = ShortcutsScreen(driver)
        create_shortcut_screen = CreateShortcutScreen(driver)
        add_shortcut_screen = AddShortcutScreen(driver)
        
        # Test flow execution
        root_view_screen.click_printer_icon()
        device_details_page.click_shortcuts_tile()
        shortcuts_screen.click_add_new_shortcut()
        create_shortcut_screen.click_create_own_shortcut_arrow()
        add_shortcut_screen.disable_email_toggle()
        
        # Assertion
        assert add_shortcut_screen.is_continue_button_disabled(), \
            "Continue button should be disabled after disabling email toggle"
    
    finally:
        driver.quit()
