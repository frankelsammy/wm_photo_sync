import customer_id_map

import os
import time
from datetime import date
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError

load_dotenv()
customer_id_map = customer_id_map.make_map()
def normalize(text):
    return text.replace("\u200b", "").strip()
with sync_playwright() as p:
    # Launch browser
    
    browser = p.chromium.launch(headless=True)
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

    def find_customer_button(customerID):
        # Scroll to top
        list_container.evaluate("(el) => el.scrollTop = 0")
        page.wait_for_timeout(1000)

        scroll_attempts = 0
        while scroll_attempts < 10:  # Allow more attempts to find the button
            button = list_container.locator("button", has_text=customerID)
            if button.count() > 0:
                return button.first

            # Scroll down
            bbox = list_container.bounding_box()
            if bbox:
                page.mouse.move(bbox['x'] + bbox['width'] / 2, bbox['y'] + bbox['height'] / 2)
            page.mouse.wheel(0, 400)
            page.wait_for_timeout(1000)
            scroll_attempts += 1

        return None  # Button not found
    
    # Make directory for today's results
    results_dir = f"results/{date.today()}"
    os.makedirs(results_dir, exist_ok=True)
    
    i = 0
    for customer_id in customer_id_map.keys():
        i += 1
        print(f"Processing customer {i} of {len(customer_id_map)}")
        current_customer = customer_id
        customer_name = customer_id_map[current_customer]
        # Create directory for current customer
        customer_dir = f"{results_dir}/{customer_name}"

        # For testing -- skip existing directories
        if os.path.exists(customer_dir):
            print(f"Directory for customer {current_customer} already exists, skipping download.")
            page.goto("https://www.wm.com/us/en/user/login?redirect=/us/en/mywm/user/my-payment/billing/overview")
            continue


        print(f"Processing customer: {current_customer}: {customer_name}")
        customer_button = find_customer_button(current_customer)
        if customer_button is None:
            print(f"Customer button for {current_customer} not found, skipping.")
            
            continue 
        print(f"Clicking button for customer: {current_customer}")
        page.click(f'button:has-text("{current_customer}")')

        page.get_by_role("button", name="My Services").wait_for()
        page.get_by_role("button", name="My Services").click()
        try:
            page.get_by_role("button", name="View Service History").wait_for()
            page.get_by_role("button", name="View Service History").click()
        except TimeoutError:
            print(f"'View Service History' button not found for customer {current_customer}, skipping.")
            page.goto("https://www.wm.com/us/en/user/login?redirect=/us/en/mywm/user/my-payment/billing/overview")
            
            continue

        try:
            page.get_by_role("button", name="View Details").first.wait_for(state="visible", timeout=3000)  # 3 seconds
            page.get_by_role("button", name="View Details").first.click()
        except TimeoutError:
            # Button never appeared → skip
            print(f"'View Details' button did not appear for customer {current_customer}, skipping.")
            page.goto("https://www.wm.com/us/en/user/login?redirect=/us/en/mywm/user/my-payment/billing/overview")
            continue
        time.sleep(5)  # Wait for the service history page to load
        

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
        # Create customer directory
        if len(media_urls) > 0:
            os.makedirs(customer_dir, exist_ok=True)
        else:
            page.goto("https://www.wm.com/us/en/user/login?redirect=/us/en/mywm/user/my-payment/billing/overview")
            continue
        # --- Download media ---
        for idx, url in enumerate(media_urls, start=1):
            print(f"Downloading media {idx}: {url}")

            content = page.request.get(url).body()

            # Determine file extension
            ext = url.split(".")[-1].split("?")[0]
            kind = "video" if ext.lower() in ("mp4", "webm", "mov") else "image"
            today = date.today()
            print(customer_dir)
            with open(f"{customer_dir}/{kind}.{idx}.{ext}", "wb") as f:
                f.write(content)
            # return to Billing overview page
        page.goto("https://www.wm.com/us/en/user/login?redirect=/us/en/mywm/user/my-payment/billing/overview")
    time.sleep(10)
    browser.close()
