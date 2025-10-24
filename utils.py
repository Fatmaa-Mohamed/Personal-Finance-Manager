import csv
import os
import re
import hashlib
import calendar
from datetime import datetime, date
from decimal import Decimal as decimal

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

def input_positive_float(prompt: str) -> decimal:
    while True:
        raw = input(prompt).strip()
        try:
            val = decimal(raw)
            if val <= 0:
                print("❌Please enter a positive number")
                continue
            return val
        except ValueError:
            print("❌Not a number. Try again.")

def today_str() -> str:
    return datetime.now().strftime("%d/%m/%Y")

def today_date() -> date:
    return date.today()

def parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%d/%m/%Y").date()

def format_date(d: date) -> str:
    return d.strftime("%d/%m/%Y")

def clamp_day(year:int, month:int, day:int) -> int:
    return calendar.monthrange(year, month)[1]

def next_monthly_date(from_date: date, day: int) -> date:
    year, month = from_date.year, from_date.month
    last_day = calendar.monthrange(year, month)[1]
    d = min(day, last_day)
    candidate = date(year, month, d)
    while candidate >= from_date:
        return candidate

    month += 1
    if month > 12:
        month = 1
        year += 1
    last_day = calendar.monthrange(year, month)[1]
    d = min(day, last_day)
    return date(year, month, d)

def next_yearly_date(from_date: date, day: int, month: int) -> date:
    year = from_date.year
    try:
        candidate = date(year, month, day)
    except ValueError:
        #handling invalid days
        day = min(day, calendar.monthrange(year, month)[1])
        candidate = date(year, month, day)
    if candidate >= from_date:
        return candidate

    year += 1
    day = min(day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')