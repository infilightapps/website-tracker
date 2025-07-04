# tracker.py
import requests
from bs4 import BeautifulSoup
import hashlib
import os

URL = "https://www.shivyogportal.com/events/tabs_all"  # Replace with the URL you want to track
CSS_SELECTOR = "body"        # Adjust this to track specific sections
HASH_FILE = "last_hash.txt"

def fetch_content():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.select_one(CSS_SELECTOR)
    return content.get_text(strip=True)

def calculate_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

def read_last_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return f.read().strip()
    return None

def write_hash(hash_val):
    with open(HASH_FILE, "w") as f:
        f.write(hash_val)

def main():
    content = fetch_content()
    new_hash = calculate_hash(content)
    old_hash = read_last_hash()

    if new_hash != old_hash:
        print("🔔 Website content changed!")
    else:
        print("No change detected.")

    write_hash(new_hash)

if __name__ == "__main__":
    main()
