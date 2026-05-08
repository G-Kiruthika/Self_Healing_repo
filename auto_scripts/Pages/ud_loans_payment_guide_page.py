# auto_scripts/Pages/ud_loans_payment_guide_page.py

from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class UdLoansPaymentGuidePage(BasePage):
    """Represents the UD Loans Payment Guide page."""

    # Locators
    UPAY_PAYMENT_OPTION = ('placeholder', 'locator_for_upay_payment_option')
    HOW_TO_PAY_YOUR_UD_LOANS_TEXT = ('placeholder', 'locator_for_how_to_pay_your_ud_loans_text')
    PLUS_ICON_RIGHT_OF_TEXT = ('placeholder', 'locator_for_plus_icon_right_of_text')

    def __init__(self, driver):
        super().__init__(driver)

    def verify_upay_payment_option_visible(self):
        """Verifies that the UPAY payment option is visible."""
        return self.is_visible(self.UPAY_PAYMENT_OPTION)

    def locate_how_to_pay_your_ud_loans_text(self):
        """Locates the 'How To Pay Your UD Loans' text."""
        return self.find(self.HOW_TO_PAY_YOUR_UD_LOANS_TEXT)

    def verify_plus_icon_displayed_right_of_text(self):
        """Verifies '+' icon is displayed to the right of the text."""
        return self.is_visible(self.PLUS_ICON_RIGHT_OF_TEXT)
