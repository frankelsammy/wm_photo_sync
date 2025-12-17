import customer_id_map

import os
import time
from datetime import date
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()
def normalize(text):
    return text.replace("\u200b", "").strip()
with sync_playwright() as p:
    # Launch browser
    print(len(customer_id_map.make_map()))
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.bring_to_front()  # Bring the browser window to the front

    # Go to login page
    page.goto("https://www.wm.com/us/en/user/login?redirect=/us/en/mywm/user/my-payment/billing/overview")

    # Fill email and password
    page.wait_for_selector("#EmailInput")
    page.fill("#EmailInput", os.getenv("WM_USER"))

    page.wait_for_selector("#PasswordInput")
    page.fill("#PasswordInput", os.getenv("WM_PASSWORD"))

    # Click login button
    page.click("button[data-testid='LoginWidget-login-button']")
    list_container = page.locator('div[data-testid="WindowedList"]')
    list_container.wait_for(state="visible", timeout=20000)

    # Scroll to top
    list_container.evaluate("(el) => el.scrollTo(0, 0)")
    page.wait_for_timeout(500)

    seen = set()
    scroll_attempts = 0

    while scroll_attempts < 3:
        # Record current count
        prev_count = len(seen)
        
        # Re-query buttons each scroll
        buttons = list_container.locator("button")
        for i in range(buttons.count()):
            txt = buttons.nth(i).inner_text().strip()
            if txt:
                seen.add(txt)

        # Check if we found new buttons
        if len(seen) > prev_count:
            scroll_attempts = 0  # reset attempts
        else:
            scroll_attempts += 1

        # Scroll slowly to make it visible
        if scroll_attempts < 3:
            print(f"Scrolling... currently have {len(seen)} buttons")
            list_container.hover()
            page.mouse.wheel(0, 400)  # Scroll down by 400 pixels
            page.wait_for_timeout(2000)  # longer wait to see the scroll

    # Print all button titles
    print(f"✅ Found {len(seen)} buttons:")
    for title in sorted(seen):
        print(title)


    # for customer_id in customer_id_map.keys():
    #     current_customer = customer_id
    #     button_found = False

    #     list_container = page.locator('div[data-testid="WindowedList"]')
    #     try:
    #         list_container.wait_for(state="visible", timeout=20000)
    #         print("✅ WindowedList container is visible")
    #     except:
    #         print("❌ WindowedList container NOT found / not visible")
    #         raise

    #     # 🔁 ALWAYS reset scroll to top before searching
    #     list_container.evaluate("(el) => el.scrollTo(0, 0)")
    #     page.wait_for_timeout(800)  # let React re-render

    #     for i in range(60):  # more passes, slower
    #         button = page.locator(
    #             "button.btn-customer-id",
    #             has_text=current_customer
    #         )

    #         if button.count() > 0:
    #             button.first.scroll_into_view_if_needed()
    #             page.wait_for_timeout(300)
    #             button.first.click()
    #             print(f"🎯 Clicked customer {current_customer} (scroll step {i})")
    #             button_found = True
    #             break

    #         # ⬇️ slow, incremental scrolling
    #         list_container.evaluate("(el) => el.scrollBy(0, el.clientHeight * 0.6)")
    #         page.wait_for_timeout(500)  # CRITICAL: slow down

    #     if not button_found:
    #         print(f"Customer {current_customer} not found")
    #         continue

    #     page.get_by_role("button", name=customer_id).wait_for()
    #     page.get_by_role("button", name=customer_id).click()
        
    #     page.get_by_role("button", name="My Services").wait_for()
    #     page.get_by_role("button", name="My Services").click()

    #     page.get_by_role("button", name="View Service History").wait_for()
    #     page.get_by_role("button", name="View Service History").click()

    #     page.get_by_role("button", name="View Details").first.wait_for(state="visible")
    #     page.get_by_role("button", name="View Details").first.click()
    #     time.sleep(5)  # Wait for the service history page to load
        
    #     # Create directory for current customer
    #     os.makedirs(current_customer, exist_ok=True)

    #     # --- Collect ALL truckimages media from the DOM ---
    #     media_urls = page.evaluate("""
    #     () => {
    #         const urls = new Set();

    #         document.querySelectorAll("img[src], video[src]").forEach(el => {
    #             const src = el.getAttribute("src");
    #             if (src && src.includes("truckimages.wm.com")) {
    #                 urls.add(src);
    #             }
    #         });

    #         return Array.from(urls);
    #     }
    #     """)

    #     # --- Download media ---
    #     for idx, url in enumerate(media_urls, start=1):
    #         print(f"Downloading media {idx}: {url}")

    #         content = page.request.get(url).body()

    #         # Determine file extension
    #         ext = url.split(".")[-1].split("?")[0]
    #         kind = "video" if ext.lower() in ("mp4", "webm", "mov") else "image"
    #         today = date.today()
    #         with open(f"results/{today}/{current_customer}/{current_customer}_{kind}_{idx}.{ext}", "wb") as f:
    #             f.write(content)
        
    #     # return to Billing overview page
    #     page.goto("https://www.wm.com/us/en/user/login?redirect=/us/en/mywm/user/my-payment/billing/overview")
    time.sleep(10)
    browser.close()
