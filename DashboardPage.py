# DashboardPage.py
"""
Page Object for Dashboard Page using Selenium WebDriver
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_dashboard_header_displayed(self):
        try:
            dashboard_elem = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except:
            return False
