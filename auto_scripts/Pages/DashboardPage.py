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
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except Exception:
            return False

    def get_dashboard_title(self):
        header_elem = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
        return header_elem.text

    def is_user_profile_icon_visible(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except Exception:
            return False

    # --- TC_LOGIN_002: Remember Me Persistence Verification ---
    def verify_remember_me_persistence(self):
        """
        Verifies that user remains logged in after browser restart by checking dashboard elements.
        Returns:
            bool: True if dashboard and user profile icon are visible, False otherwise.
        """
        try:
            dashboard_header = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            user_profile_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return dashboard_header.is_displayed() and user_profile_icon.is_displayed()
        except Exception:
            return False
