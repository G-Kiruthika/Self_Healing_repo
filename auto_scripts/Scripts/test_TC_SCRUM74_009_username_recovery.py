#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Case: TC_SCRUM74_009 - Username Recovery Page UI Validation
Author: Enterprise Test Automation Agent
Traceability: auto_scripts/Pages/UsernameRecoveryPage.py, TC_SCRUM74_009
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import sys
import os

# Ensure PageClass import works regardless of runner location
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from UsernameRecoveryPage import UsernameRecoveryPage

LOGIN_URL = "https://app.example.com/login"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def test_TC_SCRUM74_009_username_recovery_ui(driver):
    """
    Steps:
    1. Navigate to the login page
    2. Click on 'Forgot Username' link
    3. Verify username recovery page elements
    """
    # Step 1: Navigate to login page
    driver.get(LOGIN_URL)
    try:
        forgot_username_link = driver.find_element(By.LINK_TEXT, "Forgot Username")
    except Exception as e:
        pytest.fail(f"[Step 1] 'Forgot Username' link not found: {e}")
    assert forgot_username_link.is_displayed(), "[Step 1] 'Forgot Username' link should be visible"

    # Step 2: Click on 'Forgot Username' link
    forgot_username_link.click()
    # Wait for navigation
    time.sleep(1)  # Could be replaced with WebDriverWait for real-world performance
    assert "forgot-username" in driver.current_url, (
        f"[Step 2] Should be on username recovery page, current URL: {driver.current_url}")

    # Step 3: Verify username recovery page elements using PageClass
    page = UsernameRecoveryPage(driver)
    results = page.verify_recovery_page_elements()
    assert results['email_field_present'], "[Step 3] Email input field should be present on username recovery page"
    assert results['submit_button_present'], "[Step 3] Submit button should be present on username recovery page"
    # Phone field is optional, so only log, not assert
    if results['phone_field_present']:
        print("[Step 3] Phone input field is present (optional)")
    if results['exception']:
        pytest.fail(f"[Step 3] Exception during element validation: {results['exception']}")
    assert results['overall_pass'], "[Step 3] Overall page validation failed: Email and Submit button must be present"

    print("[TC_SCRUM74_009] Username recovery page UI validated successfully.")
