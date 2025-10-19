import json # built in library for handling JSON files
import csv # built in library for handling CSV files
import os # built in library for handling OS operations (files, folders, paths)
import shutil # built in library for high-level file operations like copy, move, delete
from datetime import datetime, timedelta # built in library for date and time

class DataManager:
    """Handles reading and writing user and transaction data to JSON/CSV files."""

    def __init__(self):
        # file paths
        self.users_file = 'data/users.json'
        self.users_csv = 'data/users.csv'
        self.backup_dir = 'data/backup'
        
        # Ensure folders are present if not create them
        os.makedirs('data', exist_ok=True) # Ensure data directory exists
        os.makedirs(self.backup_dir, exist_ok=True) # Ensure backup directory exists

        # Clean up old backups on startup
        self._cleanup_old_backups(days=10)

    # -----------------------------------------------------
    # LOAD USERS (from JSON)
    # -----------------------------------------------------

    def load_users(self):
        """Loads users from a JSON file."""
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
        """Saves users to a JSON file and CSV file automatically."""
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

        # Create backups
        self._backup_file(self.users_file)
        self._backup_file(self.users_csv)
    
    # -----------------------------------------------------
    # BACKUP HELPER (private)
    # -----------------------------------------------------
    def _backup_file(self, file_path):
        """Create a timestamped backup copy of a file."""

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
        """Delete backup files older than specified days."""
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