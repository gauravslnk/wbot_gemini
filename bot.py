import os
import time
import random
import pyautogui
import pygetwindow as gw
import pytesseract
import google.generativeai as genai
import keyboard
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

# OCR engine path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# WhatsApp chat region
chat_area = (1369, 856, 336, 134)

# Reply message
reply_message = "Good Morning"

# Track previous message
last_reply_hash = None

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
    img.save("debug_screenshot.png")
    img_gray = img.convert("L")
    text = pytesseract.image_to_string(img_gray)
    return text.strip()

def should_reply(text):
    prompt = f"""
You're monitoring WhatsApp messages via screenshot OCR.

Determine if a message in the following chat content seems like it needs an auto-reply. Use your own judgment based on the tone or pattern.

Chat:
{text}

Reply only "yes" or "no".
"""
    try:
        response = model.generate_content(prompt)
        result = response.text.strip().lower()
        print(f"[Gemini response]: {result}")
        return "yes" in result
    except Exception as e:
        print("[Gemini Error]:", e)
        return False

def send_reply():
    pyautogui.typewrite(reply_message)
    pyautogui.press("enter")
    print(f"[✓] Replied: {reply_message}")

def hash_text(text):
    return hash(text)

print("[🧠] Bot ready. Press 's' to start. Press 'Esc' anytime to stop.")

# Wait for manual start
keyboard.wait('s')

try:
    while True:
        if keyboard.is_pressed("esc"):
            print("[🛑] Bot stopped by user.")
            break

        print("\n[⏳] Checking for new messages...")
        if focus_whatsapp():
            chat_text = get_chat_text()
            print("[OCR Chat]:\n", chat_text)

            current_hash = hash_text(chat_text)
            if current_hash != last_reply_hash and should_reply(chat_text):
                send_reply()
                last_reply_hash = current_hash
            else:
                print("[→] No reply sent.")
        else:
            print("[!] WhatsApp not accessible.")

        time.sleep(50)  # wait 50s before next scan

except KeyboardInterrupt:
    print("[🛑] Bot stopped manually.")
