"""
Hands-On 4, Task 1 - Selenium Architecture & Environment Setup

SELENIUM COMPONENT ARCHITECTURE
--------------------------------
1. WebDriver: A W3C-standard protocol + library that sends commands (click,
   type, navigate) directly to a browser's native automation interface
   (e.g., Chrome's DevTools Protocol via chromedriver). It communicates over
   HTTP with a driver executable that sits between your script and the real
   browser - there is no browser plugin/extension involved, which is why
   WebDriver is fast and works the same way the browser behaves for a real
   user.

2. Selenium Grid: Solves the problem of running tests in parallel across
   multiple machines and/or multiple browser/OS combinations. Instead of
   running every test sequentially on one machine, Grid distributes test
   execution across a network of "nodes," dramatically cutting total suite
   run time and enabling cross-browser/cross-platform coverage.

3. Selenium IDE: A browser extension for record-and-playback test creation.
   You perform actions in the browser and Selenium IDE records them as a
   reusable script, which can also be exported as code (e.g., Python,
   Java). It's useful for quickly prototyping a test or for team members
   who are less comfortable writing code directly.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


def run_basic_navigation():
    service = Service(ChromeDriverManager().install())
    options = Options()

    driver = webdriver.Chrome(service=service, options=options)

    # Step 26: implicit wait
    # NOTE: Setting implicit_wait globally is considered bad practice because
    # it applies the same fixed wait to EVERY find_element call for the
    # entire driver session. This makes tests slower than necessary when
    # elements load quickly, and it can mask timing issues by silently
    # waiting instead of failing fast. Explicit waits (Hands-On 5) let you
    # wait for a *specific condition* (visible, clickable, etc.) only where
    # it's actually needed, which is both faster and more precise.
    driver.implicitly_wait(10)

    try:
        driver.get(BASE_URL)
        print("Page title:", driver.title)
    finally:
        driver.quit()


def run_headless_navigation():
    # Step 27: headless mode
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")

    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(BASE_URL)
        print("Headless page title:", driver.title)
    finally:
        driver.quit()


if __name__ == "__main__":
    run_basic_navigation()
    run_headless_navigation()
