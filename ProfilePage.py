# ProfilePage.py
"""
Page Object for Profile Page using Selenium WebDriver
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProfilePage:
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_profile_name(self):
        profile_elem = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
        return profile_elem.text

    def is_profile_name_displayed(self):
        try:
            profile_elem = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except:
            return False

    def get_session_cookie(self):
        # Returns session cookie if exists
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            if 'session' in cookie['name'].lower():
                return cookie['value']
        return None
