# Existing imports
import pytest
from auto_scripts.Pages.TC_SCRUM96_001_TestPage import TC_SCRUM96_001_TestPage
from auto_scripts.Pages.TC_SCRUM96_002_TestPage import TC_SCRUM96_002_TestPage
from auto_scripts.Pages.TC_SCRUM96_003_TestPage import TC_SCRUM96_003_TestPage
from auto_scripts.Pages.TC_SCRUM96_004_TestPage import TC_SCRUM96_004_TestPage
from auto_scripts.Pages.TC_SCRUM96_005_TestPage import TC_SCRUM96_005_TestPage

# Existing tests
@pytest.mark.tc_scrum96_001
def test_tc_scrum96_001(driver):
    page = TC_SCRUM96_001_TestPage(driver)
    results = page.run_tc_scrum96_001(email="user1@example.com", password="Pass123!")
    for step, result in results["step_results"].items():
        assert result["outcome"], f"Step {step} failed: {result['details']}"
    assert results["overall_pass"], "Test failed overall."

@pytest.mark.tc_scrum96_002
def test_tc_scrum96_002(driver):
    page = TC_SCRUM96_002_TestPage(driver)
    results = page.run_tc_scrum96_002(email="user2@example.com", password="Pass456!")
    for step, result in results["step_results"].items():
        assert result["outcome"], f"Step {step} failed: {result['details']}"
    assert results["overall_pass"], "Test failed overall."

@pytest.mark.tc_scrum96_003
def test_tc_scrum96_003(driver):
    page = TC_SCRUM96_003_TestPage(driver)
    results = page.run_tc_scrum96_003(email="user3@example.com", password="Pass789!")
    for step, result in results["step_results"].items():
        assert result["outcome"], f"Step {step} failed: {result['details']}"
    assert results["overall_pass"], "Test failed overall."

@pytest.mark.tc_scrum96_004
def test_tc_scrum96_004(driver):
    page = TC_SCRUM96_004_TestPage(driver)
    results = page.run_tc_scrum96_004(email="user4@example.com", password="PassABC!")
    for step, result in results["step_results"].items():
        assert result["outcome"], f"Step {step} failed: {result['details']}"
    assert results["overall_pass"], "Test failed overall."

# Newly appended test for TC-SCRUM-96-005
@pytest.mark.tc_scrum96_005
def test_tc_scrum96_005(driver):
    """
    TC-SCRUM-96-005: Negative login API test
    Steps:
      1. Register user with email and password
      2. Attempt login with wrong password
      3. Validate 401 response and error message
      4. Ensure no JWT token is returned
    """
    page = TC_SCRUM96_005_TestPage(driver)
    results = page.run_tc_scrum96_005(
        email="login@example.com",
        password="LoginPass123!",
        wrong_password="WrongPassword"
    )
    for step, result in results["step_results"].items():
        assert result["outcome"], f"Step {step} failed: {result['details']}"
    assert results["overall_pass"], "Test failed overall."
