from pages.LoginPage import LoginPage
from pages.UsernameRecoveryPage import UsernameRecoveryPage
from core.driver_factory import get_driver


def test_login_valid_user():
    driver = get_driver()
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    assert login_page.is_logged_in()
    driver.quit()


def test_login_forgot_username_recovery():
    driver = get_driver()
    login_page = LoginPage(driver)
    login_page.open()
    login_page.click_forgot_username()

    username_recovery_page = UsernameRecoveryPage(driver)
    username_recovery_page.recover_username()

    assert username_recovery_page.is_username_recovery_successful()
    driver.quit()
