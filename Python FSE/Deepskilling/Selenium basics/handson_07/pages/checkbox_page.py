"""
Hands-On 7, Task 1 - CheckboxPage
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckboxPage(BasePage):
    # Step 53: checkboxes indexed 1-based to match the visual list on the page
    CHECKBOX_LIST = (By.CSS_SELECTOR, "#itemlist input[type='checkbox']")

    def _get_checkbox(self, index):
        checkboxes = self.driver.find_elements(*self.CHECKBOX_LIST)
        return checkboxes[index]

    def check_option(self, index):
        checkbox = self._get_checkbox(index)
        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_option(self, index):
        checkbox = self._get_checkbox(index)
        if checkbox.is_selected():
            checkbox.click()

    def is_option_checked(self, index):
        return self._get_checkbox(index).is_selected()
