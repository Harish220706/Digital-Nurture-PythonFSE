"""
Hands-On 6 - test_playground.py
pytest test suite for the LambdaTest Selenium Playground.
Run with: pytest test_playground.py -v --html=report.html --self-contained-html
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# Step 42 + Step 45: form submission test, parameterised with 3 messages
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, base_url, message):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

    driver.find_element(By.ID, "user-message").send_keys(message)
    driver.find_element(By.ID, "showInput").click()

    displayed = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert displayed.text == message


# Step 43: checkbox demo test
def test_checkbox_demo(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Checkbox Demo").click()

    checkbox = driver.find_element(By.ID, "isAgeSelected")
    checkbox.click()
    assert checkbox.is_selected() is True

    checkbox.click()
    assert checkbox.is_selected() is False


# Step 49: dropdown selection test
def test_dropdown_selection(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Select Dropdown List").click()

    dropdown_element = driver.find_element(By.ID, "select-demo")
    select = Select(dropdown_element)
    select.select_by_visible_text("Wednesday")

    selected_option = select.first_selected_option
    assert selected_option.text == "Wednesday"
