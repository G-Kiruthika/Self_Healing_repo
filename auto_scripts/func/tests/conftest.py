# auto_scripts/func/tests/conftest.py

import pytest
import os
import yaml
from datetime import datetime
from auto_scripts.func.core.driver_factory import get_driver

def pytest_configure(config):
    os.makedirs("auto_scripts/func/reports/screenshots", exist_ok=True)
    os.makedirs("auto_scripts/func/logs", exist_ok=True)

@pytest.fixture(scope="session")
def config_data():
    with open('auto_scripts/func/config/config.yaml') as f:
        return yaml.safe_load(f)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = None
        for fixture_name in item.fixturenames:
            if 'driver' in fixture_name or 'setup' in fixture_name:
                try:
                    fixture_value = item.funcargs.get(fixture_name)
                    if hasattr(fixture_value, '__iter__') and not isinstance(fixture_value, str):
                        for val in fixture_value:
                            if hasattr(val, 'save_screenshot'):
                                driver = val
                                break
                    elif hasattr(fixture_value, 'save_screenshot'):
                        driver = fixture_value
                        break
                except:
                    pass
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(
                "auto_scripts/func/reports/screenshots",
                screenshot_name
            )
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
