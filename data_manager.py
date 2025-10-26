import json # built in library for handling JSON files
import csv # built in library for handling CSV files
import os # built in library for handling OS operations (files, folders, paths)
import shutil # built in library for high-level file operations like copy, move, delete
from dataclasses import field
from datetime import datetime, timedelta # built in library for date and time
from decimal import Decimal

class DataManager:
    """Handles reading and writing user and transaction data to JSON/CSV files."""

    def __init__(self):
        """Initialize data paths, ensure directories exist, and load transactions."""
        # file paths
        self.users_file = 'data/users.json'
        self.users_csv = 'data/users.csv'
        self.backup_dir = 'data/backup'
        self.transactions_file = 'data/transactions.json'
        self.transactions_csv = 'data/transactions.csv'

        # Ensure folders are present if not create them
        os.makedirs('data', exist_ok=True) # Ensure data directory exists
        os.makedirs(self.backup_dir, exist_ok=True) # Ensure backup directory exists

        # ensure transactions storage exists
        if not os.path.exists(self.transactions_file):
            with open(self.transactions_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        if not os.path.exists(self.transactions_csv):
            with open(self.transactions_csv, 'w',newline= '', encoding='utf-8') as csvfile:
                fieldnames = [
                    'transaction_id','user_id','type', 'amount',
                    'category', 'date', 'description','payment_method']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

        self.transactions = self.load_transactions()
        # Clean up old backups on startup
        self._cleanup_old_backups(days=10)

    # -----------------------------------------------------
    # LOAD USERS (from JSON)
    # -----------------------------------------------------

    def load_users(self):
        """Load all users from the JSON file; return {} if missing or corrupted."""
        if not os.path.exists(self.users_file):
            return {} # Return empty dict if no users.json exists

        # Try to load JSON
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f: # Open user.json file in read mode using utf-8 encoding for special chars
                return json.load(f) # Read JSON file and convert it to python dicts

        except json.JSONDecodeError: # Handle corrupted JSON file
            print("⚠️ Could not read users.json - file may be corrupted")
            return {}

    # -----------------------------------------------------
    # SAVE USERS (to both JSON and CSV)
    # -----------------------------------------------------

    def save_users(self, users):
        """Write users data to both JSON and CSV files for persistence."""
        # JSON saving
        with open(self.users_file, 'w', encoding='utf-8') as f: # Open user.json file in write mode using utf-8 encoding for special chars
            json.dump(users, f, indent=4, ensure_ascii=False) # Write python dicts to JSON file with pretty print indent of 4 spaces and ensure special chars are saved correctly

        # CSV saving
        with open(self.users_csv, 'w', newline='', encoding='utf-8') as csvfile: # Open user.csv file in write mode using utf-8 encoding for special chars
            fieldnames = ['user_id', 'name', 'password', 'currency']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # Always write header

            # Write users (if any)
            for user_data in users.values():
                writer.writerow(user_data)

    # Backup once function
    def create_backup_once(self):
        """Create timestamped backups for users and transactions files."""
        self._backup_file(self.users_file)
        self._backup_file(self.users_csv)
        self._backup_file(self.transactions_file)
        self._backup_file(self.transactions_csv)

    # -----------------------------------------------------
    # BACKUP HELPER (private)
    # -----------------------------------------------------
    def _backup_file(self, file_path):
        """Private helper to copy a file into the backup directory with a timestamp."""
        if os.path.exists(file_path):
            base_name = os.path.basename(file_path)  # Extracts filename from full path ex: get "users.json"

            # Add timestamp to backup name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') #  Format datetime as string ex: "20251019_143045"
            backup_name = f"{base_name}_{timestamp}.bak" # ex: "users.json_20251019_143045.bak"
            backup_path = os.path.join(self.backup_dir, backup_name) # Safely combines file path

            try:
                shutil.copy(file_path, backup_path) # Copies a file: copying original file to backup file
            # Catch any error message
            except Exception as e:
                print(f"⚠️ Backup failed: {e}")

    # -----------------------------------------------------
    # CLEANUP BACKUP HELPER (private)
    # -----------------------------------------------------

    def _cleanup_old_backups(self, days=10):
        """Private helper to delete backups older than the specified number of days."""
        try:
            # Calculate cutoff date
            cutoff_date = datetime.now() - timedelta(days=days)

            # Get all backup files, loop through all files and make a list of only .bak files
            backup_files = [f for f in os.listdir(self.backup_dir) if f.endswith('.bak')]

            deleted_count = 0 # Counter to track deleted files
            for backup_file in backup_files:
                backup_path = os.path.join(self.backup_dir, backup_file) # Get full path of backup file

                # Get file modification time
                file_time = datetime.fromtimestamp(os.path.getmtime(backup_path))

                # Delete if older than cutoff date
                if file_time < cutoff_date:
                    os.remove(backup_path)
                    deleted_count += 1

            if deleted_count > 0:
                print(f"🗑️ Deleted {deleted_count} old backup(s) (older than {days} days)")

        except Exception as e:
            print(f"⚠️ Backup cleanup failed: {e}")


    def load_transactions(self) -> list[dict]:
        """Load all transaction records from the JSON file and ensure valid Decimal amounts."""
        try:
            with open(self.transactions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for t in data:
                        if 'amount' in t:
                            try:
                                # Convert any numeric or string type to Decimal safely
                                t['amount'] = Decimal(str(t['amount']))
                            except Exception:
                                t['amount'] = Decimal('0')
                    return data
                else:
                    print("⚠️ transactions.json is not a list.")
                    return []
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ Could not read transactions.json")
            return []

    def get_transactions(self, user_id):
        """Return all transactions that belong to a specific user ID."""
        if not hasattr(self, 'transactions'):
            return []
        return [t for t in self.transactions if t.get('user_id') == user_id]

    def save_transactions(self, transactions: list[dict]) -> None:
        """Persist all transactions to JSON and CSV, converting Decimals to strings."""
        # Convert Decimals to strings so JSON/CSV can handle them
        serializable_transactions = []
        for t in transactions:
            t_copy = t.copy()
            if isinstance(t_copy.get("amount"), Decimal):
                t_copy["amount"] = str(t_copy["amount"])
            serializable_transactions.append(t_copy)
            # ---- Save as JSON ----
        with open(self.transactions_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_transactions, f, ensure_ascii=False, indent=4)
            # ---- Save as CSV ----
        fieldnames = [
            'transaction_id', 'user_id', 'type', 'amount',
            'category', 'date', 'description', 'payment_method'
        ]
        with open(self.transactions_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for t in serializable_transactions:
                row = {
                    'transaction_id': t.get('transaction_id', ''),
                    'user_id': t.get('user_id', ''),
                    'type': t.get('type', ''),
                    'amount': t.get('amount', ''),  # already string
                    'category': t.get('category', ''),
                    'date': t.get('date', ''),
                    'description': t.get('description', ''),
                    'payment_method': t.get('payment_method', '')
                }
                writer.writerow(row)
        self.transactions = self.load_transactions()

    # --------- Advanced features csv import/export ----------------
    def export_transactions_csv(self, user_id: str, tx_list: list, path: str):
        """Export given user's transactions into a CSV file at the specified path."""
        fieldnames = ["transaction_id", "user_id", "type", "amount", "category", "date", "description",
                      "payment_method"]
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            import csv
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for t in tx_list:
                if t.get("user_id") != user_id:
                    continue
                row = {k: t.get(k, "") for k in fieldnames}
                w.writerow(row)

    def import_transactions_csv(self, user_id: str, path: str) -> int:
        """Import transactions from a CSV file, skipping duplicates by (date, amount, category)."""
        if not os.path.exists(path):
            print(f"❌ File not found: {path}")
            return 0
        added = 0
        with open(path, "r", newline="", encoding="utf-8") as f:
            import csv
            r = csv.DictReader(f)
            # Load current
            try:
                txs = self.load_transactions()
            except Exception:
                txs = []
            existing_keys = {(t.get("user_id"), str(t.get("date")), str(t.get("amount")), t.get("category")) for t in
                             txs}
            # Append new
            for row in r:
                key = (user_id, row.get("date", ""), row.get("amount", ""), row.get("category", ""))
                if key in existing_keys:
                    continue
                row["user_id"] = user_id
                txs.append(row)
                added += 1
        self.save_transactions(txs)
        return added


    #--------------- load/save goals --------------
    def load_goals(self) -> list:
        """Load saving goals from goals.json, returning an empty list if missing or invalid."""
        path = "data/goals.json"
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return []

    def save_goals(self, goals: list):
        """Persist the given list of saving goals to goals.json."""
        path = "data/goals.json"
        os.makedirs("data", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(goals, f, ensure_ascii=False, indent=2)
