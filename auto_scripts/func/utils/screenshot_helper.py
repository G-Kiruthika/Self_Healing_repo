"""Screenshot utility for capturing test failures and evidence."""

import os
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ScreenshotHelper:
    """Helper class for taking and managing screenshots."""

    def __init__(self, driver, screenshot_dir="auto_scripts/func/screenshots"):
        """Initialize ScreenshotHelper.
        
        Args:
            driver: WebDriver instance
            screenshot_dir (str): Directory to store screenshots
        """
        self.driver = driver
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def take_screenshot(self, name="screenshot"):
        """Take screenshot and save to file.
        
        Args:
            name (str): Screenshot name/prefix
        
        Returns:
            str: Path to saved screenshot
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = f"{name}_{timestamp}.png"
            filepath = self.screenshot_dir / filename
            
            self.driver.save_screenshot(str(filepath))
            logger.info(f"Screenshot saved: {filepath}")
            
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return None

    def take_screenshot_on_failure(self, test_name):
        """Take screenshot for failed test.
        
        Args:
            test_name (str): Name of the failed test
        
        Returns:
            str: Path to saved screenshot
        """
        return self.take_screenshot(f"FAILED_{test_name}")

    def take_full_page_screenshot(self, name="full_page"):
        """Take full page screenshot (if supported by browser).
        
        Args:
            name (str): Screenshot name/prefix
        
        Returns:
            str: Path to saved screenshot
        """
        try:
            # Get original window size
            original_size = self.driver.get_window_size()
            
            # Get page dimensions
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            page_width = self.driver.execute_script("return document.body.scrollWidth")
            
            # Set window size to page dimensions
            self.driver.set_window_size(page_width, page_height)
            
            # Take screenshot
            screenshot_path = self.take_screenshot(name)
            
            # Restore original window size
            self.driver.set_window_size(
                original_size['width'],
                original_size['height']
            )
            
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to take full page screenshot: {str(e)}")
            return None
