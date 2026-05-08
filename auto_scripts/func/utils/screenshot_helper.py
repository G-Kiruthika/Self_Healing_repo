"""Screenshot utility for capturing test failures and evidence."""

import yaml
from pathlib import Path
from datetime import datetime


class ScreenshotHelper:
    """Helper class for taking and managing screenshots."""
    
    def __init__(self, driver):
        """Initialize ScreenshotHelper.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.config = self._load_config()
        self.screenshots_enabled = self.config.get('screenshots', {}).get('enabled', True)
        self.screenshot_path = self.config.get('screenshots', {}).get('path', 'screenshots/')
        
        # Create screenshots directory
        screenshot_dir = Path(__file__).parent.parent / self.screenshot_path
        screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self):
        """Load configuration from config.yaml."""
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def take_screenshot(self, name=None):
        """Take a screenshot.
        
        Args:
            name: Optional custom name for screenshot
            
        Returns:
            Path to saved screenshot or None
        """
        if not self.screenshots_enabled:
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
        
        screenshot_dir = Path(__file__).parent.parent / self.screenshot_path
        filepath = screenshot_dir / filename
        
        try:
            self.driver.save_screenshot(str(filepath))
            return str(filepath)
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
            return None
    
    def take_screenshot_on_failure(self, test_name):
        """Take screenshot on test failure.
        
        Args:
            test_name: Name of the failed test
            
        Returns:
            Path to saved screenshot or None
        """
        on_failure = self.config.get('screenshots', {}).get('on_failure', True)
        if on_failure:
            return self.take_screenshot(f"failure_{test_name}")
        return None
