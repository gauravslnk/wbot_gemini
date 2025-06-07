# WhatsApp Auto-Reply Bot

A Python bot that captures WhatsApp Desktop chat screenshots, extracts text using OCR, and uses AI to detect specific messages or keywords to automatically send custom replies.

## Features

* Captures and reads chat messages with Tesseract OCR
* Uses Google Gemini AI to detect user-defined message patterns
* Sends automatic replies based on AI detection
* Easy to customize detection prompt and reply messages

## Setup

1. Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and set its path in the script
2. Get a Google API key and add it to `.env` as `GOOGLE_API_KEY`
3. Adjust the `chat_area` region coordinates for your WhatsApp window
4. (Optional) Use `select_chat_area.py` to find chat area coordinates
5. Run `bot.py` to start the bot

## Customization

* Modify the AI prompt in the code to detect any message or pattern you want
* Change the reply messages in the replies list

## Notes

* Works only on WhatsApp Desktop (Windows)
* Requires Python packages: `pyautogui`, `pytesseract`, `google-generativeai`, `python-dotenv`, `pygetwindow`

---
