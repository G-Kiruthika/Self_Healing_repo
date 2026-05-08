"""Pytest configuration and fixtures."""

import pytest
import os
from datetime import datetime
from core.driver_factory import get_driver


@pytest.fixture(scope="function")
def driver():
    """Fixture to provide WebDriver instance for each test.
    
    Yields:
        WebDriver: Configured WebDriver instance
    """
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="session")
def test_config():
    """Fixture to provide test configuration.
    
    Returns:
        dict: Test configuration
    """
    import yaml
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and take screenshots on failure."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call' and report.failed:
        # Get the driver from the test fixture
        driver = item.funcargs.get('driver')
        if driver:
            # Create screenshots directory if it doesn't exist
            screenshots_dir = 'screenshots'
            os.makedirs(screenshots_dir, exist_ok=True)
            
            # Generate screenshot filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshots_dir, screenshot_name)
            
            # Take screenshot
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")


def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )
