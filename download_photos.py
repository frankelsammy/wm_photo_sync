import customer_id_map

import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

with sync_playwright() as p:
    # Launch browser
    browser = p.chromium.launch(headless=False)
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

    for customer_id in customer_id_map.customer_id_to_name.keys():
    # Click on specific customer account
        page.get_by_role("button", name=customer_id).wait_for()
        page.get_by_role("button", name=customer_id).click()
        current_customer = customer_id_map.customer_id_to_name[customer_id]

        page.get_by_role("button", name="My Services").wait_for()
        page.get_by_role("button", name="My Services").click()

        page.get_by_role("button", name="View Service History").wait_for()
        page.get_by_role("button", name="View Service History").click()

        page.get_by_role("button", name="View Details").first.wait_for(state="visible")
        page.get_by_role("button", name="View Details").first.click()
        time.sleep(5)  # Wait for the service history page to load
        
        # Create directory for current customer
        os.makedirs(current_customer, exist_ok=True)

        # --- Collect ALL truckimages media from the DOM ---
        media_urls = page.evaluate("""
        () => {
            const urls = new Set();

            document.querySelectorAll("img[src], video[src]").forEach(el => {
                const src = el.getAttribute("src");
                if (src && src.includes("truckimages.wm.com")) {
                    urls.add(src);
                }
            });

            return Array.from(urls);
        }
        """)

        # --- Download media ---
        for idx, url in enumerate(media_urls, start=1):
            print(f"Downloading media {idx}: {url}")

            content = page.request.get(url).body()

            # Determine file extension
            ext = url.split(".")[-1].split("?")[0]
            kind = "video" if ext.lower() in ("mp4", "webm", "mov") else "image"

            with open(f"results/{current_customer}/{current_customer}_{kind}_{idx}.{ext}", "wb") as f:
                f.write(content)
        
        # return to Billing overview page
        page.goto("https://www.wm.com/us/en/user/login?redirect=/us/en/mywm/user/my-payment/billing/overview")
    time.sleep(10)
    browser.close()
