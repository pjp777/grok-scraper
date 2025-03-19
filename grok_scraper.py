import os
import time
import json
from playwright.sync_api import sync_playwright

# Load X credentials securely
X_USERNAME = os.getenv("jihar98025@winsita.com")
X_PASSWORD = os.getenv("M@ramr06U")

if not X_USERNAME or not X_PASSWORD:
    raise ValueError("❌ Missing X_USERNAME or X_PASSWORD.")

GROK_PROMPT = "What are the hottest viral trends among Gen-Z today?"

def login_x(page):
    """ Logs into X and navigates to Grok chat """
    page.goto("https://twitter.com/login")
    time.sleep(2)

    # Enter username
    page.fill("input[name='text']", X_USERNAME)
    page.click("div[data-testid='LoginForm_Login_Button']")
    time.sleep(3)

    # Enter password
    page.fill("input[name='password']", X_PASSWORD)
    page.click("div[data-testid='LoginForm_Login_Button']")
    time.sleep(5)

def ask_grok(page):
    """ Sends a query to Grok-3 and extracts the response """
    page.goto("https://twitter.com/messages")  # Navigates to X DMs
    time.sleep(3)

    # Click on Grok chat (Modify if needed)
    page.click("xpath=//span[contains(text(), 'Grok')]")
    time.sleep(3)

    # Send message
    page.fill("div[role='textbox']", GROK_PROMPT)
    page.keyboard.press("Enter")
    time.sleep(5)

    # Extract response from the last message
    response = page.locator("xpath=//div[contains(@class, 'message-text')]").last.inner_text()
    return response

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            login_x(page)
            grok_response = ask_grok(page)
            print(f"✅ Grok-3 Response: {grok_response}")

            with open("/app/grok_trends.json", "w") as file:
                json.dump({"trending_topic": grok_response}, file)

        finally:
            browser.close()

if __name__ == "__main__":
    main()
