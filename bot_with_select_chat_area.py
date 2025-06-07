import os
import time
import random
import json
import pyautogui
import pygetwindow as gw
import pytesseract
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

# Gemini setup
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update if needed

# Load chat_area config
with open("config.json") as f:
    chat_area = tuple(json.load(f)["chat_area"])

# Reply pool
replies = [
    "🐱 Meow-bot detected a GM alert."
]

# Track last message
last_reply_hash = None

# --- Functions ---

def focus_whatsapp():
    try:
        win = gw.getWindowsWithTitle("WhatsApp")[0]
        win.activate()
        time.sleep(1)
        return True
    except:
        print("[!] WhatsApp window not found.")
        return False

def get_chat_text():
    img = pyautogui.screenshot(region=chat_area)
    img_gray = img.convert("L")  # improve OCR accuracy
    text = pytesseract.image_to_string(img_gray)
    return text.strip()

def is_gm_from_target_user(text):
    prompt = f"""
You are monitoring a WhatsApp group chat.

Has someone recently said "Good Morning" (or a variation like "gm") in a way that:
- Suggests they send it regularly
- Might expect a reply
- Shows a tone that sounds dramatic, energetic, or demanding?

Only answer with "Yes" or "No".

Chat Messages:
{text}
"""
    try:
        response = model.generate_content(prompt)
        result = response.text.strip().lower()
        print(f"[Gemini response]: {result}")
        return "yes" in result
    except Exception as e:
        print("[Error] Gemini API failed:", e)
        return False

def send_reply():
    reply = random.choice(replies)
    pyautogui.typewrite(reply)
    pyautogui.press("enter")
    print(f"[✓] Replied: {reply}")

def hash_text(text):
    return hash(text)

# --- Main loop ---
while True:
    print("\n[⏳] Checking for new messages...")
    if focus_whatsapp():
        chat_text = get_chat_text()
        print("[OCR Chat]:\n", chat_text)

        current_hash = hash_text(chat_text)
        if current_hash != last_reply_hash and is_gm_from_target_user(chat_text):
            send_reply()
            last_reply_hash = current_hash
        else:
            print("[→] No reply sent.")
    else:
        print("[!] WhatsApp window not accessible.")

    time.sleep(600)  # wait 10 minutes
