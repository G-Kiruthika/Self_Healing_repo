# auto_scripts/func/tests/ui/test_loan_payment_guides.py

import pytest
from auto_scripts.Pages.home_page import HomePage
from auto_scripts.Pages.loan_payment_guides_page import LoanPaymentGuidesPage
from auto_scripts.Pages.ud_loans_payment_guide_page import UdLoansPaymentGuidePage
from auto_scripts.func.core.driver_factory import get_driver
import yaml

class TestLoanPaymentGuides:
    """Test suite for Loan Payment Guides functionality."""

    @pytest.fixture(scope="function")
    def setup(self):
        """Setup driver and load configuration."""
        with open('auto_scripts/func/config/config.yaml') as f:
            config = yaml.safe_load(f)
        driver = get_driver(browser=config['ui']['browser'])
        driver.maximize_window()
        driver.implicitly_wait(config['ui']['implicit_wait'])
        yield driver, config
        driver.quit()

    def test_scrum_23804_ts_003_tc_001(self, setup):
        """
        Test Case - SCRUM-23804 TS-003 TC-001
        Verify '+' icon expands payment options on UD Loans Payment Guide page.
        """
        driver, config = setup
        base_url = config['ui']['base_url']
        driver.get(base_url)
        home_page = HomePage(driver)
        home_page.click_loan_payment_guides_link()
        loan_payment_guides_page = LoanPaymentGuidesPage(driver)
        loan_payment_guides_page.click_ud_loans_link()
        ud_loans_page = UdLoansPaymentGuidePage(driver)
        how_to_pay_section = ud_loans_page.locate_how_to_pay_section()
        assert how_to_pay_section is not None, "How To Pay section not found"
        ud_loans_page.click_expand_payment_options_icon()
        assert ud_loans_page.is_element_visible(ud_loans_page.UPAY_SECTION), "Payment option details not displayed after clicking expand icon"

    def test_scrum_23804_ts_004_tc_001(self, setup):
        """
        Test Case - SCRUM-23804 TS-004 TC-001
        Verify UPAY payment link is visible after expanding payment options.
        """
        driver, config = setup
        base_url = config['ui']['base_url']
        driver.get(base_url)
        home_page = HomePage(driver)
        home_page.click_loan_payment_guides_link()
        loan_payment_guides_page = LoanPaymentGuidesPage(driver)
        loan_payment_guides_page.click_ud_loans_link()
        ud_loans_page = UdLoansPaymentGuidePage(driver)
        ud_loans_page.click_expand_payment_options_icon()
        upay_section = ud_loans_page.locate_upay_section()
        assert upay_section is not None, "UPAY section not found"
        assert ud_loans_page.verify_upay_link_displayed(), "'Click here to pay via UPAY' link is not visible"
