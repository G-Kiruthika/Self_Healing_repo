"""Test script for verifying delete shortcut popup button positions.

Test Case ID: 73
Description: Verify the position of the buttons on the 'Delete this Shortcut?' pop up window.
"""

import pytest
from pages.root_view_screen import RootViewScreen
from pages.shortcuts_screen import ShortcutsScreen
from pages.delete_shortcut_popup import DeleteShortcutPopup
from core.driver_factory import get_driver


class TestShortcutsDeletePopup:
    """Test class for delete shortcut popup button verification."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup test fixture with driver."""
        self.driver = driver
        yield

    def test_verify_delete_popup_button_positions(self):
        """Test Case 73: Verify button positions on Delete Shortcut popup.
        
        Steps:
        1. Launch the application
        2. Navigate to shortcuts screen and click edit link
        3. Click delete icon
        4. Verify buttons position on delete popup
        
        Expected Result:
        The position of the buttons on the 'Delete this Shortcut?' screen should have 
        'Delete' as the primary button and 'Cancel' as the secondary button.
        """
        # Step 1: Launch app
        root_view = RootViewScreen(self.driver)
        root_view.launch_app()
        
        # Step 2: Navigate to shortcuts screen and click edit link
        shortcuts_screen = ShortcutsScreen(self.driver)
        shortcuts_screen.navigate_and_click_edit_link()
        
        # Step 3: Click delete icon
        shortcuts_screen.click_delete_icon()
        
        # Step 4: Verify buttons position
        delete_popup = DeleteShortcutPopup(self.driver)
        result = delete_popup.verify_buttons_position()
        assert result, "Delete button should be primary and Cancel should be secondary"
