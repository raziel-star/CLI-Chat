import time
import sys
import os
import pickle
import re
from colorama import Fore, Style
from config import MEMORY_FILE

def typewriter(text, delay=0.001):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def reverse_hebrew_advanced(text):
    def is_hebrew(char):
        return '\u0590' <= char <= '\u05FF'

    def process_word(word):
        if any(is_hebrew(c) for c in word):
            return word[::-1]
        return word

    words = re.findall(r'\w+|[^\w\s]', text, re.UNICODE)
    reversed_words = [process_word(word) for word in words]
    result = ""
    for i, word in enumerate(reversed_words):
        if i > 0 and re.match(r'\w', word):
            result += " "
        result += word
    return result

def extract_text(response):
    try:
        if hasattr(response, "text") and response.text:
            return response.text
        return response.candidates[0].content.parts[0].text
    except Exception:
        return "Failed to get a response from the model."

def dots_spinner(flag, message="Processing", color=Fore.CYAN):
    count = 0
    while flag[0]:
        dots = "." * (count % 4)
        sys.stdout.write(color + f"\r{message}{dots}   " + Style.RESET_ALL)
        sys.stdout.flush()
        count += 1
        time.sleep(0.5)
    sys.stdout.write("\r" + " " * 50 + "\r")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "rb") as f:
            return pickle.load(f)
    return []

def save_memory(conversation_memory):
    with open(MEMORY_FILE, "wb") as f:
        pickle.dump(conversation_memory, f)
