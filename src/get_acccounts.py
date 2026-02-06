from playwright.sync_api import sync_playwright
import time
import json

API_URL = "https://rest-api.wm.com/authorize/user/00u44umwkllPqgs912p7/accounts"
API_KEY = "AABFF96D4542575160FC"
data = None
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # 1️⃣ Go to WM and log in manually
    page.goto("https://www.wm.com/")
    input("👉 Log in fully, then press ENTER to continue...")

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
