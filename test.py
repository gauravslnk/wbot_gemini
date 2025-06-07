import pyautogui
import time

print("[🖱️] Move your mouse to the TOP-LEFT corner of the chat area in the next 5 seconds...")
time.sleep(5)
top_left = pyautogui.position()
print("Top-left:", top_left)

print("[🖱️] Now move to the BOTTOM-RIGHT corner of the chat area in the next 5 seconds...")
time.sleep(5)
bottom_right = pyautogui.position()
print("Bottom-right:", bottom_right)

width = bottom_right.x - top_left.x
height = bottom_right.y - top_left.y
print(f"[✅] Final Region: ({top_left.x}, {top_left.y}, {width}, {height})")
