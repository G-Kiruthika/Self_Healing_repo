# auto_scripts/func/utils/report_helper.py

import os
from datetime import datetime

class ReportHelper:
    @staticmethod
    def create_report_directory():
        report_dir = "auto_scripts/func/reports"
        os.makedirs(report_dir, exist_ok=True)
        os.makedirs(f"{report_dir}/screenshots", exist_ok=True)
        return report_dir
    @staticmethod
    def generate_screenshot_name(test_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{test_name}_{timestamp}.png"
    @staticmethod
    def save_screenshot(driver, test_name, directory="auto_scripts/func/reports/screenshots"):
        os.makedirs(directory, exist_ok=True)
        filename = ReportHelper.generate_screenshot_name(test_name)
        filepath = os.path.join(directory, filename)
        driver.save_screenshot(filepath)
        return filepath
