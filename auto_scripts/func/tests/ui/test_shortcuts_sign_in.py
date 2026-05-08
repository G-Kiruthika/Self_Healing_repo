"""Test Case 72: Verify the screen when user clicks on 'Sign in' link of any cloud accounts under Add accounts in 'Add save' screen."""

import pytest
from pages.root_view_screen import RootViewScreen
from pages.device_details_page import DeviceDetailsPage
from pages.shortcuts_screen import ShortcutsScreen
from pages.create_shortcut_screen import CreateShortcutScreen
from pages.add_save_screen import AddSaveScreen


class TestShortcutsSignIn:
    """Test suite for shortcuts sign-in functionality."""

    def test_sign_in_link_cloud_accounts(self, driver):
        """Test Case 72: Verify sign-in behavior for cloud accounts in Add save screen.
        
        Steps:
        1. Launch the application
        2. Click on printer icon from root view
        3. Click on shortcuts tile from device details page
        4. Click on add new shortcuts button
        5. Click on create own shortcut arrow
        6. Navigate to Add save screen
        7. Click on sign-in link
        8. Verify user can sign in with desired cloud accounts
        
        Expected Result:
        User should be able to signed in with the desired cloud accounts.
        """
        # Initialize page objects
        root_view = RootViewScreen(driver)
        device_details = DeviceDetailsPage(driver)
        shortcuts_screen = ShortcutsScreen(driver)
        create_shortcut = CreateShortcutScreen(driver)
        add_save_screen = AddSaveScreen(driver)
        
        # Step 1: Launch app (handled by conftest fixture)
        # Verify root view is loaded
        assert root_view.is_printer_icon_visible(), "Printer icon should be visible on root view"
        
        # Step 2: Click printer icon
        root_view.click_printer_icon()
        
        # Step 3: Click shortcuts tile
        assert device_details.is_shortcuts_tile_visible(), "Shortcuts tile should be visible"
        device_details.click_shortcuts_tile()
        
        # Step 4: Click add new shortcuts button
        assert shortcuts_screen.is_add_new_shortcuts_button_visible(), "Add new shortcuts button should be visible"
        shortcuts_screen.click_add_new_shortcuts_button()
        
        # Step 5: Click create own shortcut arrow
        assert create_shortcut.is_create_own_shortcut_arrow_visible(), "Create own shortcut arrow should be visible"
        create_shortcut.click_create_own_shortcut_arrow()
        
        # Step 6: Navigate to Add save screen (implicit navigation)
        # Step 7: Click sign-in link
        assert add_save_screen.is_sign_in_link_visible(), "Sign-in link should be visible on Add save screen"
        add_save_screen.click_sign_in_link()
        
        # Step 8: Verify sign-in behavior
        # Note: Actual verification depends on cloud account sign-in flow
        # This is a placeholder for the verification logic
        # In real implementation, this would check for successful sign-in indicators
        # such as redirects, authentication tokens, or UI changes
        
        # Expected Result: User should be able to sign in with desired cloud accounts
        # Add appropriate assertions based on your application's sign-in behavior
        # Example: assert add_save_screen.is_signed_in(), "User should be signed in successfully"
