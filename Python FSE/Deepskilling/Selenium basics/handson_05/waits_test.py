"""
Hands-On 5, Task 2 - WebDriverWait and Expected Conditions
"""

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


def test_alert_with_explicit_wait(driver):
    # Step 36: click Success Message button, wait for the alert, assert text
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

    driver.find_element(By.XPATH, "//button[text()='Success Message']").click()

    alert = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "successfully" in alert.text.lower(), f"Unexpected alert text: {alert.text}"
    print("Explicit wait alert text:", alert.text)


def compare_sleep_vs_explicit_wait(driver):
    # Step 37: demonstrate why time.sleep() is worse than an explicit wait
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

    # --- Version A: time.sleep() ---
    start = time.time()
    driver.find_element(By.XPATH, "//button[text()='Success Message']").click()
    time.sleep(3)  # fixed guess - always waits the full 3 seconds, even if
    # the alert appeared in 200ms. On a slow machine/network, 3s might not
    # even be enough, making this both slower AND less reliable.
    alert = driver.find_element(By.CSS_SELECTOR, ".alert-success")
    sleep_duration = time.time() - start
    print(f"time.sleep() version took {sleep_duration:.2f}s, alert text: {alert.text}")

    driver.refresh()

    # --- Version B: explicit wait ---
    start = time.time()
    driver.find_element(By.XPATH, "//button[text()='Success Message']").click()
    alert = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    wait_duration = time.time() - start
    print(f"explicit wait version took {wait_duration:.2f}s, alert text: {alert.text}")
    # On a fast machine, the explicit wait finishes as soon as the element
    # is visible (often well under 3s) - faster than the fixed sleep. On a
    # slow machine, the explicit wait can tolerate delays beyond 3s (up to
    # its own timeout), making it more reliable too.


def test_clickable_wait(driver):
    # Step 38: element_to_be_clickable vs visibility_of_element_located
    # visibility_of_element_located: element exists in the DOM and is
    # rendered/visible (has non-zero size, not display:none) - but it could
    # still be disabled or covered by another element.
    # element_to_be_clickable: everything visibility_of_element_located
    # checks, PLUS the element is enabled and not obscured, so an actual
    # click will succeed.
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Success Message']")
        )
    )
    button.click()
    print("Clicked button once it was confirmed clickable.")


def fluent_wait_for_table_row(driver):
    # Step 39: FluentWait - poll every 500ms, timeout 10s, ignore NoSuchElementException
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Table Sort").click()

    fluent_wait = WebDriverWait(
        driver,
        timeout=10,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException],
    )
    row = fluent_wait.until(
        lambda d: d.find_element(By.CSS_SELECTOR, "table tbody tr")
    )
    print("Found dynamically-loaded table row:", row.text)


if __name__ == "__main__":
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        test_alert_with_explicit_wait(driver)
        compare_sleep_vs_explicit_wait(driver)
        test_clickable_wait(driver)
        fluent_wait_for_table_row(driver)
    finally:
        driver.quit()
