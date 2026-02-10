from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def is_dashboard_displayed(self):
        """
        Verifies that the dashboard header is visible after login.
        Returns:
            bool: True if dashboard header is visible, False otherwise.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except Exception:
            return False

    def get_dashboard_title(self):
        """
        Returns the text of the dashboard header.
        Returns:
            str: Dashboard title text.
        """
        header_elem = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
        return header_elem.text

    def is_user_profile_icon_visible(self):
        """
        Checks if the user profile icon is visible on dashboard.
        Returns:
            bool: True if visible, False otherwise.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except Exception:
            return False