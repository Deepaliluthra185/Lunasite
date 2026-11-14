import http.server
import socketserver
import threading
import time
import os
from playwright.sync_api import sync_playwright

PORT = 8089
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_server():
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
    httpd.serve_forever()

def main():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    print(f"Server started at http://127.0.0.1:{PORT}")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page()
        
        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))

        print("Navigating to index.html...")
        page.goto(f"http://127.0.0.1:{PORT}/index.html")
        page.wait_for_timeout(3000)

        # Check report text
        report_text = page.inner_text("#report")
        print("\n=== Report Text ===")
        print(report_text[:400])

        print("\n=== Console Messages ===")
        for msg in console_messages:
            print(msg)

        print("\n=== Page Errors ===")
        print(errors if errors else "None (Clean run!)")

        browser.close()

    print("\nTest completed successfully.")

if __name__ == "__main__":
    main()
