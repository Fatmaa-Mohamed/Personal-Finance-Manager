from user_manager import UserManager
from data_manager import DataManager
from transactions import TransactionManager
from utils import pause

class PersonalFinanceApp:
    """Main app controller."""

    def __init__(self):
        self.data_manager = DataManager() # Used for JSON files handling
        self.user_manager = UserManager(self.data_manager) # UserManager reads and writes users through data_manager
        self.transaction_manager = TransactionManager(self.data_manager) # TransactionManager reads and writes transactions through data_manager
        self.current_user = None
        self.current_user_id = None

    # ---------------------------
    # MAIN MENU
    # ---------------------------
    def show_main_menu(self):
        print("\n💸 Your Personal Finance Manager")
        print("1. 🪪 Create User")
        print("2. 🔓 Login")
        print("3. 🔚 Exit")
        return input("👉🏼 Choose an option (1-3): ").strip()

    def run(self):
        while True:
            choice = self.show_main_menu()

            if choice == "1":
                self.user_manager.create_user()
            elif choice == "2":
                user = self.user_manager.login_user()
                if user:
                    self.current_user = user
                    self.current_user_id = user.get("user_id")
                    self.user_menu()  # open sub-menu after login
            elif choice == "3":
                self.exit_program()
                break
            else:
                print("❌ Invalid choice.")
            pause()

    # ---------------------------
    # USER SUBMENU
    # ---------------------------
    def user_menu(self):
        while True:
            current = self.user_manager.current_user
            print(f"\n👤 Welcome, {current['name']}")
            print("1. 👁️ View Profile")
            print("2. 🔑 Change Password")
            print("3. 🔄 Switch User")
            print("4. ➕ Add Transaction")
            print("5. 📊 View Transactions")
            print("6. 🔒 Logout")

            choice = input("👉🏼 Choose an option (1-6): ").strip()

            if choice == "1":
                self.user_manager.view_profile()
            elif choice == "2":
                self.user_manager.change_password()
            elif choice == "3":
                self.user_manager.switch_user()
            elif choice == "4":
                self.transaction_manager.add_transactions_loop(self.current_user_id)
            elif choice == "5":
                self.transaction_manager.print_all_for_user(self.current_user_id)
            elif choice == "6":
                self.user_manager.logout()  # Auto-saves and clears user
                return  # goes back to main menu
            else:
                print("❌ Invalid choice.")
            pause()

    # ---------------------------
    # EXIT PROGRAM
    # ---------------------------
    def exit_program(self):
        self.data_manager.create_backup_once()
        self.data_manager.save_transactions()
        print("👋🏼 Goodbye!")

if __name__ == "__main__":
    app = PersonalFinanceApp()
    app.run()