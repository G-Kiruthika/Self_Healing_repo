"""Test script for verifying cloud account sign-in functionality in Add Save screen.

Test Case ID: 72
Description: Verify the screen, when user click on 'Sign in' link of any cloud accounts 
under Add accounts in 'Add save' screen.
"""

import pytest
from pages.root_view_screen import RootViewScreen
from pages.device_details_page import DeviceDetailsPage
from pages.shortcuts_screen import ShortcutsScreen
from pages.create_shortcut_screen import CreateShortcutScreen
from pages.add_save_screen import AddSaveScreen
from core.driver_factory import get_driver


class TestShortcutsCloudSignIn:
    """Test class for cloud account sign-in in shortcuts flow."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup test fixture with driver."""
        self.driver = driver
        yield

    def test_verify_cloud_account_signin_from_add_save_screen(self):
        """Test Case 72: Verify cloud account sign-in from Add Save screen.
        
        Steps:
        1. Launch the application
        2. Click on printer icon
        3. Click on shortcuts tile
        4. Click on add new shortcuts button
        5. Click on create own shortcut arrow
        6. Navigate to Add Save screen
        7. Click on sign in link
        8. Verify sign in behavior
        
        Expected Result:
        User should be able to signed in with the desired cloud accounts.
        """
        # Step 1: Launch app
        root_view = RootViewScreen(self.driver)
        root_view.launch_app()
        
        # Step 2: Click printer icon
        root_view.click_printer_icon()
        
        # Step 3: Click shortcuts tile
        device_details = DeviceDetailsPage(self.driver)
        device_details.click_shortcuts_tile()
        
        # Step 4: Click add new shortcuts button
        shortcuts_screen = ShortcutsScreen(self.driver)
        shortcuts_screen.click_add_new_shortcuts_button()
        
        # Step 5: Click create own shortcut arrow
        create_shortcut = CreateShortcutScreen(self.driver)
        create_shortcut.click_create_own_shortcut_arrow()
        
        # Step 6: Navigate to Add Save screen
        add_save_screen = AddSaveScreen(self.driver)
        add_save_screen.navigate()
        
        # Step 7: Click sign in link
        add_save_screen.click_sign_in_link()
        
        # Step 8: Verify sign in behavior
        result = add_save_screen.verify_sign_in_behavior()
        assert result, "User should be able to sign in with the desired cloud accounts"
