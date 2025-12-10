import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
load_dotenv()

# Setup Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.wm.com/us/en/user/login?redirect=/us/en/mywm/user/my-payment/billing/overview')

# Find the input fields and login buttonPasswordInput
email_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "EmailInput"))
)
password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "PasswordInput"))  # replace with actual password field ID
)

# Enter your credentials
email_input.send_keys(os.getenv("WM_USER"))
password_input.send_keys(os.getenv("WM_PASSWORD"))

# Click login
login_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='LoginWidget-login-button']")
login_button.click()

# Optional: wait for redirect / page load
time.sleep(5)

# Click service history button
service_history_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='ButtonArrow__text']"))
)
service_history_button.click()
time.sleep(5)
driver.quit()