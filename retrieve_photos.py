import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

with sync_playwright() as p:
    # Launch browser
    browser = p.chromium.launch(headless=False)  # set headless=True if you want invisible
    context = browser.new_context()
    page = context.new_page()

    # Go to login page
    page.goto("https://www.wm.com/us/en/user/login?redirect=/us/en/mywm/user/my-payment/billing/overview")

    # Fill email and password
    page.wait_for_selector("#EmailInput")
    page.fill("#EmailInput", os.getenv("WM_USER"))

    page.wait_for_selector("#PasswordInput")
    page.fill("#PasswordInput", os.getenv("WM_PASSWORD"))

    # Click login button
    page.click("button[data-testid='LoginWidget-login-button']")

    # Wait for page to load/redirect after login
    page.wait_for_load_state("networkidle")

    # Click service history button
    page.click("div[data-testid='ButtonArrow__text']")

    time.sleep(5)

    browser.close()
