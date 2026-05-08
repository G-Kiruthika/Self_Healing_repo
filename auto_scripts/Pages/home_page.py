# auto_scripts/Pages/home_page.py

from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class HomePage(BasePage):
    """Represents the UnionDigital Bank homepage."""

    # Locators
    LOAN_PAYMENT_GUIDES_LINK = ('placeholder', 'locator_for_loan_payment_guides_link')

    def __init__(self, driver):
        super().__init__(driver)

    def click_loan_payment_guides(self):
        """Clicks on the 'Loan Payment Guides' link."""
        self.click(self.LOAN_PAYMENT_GUIDES_LINK)
