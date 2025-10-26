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
    """Prompt until a non-empty string is entered and return it."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("❌Please enter a non-empty string")

def input_positive_float(prompt: str) -> float:
    """Prompt until a positive decimal number is entered and return it."""
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
    """Return today's date as a formatted string (dd/mm/YYYY)."""
    return datetime.now().strftime("%d/%m/%Y")

def today_date() -> date:
    """Return today's date as a datetime.date object."""
    return date.today()

def parse_date(date_str: str) -> date:
    """Convert a dd/mm/YYYY string into a datetime.date object."""
    return datetime.strptime(date_str, "%d/%m/%Y").date()

def format_date(d: date) -> str:
    """Format a date object into dd/mm/YYYY string form."""
    return d.strftime("%d/%m/%Y")

def clamp_day(year:int, month:int, day:int) -> int:
    """Return the maximum valid day for the given month/year."""
    return calendar.monthrange(year, month)[1]

def next_monthly_date(from_date: date, day: int) -> date:
    """Compute the next monthly date from a reference date for a target day."""
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
    """Compute the next yearly date from a reference date for a target day and month."""
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

def bar(value: float, scale: float = 100.0, char: str = "#", width: int = 30) -> str:
    # small ASCII bar helper used by reports
    try:
        n = int(min(width, max(0, value / scale * width)))
    except Exception:
        n = 0
    return char * n