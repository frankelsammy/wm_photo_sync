import os
from playwright.sync_api import sync_playwright
import time
import json
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
data = None
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # 1️⃣ Go to WM and log in manually
    page.goto("https://www.wm.com/")
    page.get_by_test_id("LoginPopover-Button").click()
    page.wait_for_selector("#flyoutloginEmail")
    page.fill("#flyoutloginEmail", os.getenv("WM_USER"))
    page.locator("#flyoutloginPassword").fill(os.getenv("WM_PASSWORD"))
    # page.wait_for_selector("#PasswordInput")
    # page.fill("#PasswordInput", os.getenv("WM_PASSWORD"))
    page.locator("#flyoutloginPassword") \
    .locator("xpath=ancestor::form") \
    .locator("button[type='submit']") \
    .click()

    # Click login button
    # page.click("button[data-testid='LoginWidget-login-button']")
    # 2️⃣ Call API using authenticated session
    response = page.request.get(
        API_URL,
        params={
            "timestamp": int(time.time() * 1000),
            "lang": "en_US"
        },
        headers={
            "apikey": API_KEY,
            "accept": "application/json"
        }
    )

    # 3️⃣ Manual status check (Playwright style)
    if not response.ok:
        print("❌ Request failed")
        print("Status:", response.status)
        print("Body:", response.text())
        exit(1)

    data = response.json()

    browser.close()
# 4️⃣ Process and save data
with open("accounts.json", "w") as f:
    json.dump(data, f, indent=4)
