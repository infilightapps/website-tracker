import requests
from bs4 import BeautifulSoup
import hashlib
import os

# === Configuration ===
URL = "https://www.shivyogportal.com/events/tabs_all"  # 🔁 Replace with the website you want to monitor
CSS_SELECTOR = "body"        # 🔁 Replace with the specific section if needed
HASH_FILE = "last_hash.txt"

# === Fetch website content ===
def fetch_content():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.select_one(CSS_SELECTOR)
        return content.get_text(strip=True) if content else ""
    except Exception as e:
        print(f"⚠️ Failed to fetch content: {e}")
        return ""

# === Calculate SHA256 hash ===
def calculate_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

# === Load previous hash ===
def read_last_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return f.read().strip()
    return None

# === Save new hash ===
def write_hash(new_hash):
    with open(HASH_FILE, "w") as f:
        f.write(new_hash)

# === Send Telegram alert ===
def send_telegram_alert(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_USER_ID")
    if not token or not chat_id:
        print("⚠️ Telegram credentials not set. Skipping alert.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload, timeout=5)
        if response.status_code != 200:
            print(f"⚠️ Telegram error: {response.text}")
        else:
            print("✅ Telegram alert sent.")
    except Exception as e:
        print(f"⚠️ Telegram request failed: {e}")

# === Main logic ===
def main():
    print("🔍 Checking for updates...")
    content = fetch_content()
    if not content:
        print("❌ No content fetched. Exiting.")
        return

    new_hash = calculate_hash(content)
    old_hash = read_last_hash()

    if new_hash != old_hash:
        print("🔔 Website content changed!")
        send_telegram_alert(f"🔔 Change detected on: `{URL}`")
    else:
        print("✅ No change detected.")

    write_hash(new_hash)

if __name__ == "__main__":
    main()
