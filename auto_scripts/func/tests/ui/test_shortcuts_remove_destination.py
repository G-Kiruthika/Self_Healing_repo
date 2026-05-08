"""Test Case 82: Verify the screen when user removes the 'Save' destination shortcut."""

import pytest
from auto_scripts.Pages.root_view_screen import RootViewScreen
from auto_scripts.Pages.printer_details_screen import PrinterDetailsScreen
from auto_scripts.Pages.shortcuts_screen import ShortcutsScreen
from auto_scripts.Pages.remove_destination_popup import RemoveDestinationPopup


class TestShortcutsRemoveDestination:
    """Test suite for removing Save destination shortcut."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup test fixtures."""
        self.driver = driver
        self.root_view_screen = RootViewScreen(self.driver)
        self.printer_details_screen = PrinterDetailsScreen(self.driver)
        self.shortcuts_screen = ShortcutsScreen(self.driver)
        self.remove_destination_popup = RemoveDestinationPopup(self.driver)

    def test_remove_save_destination_shortcut(self):
        """Test Case 82: Verify the screen when user removes the 'Save' destination shortcut.
        
        Expected Result: Remove this destination?' pop up should be displayed.
        """
        # Step 1: Launch app
        self.root_view_screen.launch_app()
        
        # Step 2: Navigate to PrinterDetailsScreen
        # Navigation logic handled by framework/app flow
        
        # Step 3: Navigate to ShortcutsScreen
        # Navigation logic handled by framework/app flow
        
        # Step 4: Click edit link on PrinterDetailsScreen
        self.printer_details_screen.click_edit_link()
        
        # Step 5: Click edit icon for save shortcut
        self.shortcuts_screen.click_edit_icon_save_shortcut()
        
        # Step 6: Verify popup is displayed
        assert self.remove_destination_popup.verify_popup_displayed(), \
            "Remove destination popup should be displayed"
