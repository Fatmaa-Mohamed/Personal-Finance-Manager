import csv
import re
import hashlib
from datetime import datetime

def is_valid_password(password):
    """
    Validates password strength using regex.
    Rules:
    - At least 8 characters
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))

def hash_password(password: str) -> str:
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest() # Convert password into JSON/CSV readable hexadecimal string 64 chars long

def pause():
    input("\nPress Enter to continue...")

#transaction helpers
def input_non_empty(prompt: str) -> str:
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("❌Please enter a non-empty string")

def input_positive_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            val = float(raw)
            if val <= 0:
                print("❌Please enter a positive number")
                continue
            return val
        except ValueError:
            print("❌Not a number. Try again.")

def today_str() -> str:
    return datetime.now().strftime("%d/%m/%Y")

