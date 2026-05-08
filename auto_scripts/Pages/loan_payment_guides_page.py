# auto_scripts/Pages/loan_payment_guides_page.py

from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class LoanPaymentGuidesPage(BasePage):
    """Represents the Loan Payment Guides page."""

    # Locators
    UD_LOANS_LINK = ('placeholder', 'locator_for_ud_loans_link')

    def __init__(self, driver):
        super().__init__(driver)

    def click_ud_loans(self):
        """Clicks on the 'UD Loans' link."""
        self.click(self.UD_LOANS_LINK)
