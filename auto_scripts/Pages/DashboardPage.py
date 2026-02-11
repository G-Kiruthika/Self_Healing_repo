# DashboardPage.py
# Automated PageClass for post-login dashboard validation (TC_LOGIN_001)

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.dashboard_header = (By.CSS_SELECTOR, 'h1.dashboard-title')
        self.user_profile_icon = (By.CSS_SELECTOR, '.user-profile-name')

    def is_dashboard_displayed(self):
        """
        Validate dashboard page is displayed
        """
        try:
            return self.driver.find_element(*self.dashboard_header).is_displayed()
        except NoSuchElementException:
            return False

    def is_user_profile_icon_displayed(self):
        """
        Validate user profile icon is visible
        """
        try:
            return self.driver.find_element(*self.user_profile_icon).is_displayed()
        except NoSuchElementException:
            return False

    def validate_dashboard(self):
        """
        Combined validation for dashboard
        """
        assert self.is_dashboard_displayed(), 'Dashboard header not visible after login'
        assert self.is_user_profile_icon_displayed(), 'User profile icon not visible after login'

# Example usage:
# from selenium import webdriver
# driver = webdriver.Chrome()
# dashboard_page = DashboardPage(driver)
# dashboard_page.validate_dashboard()
# print('Dashboard validated: PASSED')
