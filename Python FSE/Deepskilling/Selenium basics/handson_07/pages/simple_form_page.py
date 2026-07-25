"""
Hands-On 7, Task 1 - SimpleFormPage

Golden rule: this file contains ONLY interactions (how to do something).
No assert statements live here - those belong in the test files.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SimpleFormPage(BasePage):
    # Step 51: locators as class-level tuples - never hardcoded in methods
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.ID, "showInput")
    DISPLAYED_MESSAGE = (By.ID, "message")

    def enter_message(self, text):
        input_field = self.wait_for_element(self.MESSAGE_INPUT)
        input_field.clear()
        input_field.send_keys(text)

    def click_submit(self):
        button = self.wait_for_clickable(self.SUBMIT_BUTTON)
        button.click()

    def get_displayed_message(self):
        return self.wait_for_element(self.DISPLAYED_MESSAGE).text
