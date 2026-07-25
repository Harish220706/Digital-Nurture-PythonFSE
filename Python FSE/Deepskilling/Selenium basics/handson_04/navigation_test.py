"""
Hands-On 4, Task 2 - WebDriver Navigation and Window Commands
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


def run_navigation_and_windows():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Step 28: navigate to Simple Form Demo, assert URL, go back
        driver.get(BASE_URL)
        simple_form_link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
        simple_form_link.click()

        assert "simple-form-demo" in driver.current_url, (
            f"Expected 'simple-form-demo' in URL, got {driver.current_url}"
        )
        print("Confirmed on Simple Form Demo page:", driver.current_url)

        driver.back()
        print("Navigated back to:", driver.current_url)

        # Step 29: open a new tab, list handles, switch to it
        driver.execute_script('window.open("https://www.google.com");')
        all_handles = driver.window_handles
        print("Open window handles:", all_handles)

        driver.switch_to.window(all_handles[1])
        print("Second tab title:", driver.title)

        # Step 30: switch back to original tab and take a screenshot
        driver.switch_to.window(all_handles[0])
        driver.save_screenshot("playground_screenshot.png")
        print("Screenshot saved as playground_screenshot.png")

        # Step 31: window size commands
        # Consistent window size matters because responsive layouts change
        # their DOM structure/visibility at different breakpoints (e.g., a
        # hamburger menu appears below 768px). If tests run at inconsistent
        # or undefined window sizes, locators that only exist at certain
        # breakpoints will intermittently fail - fixing the size makes
        # layout-dependent tests deterministic and reproducible.
        current_size = driver.get_window_size()
        print("Current window size:", current_size)

        driver.set_window_size(1280, 800)
        print("Window resized to:", driver.get_window_size())

    finally:
        driver.quit()


if __name__ == "__main__":
    run_navigation_and_windows()
