import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    console_messages = []
    page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
    page.on("pageerror", lambda err: print("PAGE ERROR:", err))

    print("Navigating to http://localhost:8000/index.html ...")
    page.goto("http://localhost:8000/index.html")
    page.wait_for_timeout(2000)

    # 1. Test AI Flight Briefing
    print("Testing AI Flight Briefing button click...")
    page.click("#aiExplainBtn")
    # Wait for Gemini response
    for _ in range(15):
        text = page.inner_text("#aiExplainContent")
        if "Power Architecture" in text or "Briefing error" in text:
            print("Briefing response received:")
            print(text[:300])
            break
        time.sleep(1)

    # 2. Test AI Natural Language Search
    print("\nTesting AI Natural Language Search...")
    page.fill("#aiQuery", "Where is Apollo 11 located?")
    page.click("#aiSearchBtn")
    # Wait for Search response
    for _ in range(15):
        feedback = page.inner_text("#aiSearchFeedback")
        if "Apollo 11" in feedback or "Search error" in feedback:
            print("Search feedback received:")
            print(feedback)
            break
        time.sleep(1)

    page.wait_for_timeout(1000)
    page.screenshot(path="C:/Users/HP/.gemini/antigravity/brain/837b1be4-4b1e-4418-8f28-33a5de93c5d6/screenshot_ai.png")
    print("\nScreenshot saved to screenshot_ai.png!")

    browser.close()
