import os
import time
import random
import hashlib
import pyautogui
import pygetwindow as gw
import pytesseract
import google.generativeai as genai
import keyboard
from dotenv import load_dotenv
from PIL import Image, ImageOps
from datetime import datetime

# ===== CONFIGURATION =====
load_dotenv()

# WhatsApp Window Settings
WHATSAPP_WINDOW_TITLE = "WhatsApp"  # Might need adjustment for your language
CHAT_AREA = (1369, 856, 336, 134)  # (left, top, width, height)

# Gemini AI Settings
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")  # Renamed for clarity
if not GOOGLE_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in .env file")

# Response Settings
REPLIES = [
    "Good morning! ☀️",
    "GM detected. Coffee level: 0/10",
    "System.out.println('Morning spam received');",
    "if (morning) { coffee++; sleep--; }"
]
REPLY_COOLDOWN = 300  # 5 minutes (seconds) between replies to same message
SCAN_INTERVAL = 30  # Seconds between checks

# ===== INITIALIZATION =====
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Track message history to avoid duplicates
message_history = {}

# ===== CORE FUNCTIONS =====
def focus_whatsapp():
    """Brings WhatsApp window to focus"""
    try:
        wins = gw.getWindowsWithTitle(WHATSAPP_WINDOW_TITLE)
        if not wins:
            print("[!] WhatsApp window not found")
            return False
            
        win = wins[0]
        if win.isMinimized:
            win.restore()
        win.activate()
        time.sleep(1)  # Allow window to come to foreground
        return True
    except Exception as e:
        print(f"[!] Window focus error: {e}")
        return False

def get_chat_image():
    """Captures the chat area with error handling"""
    try:
        # Take screenshot and convert to RGB for consistency
        img = pyautogui.screenshot(region=CHAT_AREA)
        img = ImageOps.exif_transpose(img)  # Fix orientation if needed
        if img.mode != "RGB":
            img = img.convert("RGB")
            
        # Save debug image with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_path = f"debug/debug_{timestamp}.png"
        os.makedirs("debug", exist_ok=True)
        img.save(debug_path)
        
        return img
    except Exception as e:
        print(f"[!] Screenshot error: {e}")
        return None

def generate_image_hash(img):
    """Generates consistent hash of image content"""
    return hashlib.md5(img.tobytes()).hexdigest()

def is_gm_message(img):
    """Uses Gemini Vision to detect GM messages"""
    try:
        prompt = """Analyze this WhatsApp message screenshot. 
        Reply ONLY 'YES' if you see any form of "Good Morning" (GM, morning greeting, etc.),
        'NO' otherwise. No other text."""
        
        response = vision_model.generate_content(
            [prompt, img],
            generation_config={"temperature": 0.1}
        )
        result = response.text.strip().upper()
        print(f"[AI] Response: {result}")
        return result == "YES"
    except Exception as e:
        print(f"[!] Gemini error: {e}")
        return False

def send_reply():
    """Sends a reply with typing simulation"""
    try:
        reply = random.choice(REPLIES)
        
        # Simulate human typing with random delays
        pyautogui.click()  # Ensure focus
        for char in reply:
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.05, 0.2))
            
        pyautogui.press("enter")
        print(f"[✓] Sent: {reply}")
        return True
    except Exception as e:
        print(f"[!] Reply failed: {e}")
        return False

# ===== MAIN LOOP =====
def main():
    print("=== WhatsApp GM Bot Started ===")
    print(f"Configuration:")
    print(f"- Scan Interval: {SCAN_INTERVAL}s")
    print(f"- Reply Cooldown: {REPLY_COOLDOWN}s")
    print(f"- Monitoring Area: {CHAT_AREA}")
    
    while True:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking...")
        
        if not focus_whatsapp():
            time.sleep(SCAN_INTERVAL)
            continue
            
        chat_img = get_chat_image()
        if not chat_img:
            time.sleep(SCAN_INTERVAL)
            continue
            
        img_hash = generate_image_hash(chat_img)
        
        # Check if we've already replied to this message
        last_reply_time = message_history.get(img_hash, 0)
        if time.time() - last_reply_time < REPLY_COOLDOWN:
            print("[→] Already replied to this message recently")
            time.sleep(SCAN_INTERVAL)
            continue
            
        # Analyze the message
        if is_gm_message(chat_img):
            if send_reply():
                message_history[img_hash] = time.time()
                # Clean up old entries
                for h in list(message_history.keys()):
                    if time.time() - message_history[h] > 86400:  # 24h retention
                        del message_history[h]
        else:
            print("[→] No GM detected")
            
        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Bot stopped by user")
    except Exception as e:
        print(f"[CRASH] Unexpected error: {e}")
