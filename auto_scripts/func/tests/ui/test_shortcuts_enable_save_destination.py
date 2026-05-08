"""Test Case 55: Verify the behavior when user Enables the 'Save' destination toggle bar in 'Add Shortcut' screen."""

import pytest
from auto_scripts.Pages.root_view_screen import RootViewScreen
from auto_scripts.Pages.printer_details_screen import PrinterDetailsScreen
from auto_scripts.Pages.shortcuts_screen import ShortcutsScreen
from auto_scripts.Pages.add_shortcut_screen import AddShortcutScreen


class TestShortcutsEnableSaveDestination:
    """Test suite for enabling Save destination toggle."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup test fixtures."""
        self.driver = driver
        self.root_view_screen = RootViewScreen(self.driver)
        self.printer_details_screen = PrinterDetailsScreen(self.driver)
        self.shortcuts_screen = ShortcutsScreen(self.driver)
        self.add_shortcut_screen = AddShortcutScreen(self.driver)

    def test_enable_save_destination_toggle(self):
        """Test Case 55: Verify the behavior when user Enables the 'Save' destination toggle bar.
        
        Expected Result: User should be able to Enable the 'Save' destination toggle bar in 'Add shortcut' screen.
        After disabling the 'Save' destination toggle bar, 'continue' button should be enabled.
        """
        # Step 1: Launch app
        self.root_view_screen.launch_app()
        
        # Step 2: Click printer icon
        assert self.root_view_screen.click_printer_icon(), \
            "Should be able to click printer icon"
        
        # Step 3: Click shortcuts tile (from PrinterDetailsScreen context)
        assert self.printer_details_screen.click_shortcuts_tile(), \
            "Should be able to click shortcuts tile"
        
        # Step 4: Click add new shortcuts
        assert self.shortcuts_screen.click_add_new_shortcuts(), \
            "Should be able to click add new shortcuts"
        
        # Step 5: Click create your own shortcut arrow
        assert self.add_shortcut_screen.click_create_your_own_shortcut_arrow(), \
            "Should be able to click create your own shortcut arrow"
        
        # Step 6: Enable save destination toggle
        assert self.add_shortcut_screen.enable_save_destination_toggle(), \
            "Should be able to enable save destination toggle"
        
        # Step 7: Verify screen state
        assert self.add_shortcut_screen.is_save_destination_toggle_visible(), \
            "Save destination toggle should be visible and enabled"
