"""
Test Suite: AddShortcutEmailDestination
Test Case ID: 63
Description: Verify the screen when the user enables only the 'Email' destination in the 'Add Shortcut' screen.
"""

import pytest
from auto_scripts.Pages.RootViewScreen import RootViewScreen
from auto_scripts.Pages.DeviceDetailsPage import DeviceDetailsPage
from auto_scripts.Pages.ShortcutsScreen import ShortcutsScreen
from auto_scripts.Pages.CreateShortcutScreen import CreateShortcutScreen
from auto_scripts.Pages.AddShortcutScreen import AddShortcutScreen


def test_verify_email_destination_screen(driver):
    """
    Test Case ID: 63
    Verify the screen when the user enables only the 'Email' destination in the 'Add Shortcut' screen.
    
    Steps:
    1. Install and Launch the HPX app
    2. Click on the printer icon on the root view screen
    3. Click on the shortcuts tile on the device details page
    4. Click on the Add new shortcuts in shortcuts screen
    5. Click on the Create your own shortcut arrow button
    6. Enable only the 'Email' destination toggle bar in 'Add Shortcut' screen
    7. Click on the Continue button
    8. Verify the screen
    
    Expected Result: User should be navigated to the 'Add Email' screen.
    """
    
    # Step 1: Install and Launch the HPX app (handled by conftest fixture)
    # Driver is already initialized and app is launched
    
    # Step 2: Click on the printer icon on the root view screen
    root_view_screen = RootViewScreen(driver)
    root_view_screen.click_printer_icon()
    
    # Step 3: Click on the shortcuts tile on the device details page
    device_details_page = DeviceDetailsPage(driver)
    device_details_page.click_shortcuts_tile()
    
    # Step 4: Click on the Add new shortcuts in shortcuts screen
    shortcuts_screen = ShortcutsScreen(driver)
    shortcuts_screen.click_add_new_shortcut()
    
    # Step 5: Click on the Create your own shortcut arrow button
    create_shortcut_screen = CreateShortcutScreen(driver)
    create_shortcut_screen.click_create_your_own_arrow()
    
    # Step 6: Enable only the 'Email' destination toggle bar in 'Add Shortcut' screen
    add_shortcut_screen = AddShortcutScreen(driver)
    add_shortcut_screen.enable_email_destination_toggle()
    
    # Step 7: Click on the Continue button
    add_shortcut_screen.click_continue()
    
    # Step 8: Verify the screen
    add_shortcut_screen.verify_screen()
