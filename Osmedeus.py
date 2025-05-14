import subprocess
import requests
import time
import os

# ========== CONFIG ==========
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
CHAT_ID = 'YOUR_CHAT_ID_HERE'
OSMEDEUS_PATH = '/path/to/Osmedeus/osmedeus'
# ============================

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram error:", e)

def run_osmedeus(target):
    send_telegram_message(f"🚀 Starting scan on: {target}")
    command = [OSMEDEUS_PATH, 'scan', '-t', target]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in iter(process.stdout.readline, ''):
        print(line.strip())
        send_telegram_message(f"[{target}] ➤ {line.strip()}")
        time.sleep(1.5)  # Rate limit to avoid Telegram flooding

    process.stdout.close()
    process.wait()
    send_telegram_message(f"✅ Scan completed for: {target}")

if __name__ == "__main__":
    target = input("Enter target URL (e.g., example.com): ").strip()
    if target:
        run_osmedeus(target)
    else:
        print("Invalid input. Exiting.")
