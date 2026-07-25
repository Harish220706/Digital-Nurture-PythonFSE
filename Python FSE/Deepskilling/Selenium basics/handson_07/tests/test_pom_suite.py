"""
Hands-On 7, Task 2 - Full POM-based test suite
Run from the handson_07/ folder: pytest tests/ -v --html=report.html --self-contained-html

Note: zero driver.find_element calls appear below - verify with:
  grep -rn "find_element" tests/
(it should return no matches - all element interaction lives in pages/)
"""

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage


# Step 55: refactored simple form test - reads like a business requirement
def test_simple_form_submission(driver, base_url):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + "simple-form-demo/")
    page.enter_message("Hello Selenium")
    page.click_submit()
    assert page.get_displayed_message() == "Hello Selenium"


# Step 56: refactored checkbox test
def test_checkbox_demo(driver, base_url):
    page = CheckboxPage(driver)
    page.navigate_to(base_url + "checkbox-demo/")

    page.check_option(0)
    assert page.is_option_checked(0) is True

    page.uncheck_option(0)
    assert page.is_option_checked(0) is False


# Step 56: refactored dropdown test
def test_dropdown_selection(driver, base_url):
    page = DropdownPage(driver)
    page.navigate_to(base_url + "select-dropdown-demo/")
    page.select_day("Wednesday")
    assert page.get_selected_day() == "Wednesday"


# Step 57: new Input Form Submit test
def test_input_form_submit(driver, base_url):
    page = InputFormPage(driver)
    page.navigate_to(base_url + "input-form-demo/")
    page.fill_form(
        name="Jane Doe",
        email="jane.doe@example.com",
        phone="9876543210",
        address="221B Baker Street",
    )
    page.submit_form()
    assert "success" in page.get_success_message().lower()
