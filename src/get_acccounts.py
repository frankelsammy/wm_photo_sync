import os
import time
import json
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


def fetch_accounts(output_file="accounts.json"):
    """
    Logs into WM, retrieves account data, optionally saves it to a file,
    and returns the parsed JSON response.

    Args:
        output_file (str | None): Path to save the JSON response.
                                  Pass None to skip writing a file.

    Returns:
        dict | list: Parsed JSON response from the API.

    Raises:
        RuntimeError: If the API request fails.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Go to WM and log in
            page.goto("https://www.wm.com/")
            page.get_by_test_id("LoginPopover-Button").click()

            page.wait_for_selector("#flyoutloginEmail")
            page.fill("#flyoutloginEmail", os.getenv("WM_USER"))
            page.fill("#flyoutloginPassword", os.getenv("WM_PASSWORD"))

            (
                page.locator("#flyoutloginPassword")
                .locator("xpath=ancestor::form")
                .locator("button[type='submit']")
                .click()
            )

            # Call API using authenticated session
            response = page.request.get(
                API_URL,
                params={
                    "timestamp": int(time.time() * 1000),
                    "lang": "en_US",
                },
                headers={
                    "apikey": API_KEY,
                    "accept": "application/json",
                },
            )

            if not response.ok:
                raise RuntimeError(
                    f"Request failed ({response.status}): {response.text()}"
                )

            data = response.json()

            if output_file:
                with open(output_file, "w") as f:
                    json.dump(data, f, indent=4)

            return data

        finally:
            browser.close()


if __name__ == "__main__":
    fetch_accounts()