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

    video_urls = page.locator("video").evaluate_all("els => els.map(e => e.src)")
    downloaded_videos = set()
    for idx, video_url in enumerate(video_urls):
        if video_url in downloaded_videos:
            continue
        print(f"Downloading video {idx + 1} from {video_url}")
        video_content = page.request.get(video_url).body()
        with open(f"{current_customer}/{current_customer}_video_{idx + 1}.mp4", "wb") as video_file:
            video_file.write(video_content)
            downloaded_videos.add(video_url)

    # Download images, avoid duplicates
    # Wait for images to appear
    page.wait_for_selector("img")

    # Get all image URLs from truckimages.wm.com
    image_urls = page.locator("img").evaluate_all(
        "els => els.map(e => e.src).filter(src => src.includes('truckimages.wm.com'))"
    )
    downloaded_images = set()
    for idx, image_url in enumerate(image_urls):
        if image_url in downloaded_images:
            continue
        print(f"Downloading image {idx + 1} from {image_url}")
        image_content = page.request.get(image_url).body()
        ext = image_url.split(".")[-1].split("?")[0]  # handle query strings
        with open(f"{current_customer}/{current_customer}_image_{idx + 1}.{ext}", "wb") as img_file:
            img_file.write(image_content)
            downloaded_images.add(image_url)
    
    # return to Billing overview page
    page.goto("https://www.wm.com/us/en/user/login?redirect=/us/en/mywm/user/my-payment/billing/overview")
    time.sleep(10)
    browser.close()
