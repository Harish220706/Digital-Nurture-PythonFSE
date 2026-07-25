"""
Hands-On 5, Task 1 - Locator Strategies - From Simple to Robust

Ranking of locator strategies, most to least preferred (see justification
below each entry):

1. By.ID              - unique per page (in a well-built app), fastest to
                         match, and immune to layout/structure changes.
2. By.NAME             - nearly as reliable as ID, common on form inputs,
                         but less universally present than ID.
3. By.CSS_SELECTOR     - concise, generally faster than XPath, and reads
                         close to how a frontend developer already thinks
                         about the DOM (classes, attributes).
4. By.XPATH (relative,
   attribute-based)     - flexible and can express relationships CSS can't
                         (e.g., text matching, parent traversal), but more
                         verbose and slightly slower than CSS.
5. By.CLASS_NAME / By.TAG_NAME - classes are often reused across many
                         elements (not unique) and tag names match dozens
                         of elements on a real page, so both usually need
                         to be combined with something else to be reliable
                         on their own.
6. By.XPATH (absolute path, e.g. /html/body/div[2]/div[1]/form/input[3])
                         - the least preferred: it hard-codes the exact DOM
                         tree position, so it breaks the instant any
                         ancestor element is added, removed, or reordered.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


def locate_simple_form_message_input(driver):
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

    # Step 32: six locator strategies for the same message input field
    by_id = driver.find_element(By.ID, "user-message")
    by_name = driver.find_element(By.NAME, "message")
    by_class = driver.find_element(By.CLASS_NAME, "form-control")
    by_tag = driver.find_element(By.TAG_NAME, "textarea")
    by_xpath_absolute = driver.find_element(
        By.XPATH, "/html/body/div[3]/div/div[2]/div[2]/div[1]/div/textarea"
    )
    by_xpath_relative = driver.find_element(
        By.XPATH, "//textarea[@id='user-message']"
    )

    for name, element in [
        ("ID", by_id),
        ("NAME", by_name),
        ("CLASS_NAME", by_class),
        ("TAG_NAME", by_tag),
        ("XPATH (absolute)", by_xpath_absolute),
        ("XPATH (relative)", by_xpath_relative),
    ]:
        print(f"Located via {name}: {element.tag_name}")

    # Step 33: three CSS selectors for the same element
    css_by_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
    css_by_attribute = driver.find_element(By.CSS_SELECTOR, "[name='message']")
    css_by_parent_child = driver.find_element(
        By.CSS_SELECTOR, "div.form-group > textarea"
    )

    for name, element in [
        ("CSS by ID", css_by_id),
        ("CSS by attribute", css_by_attribute),
        ("CSS by parent > child", css_by_parent_child),
    ]:
        print(f"Located via {name}: {element.tag_name}")


def locate_checkbox_labels(driver):
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Checkbox Demo").click()

    # Step 34: XPath text() and contains()
    first_option = driver.find_element(By.XPATH, "//label[text()='Option 1']")
    print("Exact text() match:", first_option.text)

    all_options = driver.find_elements(
        By.XPATH, "//label[contains(text(),'Option')]"
    )
    print(f"Found {len(all_options)} labels containing 'Option'")


if __name__ == "__main__":
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        locate_simple_form_message_input(driver)
        locate_checkbox_labels(driver)
    finally:
        driver.quit()
