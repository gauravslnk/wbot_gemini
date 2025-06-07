import os
import time
import random
import pyautogui
import pygetwindow as gw
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

# Gemini Vision setup
genai.configure(api_key=GOOGLE_API_KEY)
vision_model = genai.GenerativeModel("gemini-1.5-flash")

# Set the region for chat screenshot (top-left-x, top-left-y, width, height)
chat_area = (1369, 856, 336, 134)  # Update this if your layout changes

# Possible replies
replies = [
    "Good morning! ☀️"
]

# Track last message to avoid repeat replies
last_reply_hash = None

# Focus the WhatsApp window
def focus_whatsapp():
    try:
        win = gw.getWindowsWithTitle("WhatsApp")[0]
        win.activate()
        time.sleep(1)
        return True
    except:
        print("[!] WhatsApp window not found.")
        return False

# Capture the chat area as an image
def get_chat_image():
    img = pyautogui.screenshot(region=chat_area)
    img.save("debug_screenshot.png")  # For manual debugging
    return img

# Use Gemini Vision to decide if GM message is present
def is_gm_from_image(img):
    try:
        if img.mode != "RGB":
            img = img.convert("RGB")

        prompt = """
You're viewing a screenshot of a WhatsApp group chat.

Has someone said "Good Morning" (or "gm") in any form, especially if it's dramatic, enthusiastic, or attention-seeking?

Only reply "Yes" or "No". Nothing else.
"""

        response = vision_model.generate_content([prompt, img], stream=False)
        result = response.text.strip().lower()
        print(f"[Gemini Vision Response]: {result}")
        return "yes" in result

    except Exception as e:
        print("[Error] Gemini Vision API failed:", e)
        return False

# Send a reply
def send_reply():
    reply = random.choice(replies)
    pyautogui.typewrite(reply)
    pyautogui.press("enter")
    print(f"[✓] Replied: {reply}")

# Hash the image to avoid duplicates
def hash_image(img):
    return hash(img.tobytes())

# --- Main Loop ---
while True:
    print("\n[⏳] Checking for new messages...")

    if focus_whatsapp():
        chat_img = get_chat_image()
        current_hash = hash_image(chat_img)

        if current_hash != last_reply_hash and is_gm_from_image(chat_img):
            send_reply()
            last_reply_hash = current_hash
        else:
            print("[→] No reply sent.")
    else:
        print("[!] WhatsApp window not accessible.")

    print("[⏰] Waiting for the next check...")
    time.sleep(10)  # ~1 min delay (change if needed)
