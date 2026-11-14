import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8000/index.html")
    page.wait_for_timeout(2500)
    page.screenshot(path="C:/Users/HP/.gemini/antigravity/brain/837b1be4-4b1e-4418-8f28-33a5de93c5d6/screenshot.png")
    print("Screenshot captured successfully!")
    browser.close()

