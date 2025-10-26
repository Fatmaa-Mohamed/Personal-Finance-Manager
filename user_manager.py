import uuid
from utils import is_valid_password, hash_password
import getpass # for secure password input

class UserManager:
    """Manages users: create, login, profiles, switching, logout."""

    def __init__(self, data_manager):
        """Initialize the user manager and load users from storage via data_manager."""
        self.data_manager = data_manager
        self.users = data_manager.load_users()  # uses load_users from data_manager to read users from users.json as dict {user_id: user_data}
        self.current_user = None

    # -----------------------------
    # Private Helper Method
    # -----------------------------
    def _find_user_by_name(self, name): # Used to handle login, create, and switch user flows
        """Return the user dict matching a case-insensitive name, or None if not found."""
        for user in self.users.values():
            if user['name'].lower() == name.lower():
                return user
        return None

    # -----------------------------
    # CREATE USER
    # -----------------------------
    def create_user(self):
        """Interactively create a new user with a strong password and default currency."""
        print("\n🆕 Create New User")
        name = input("Enter name (must be unique): ").strip()
        if not name:
            print("❌ Name cannot be empty!")
            return
        if self._find_user_by_name(name):
            print(f"❌ User '{name}' already exists!")
            return

        while True:
            password = getpass.getpass("Enter password: ").strip()
            if not is_valid_password(password):
                print("❌ Weak password! Must include uppercase, lowercase, number, and special character.")
                continue  # ask again
            confirm = getpass.getpass("Confirm password: ").strip()
            if password and password == confirm:
                break
            print("❌ Passwords don't match or empty!")

        currency = input("Currency (default USD): ").strip().upper() or "USD"
        user_id = str(uuid.uuid4())[:8]  # Generate unique user ID using uuid4 taking first 8 chars

        new_user = {  # Create dictionary for new user
            "user_id": user_id,
            "name": name,
            "password": hash_password(password),
            "currency": currency
        }

        self.users[user_id] = new_user
        self.data_manager.save_users(self.users) # Save the updated users dictionary to JSON/CSV file
        print(f"✅ User '{name}' created successfully!")

    # -----------------------------
    # LOGIN USER
    # -----------------------------
    def login_user(self):
        """Authenticate by name and password; sets current_user on success and returns it."""
        print("\n🔓 Login")
        if not self.users: # This is a safety check in case there are no users at all.
            print("❌ No users found. Create one first!")
            return None

        name = input("Enter name: ").strip()
        user = self._find_user_by_name(name) # Check if user name exists as a user
        if not user:
            print("❌ No account found with that name.")
            return None

        while True: # Loop until correct password is entered
            password = getpass.getpass("Enter password (or 'q' to quit): ").strip()
            # Allow exit
            if password.lower() in ('q', 'quit'):
                print("↩️ Returning to main menu...")
                return None

            if user['password'] == hash_password(password):
                self.current_user = user
                print(f"✅ Welcome back, {user['name']}!")
                return user
            else:
                print("❌ Wrong password! Please try again.\n")

    # -----------------------------
    # VIEW PROFILE
    # -----------------------------
    def view_profile(self):
        """Print the currently logged-in user's profile details."""
        if not self.current_user: # Again a safety check to prevent system crashing
            print("❌ Please login first!")
            return
        user = self.current_user
        print("\n👤 Profile Information")
        print("-" * 40)
        print(f"User ID: {user['user_id']}")
        print(f"Name: {user['name']}")
        print(f"Password (hidden): {'*' * len(user['password'])}")
        print(f"Currency: {user['currency']}")

    # -----------------------------
    # CHANGE PASSWORD
    # -----------------------------
    def change_password(self):
        """Securely change the current user's password after verifying the old one."""
        if not self.current_user: # Again prevents errors if no one is logged in.
            print("❌ Please login first!")
            return

        print("\n🔑 Change Password")
        # Keep asking for the old password until it's correct
        while True:
            old_pass = getpass.getpass("Enter old password (or 'q' to quit): ").strip()

            if old_pass.lower() in ('q', 'quit'):
                print("↩️ Returning to user menu...")
                return None

            if self.current_user['password'] == hash_password(old_pass):
                break
            print("❌ Incorrect old password! Please try again.")

        while True:
            new_pass = getpass.getpass("Enter new password: ").strip()
            if not is_valid_password(new_pass):
                print("❌ Weak password! Must include uppercase, lowercase, number, and special character.")
                continue  # ask again
            confirm = getpass.getpass("Confirm new password: ").strip()
            if new_pass and new_pass == confirm:
                break
            print("❌ Passwords don't match or empty!")

        self.current_user['password'] = hash_password(new_pass)
        self.users[self.current_user['user_id']] = self.current_user
        self.data_manager.save_users(self.users)
        print("✅ Password updated successfully!")

    # -----------------------------
    # SWITCH USER
    # -----------------------------
    def switch_user(self):
        """Switch to another existing user after password verification; updates current_user."""
        print("\n🔄 Switch User")
        if not self.users:
            print("❌ No users available.")
            return None

        users_list = list(self.users.values()) # Converts the self.users dictionary into a list of user dictionaries.
        for i, user in enumerate(users_list, 1): # Display users with numbering starting from 1
            print(f"{i}. {user['name']}")

        try:
            choice = int(input("Choose user number: ")) 
            if choice < 1 or choice > len(users_list): # Checks if the user choice within valid range
                print("❌ Invalid choice!")
                return None
        except ValueError: # Catches non-integer inputs
            print("❌ Enter a valid number!")
            return None

        selected = users_list[choice - 1] # Retrieves the chosen user dictionary from the indices

        # Check if selected user is the same as current
        if self.current_user and selected['user_id'] == self.current_user['user_id']:
            print(f"ℹ️ You are already logged in as '{selected['name']}'.")
            return None
        
        password = getpass.getpass(f"Password for {selected['name']}: ").strip()

        if selected['password'] != hash_password(password): # Verify the password
            print("❌ Wrong password!")
            return None

        # Auto-save before switching
        self.data_manager.save_users(self.users)
        self.current_user = selected # Updates the current user to the selected user.
        print(f"✅ Switched to {selected['name']}!")
        return selected

    # -----------------------------
    # LOGOUT
    # -----------------------------
    def logout(self):
        """Log out and auto-save data."""
        if not self.current_user:
            print("❌ No user is currently logged in.")
            return

        self.data_manager.save_users(self.users)
        print(f"🔒 User '{self.current_user['name']}' logged out. Data saved automatically.")
        self.current_user = None