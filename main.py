from user_manager import UserManager
from data_manager import DataManager  # not used yet
from transactions import TransactionManager # not used yet
from utils import pause # not used yet by present

class PersonalFinanceApp:
    """Main app controller."""

    def __init__(self):
        self.data_manager = DataManager() # not used yet will be used for JSON files handling
        self.user_manager = UserManager(self.data_manager) # UserManager reads and writes users through data_manager
        self.transaction_manager = TransactionManager(self.data_manager) # TransactionManager reads and writes transactions through data_manager
        self.current_user = None

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
                self.current_user = self.user_manager.login_user()
                if self.current_user:
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
            print(f"\n👤 Welcome, {self.current_user['name']}")
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
                switched_user = self.user_manager.switch_user()
                if switched_user:
                    self.current_user = switched_user
            elif choice == "4":
                self.transaction_manager.add_transaction(self.current_user)
            elif choice == "5":
                self.transaction_manager.view_transactions(self.current_user)
            elif choice == "6":
                self.user_manager.logout()  # Auto-saves and clears user
                self.current_user = None
                return  # goes back to main menu
            else:
                print("❌ Invalid choice.")
            pause()

    # ---------------------------
    # EXIT PROGRAM
    # ---------------------------
    def exit_program(self):
        # no need to save users, logout already does it
        self.transaction_manager.save_transactions()
        print("👋🏼 Goodbye!")

if __name__ == "__main__":
    app = PersonalFinanceApp()
    app.run()