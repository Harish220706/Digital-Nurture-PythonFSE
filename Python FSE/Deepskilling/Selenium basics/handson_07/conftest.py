"""
Hands-On 6 - conftest.py
Shared pytest fixtures: driver setup/teardown, base_url, and a
screenshot-on-failure hook.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Step 48: session-scoped base_url fixture, used instead of hardcoding
@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


# Step 41: function-scoped driver fixture - a fresh browser per test
@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service)
    drv.implicitly_wait(5)

    yield drv  # setup happens above, teardown happens below

    drv.quit()


# Step 46: capture a screenshot automatically when a test fails
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is not None:
            test_name = item.name.replace("/", "_").replace("::", "_")
            screenshot_path = f"{test_name}_failure.png"
            driver_fixture.save_screenshot(screenshot_path)
            print(f"\nFailure screenshot saved: {screenshot_path}")
