from user_manager import UserManager
from data_manager import DataManager
from transactions import TransactionManager
from reports import Reports
from utils import pause
import atexit

class PersonalFinanceApp:
    """Main app controller."""

    def __init__(self):
        self.data_manager = DataManager() # Used for JSON files handling
        self.user_manager = UserManager(self.data_manager) # UserManager reads and writes users through data_manager
        self.transaction_manager = TransactionManager(self.data_manager) # TransactionManager reads and writes transactions through data_manager
        self.reports = Reports(self.data_manager)
        self.current_user = None
        self.current_user_id = None

    # ---------------------------
    # MAIN MENU
    # ---------------------------
    def show_main_menu(self):
        print("\n💸 Your Personal Finance Manager")
        print("1. 🪪 Create User")
        print("2. 🔓 Login")
        print("3. ❓ Help")
        print("4. 🔚 Exit")
        return input("👉🏼 Choose an option (1-4): ").strip()

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
                self.show_help()
            elif choice == "4":
                self.exit_program()
                break
            else:
                print("❌ Invalid choice.")
            pause()

    #----------------------------
    # HELP SYSTEM
    #----------------------------

    def show_help(self):
        """Interactive help system"""
        print("\n" + "="*50)
        print("📖 HELP SYSTEM")
        print("="*50)
        
        # General overview first
        print("\n🎯 WELCOME TO PERSONAL FINANCE MANAGER!")
        print("This app helps you track income, expenses, and reach your financial goals.")
        print("\nLet's explore what you can do...\n")
        
        # Ask about each section
        if self.current_user:
            # User is logged in - show all options
            self.help_transactions()
            self.help_reports()
            self.help_data_management()
            self.help_user_management()
        else:
            # User not logged in - show basic help
            self.help_getting_started()
            self.show_quick_tips()
    
    def help_getting_started(self):
        """Help for users who aren't logged in"""
        print("\n📝 GETTING STARTED")
        print("-" * 50)
        print("To use the app, you need to:")
        print("  1. Create a user account (Choose option 1)")
        print("  2. Login with your credentials (Choose option 2)")
        print("  3. Start tracking your finances!")
        print("\n💡 Your password must have:")
        print("  • At least 8 characters")
        print("  • Uppercase and lowercase letters")
        print("  • Numbers and special characters (@$!%*?&)")
        
    def help_transactions(self):
        """Help for transaction management"""
        response = input("\n❓ Do you want help with TRANSACTIONS? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print("\n💰 TRANSACTIONS MENU - What You Can Do:")
            print("-" * 50)
            print("1️⃣  ADD TRANSACTION")
            print("    • Record income (salary, gifts) or expenses (bills, shopping)")
            print("    • Enter amount, category, date, and payment method")
            print("    • Tip: Use consistent categories for better reports!")
            
            print("\n2️⃣  VIEW ALL TRANSACTIONS")
            print("    • See complete list of your transactions")
            print("    • Shows totals for income, expenses, and balance")
            
            print("\n3️⃣  EDIT TRANSACTION")
            print("    • Fix mistakes or update details")
            print("    • Press Enter to keep current values")
        
            print("\n4️⃣  DELETE TRANSACTION")
            print("    • Remove unwanted transactions")
            print("    • Confirmation required for safety")
            
            print("\n5️⃣  ADD RECURRING TRANSACTION")
            print("    • Set up repeating income/expenses")
            print("    • Monthly: Rent, subscriptions (choose day)")
            print("    • Yearly: Insurance, memberships (choose date)")
            
            print("\n6️⃣  SAVINGS GOAL")
            print("    • Set a target amount to save")
            print("    • Track progress automatically")
            print("    • Tip: Category must be 'savings' to count!")
            
            # Ask if they want to go to transactions menu
            go_there = input("\n➡️  Go to Transactions Menu now? (y/n): ").strip().lower()
            if go_there in ['y', 'yes']:
                if self.current_user_id:
                    self.transaction_manager.menu(self.current_user_id)
                else:
                    print("⚠️  You need to login first!")
                    pause()
                
    def help_reports(self):
        """Help for reports and analytics"""
        response = input("\n❓ Do you want help with REPORTS? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print("\n📊 REPORTS MENU - What You Can Do:")
            print("-" * 50)
            print("1️⃣  DASHBOARD SUMMARY")
            print("    • Quick overview of your finances")
            print("    • Total income, expenses, and current balance")
            
            print("\n2️⃣  MONTHLY REPORT")
            print("    • Detailed breakdown for specific month")
            print("    • Enter year and month to view")
            
            print("\n3️⃣  CATEGORY BREAKDOWN")
            print("    • See how much you spend per category")
            print("    • Identifies your biggest expense areas")
            
            print("\n4️⃣  SPENDING TRENDS")
            print("    • Track spending patterns over time")
            print("    • Shows monthly expense totals")
            
            print("\n5️⃣  SEARCH & FILTER")
            print("    • Find specific transactions")
            print("    • Filter by: category, date range, amount range")
            print("    • Sort by: date or amount")
            
            print("\n6️⃣  ASCII CATEGORY BARS")
            print("    • Visual bar chart of expenses by category")
            print("    • See spending distribution at a glance")
            
            print("\n7️⃣  ASCII LAST 12 MONTHS")
            print("    • Vertical chart showing expense trends")
            print("    • Compare spending across months")
            
            # Ask if they want to go to reports menu
            go_there = input("\n➡️  Go to Reports Menu now? (y/n): ").strip().lower()
            if go_there in ['y', 'yes']:
                if self.current_user_id:
                    self.reports.menu(self.current_user_id)
                else:
                    print("⚠️  You need to login first!")
                    pause()
                    
    def help_data_management(self):
        """Help for data import/export"""
        response = input("\n❓ Do you want help with DATA MANAGEMENT? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print("\n📂 DATA MANAGEMENT - What You Can Do:")
            print("-" * 50)
            print("1️⃣  EXPORT TRANSACTIONS TO CSV")
            print("    • Save your transactions to a CSV file")
            print("    • Open in Excel or Google Sheets")
            print("    • Great for backups or sharing with accountant")
            print("    • Example path: exports/my_data.csv")
            
            print("\n2️⃣  IMPORT TRANSACTIONS FROM CSV")
            print("    • Load transactions from a CSV file")
            print("    • Automatically avoids duplicates")
            print("    • File must have correct columns:")
            print("      transaction_id, user_id, type, amount,")
            print("      category, date, description, payment_method")
            
            print("\n💡 TIPS:")
            print("  • Data is auto-saved after every change")
            print("  • Backups created automatically when you exit")
            print("  • Backups kept for 10 days in data/backup/")
            
            # Ask if they want to go to data menu
            go_there = input("\n➡️  Go to Data Management Menu now? (y/n): ").strip().lower()
            if go_there in ['y', 'yes']:
                if self.current_user_id:
                    self.data_menu()
                else:
                    print("⚠️  You need to login first!")
                    pause()
                    
    def help_user_management(self):
        """Help for user account features"""
        response = input("\n❓ Do you want help with USER MANAGEMENT? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print("\n👤 USER MANAGEMENT - What You Can Do:")
            print("-" * 50)
            print("1️⃣  VIEW PROFILE")
            print("    • See your account information")
            print("    • Shows: User ID, name, currency")
            
            print("\n2️⃣  CHANGE PASSWORD")
            print("    • Update your password for security")
            print("    • Must enter old password first")
            print("    • New password must meet strength requirements")
            
            print("\n3️⃣  SWITCH USER")
            print("    • Log in as a different user")
            print("    • Perfect for shared computers")
            print("    • Data is auto-saved before switching")
            
            print("\n💡 SECURITY TIPS:")
            print("  • Use unique passwords for each user")
            print("  • Change password regularly")
            print("  • Always logout when done")
            
            pause()
            
    def show_quick_tips(self):
        """Show quick tips and best practices"""
        print("\n💡 QUICK TIPS FOR SUCCESS")
        print("-" * 50)
        print("✓ Add transactions regularly (daily is best)")
        print("✓ Use consistent category names")
        print("✓ Check your dashboard weekly")
        print("✓ Set realistic savings goals")
        print("✓ Review monthly reports to spot trends")
        print("✓ Export data monthly for backup")
        print("✓ Use descriptive names for transactions")
        print("-" * 50)
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
            print("4. 💰 Transactions Menu")
            print("5. 📊 Reports Menu")
            print("6. 📂 Data Management")
            print("7. ❓ Help")
            print("8. 🔒 Logout")

            choice = input("👉🏼 Choose an option (1-8): ").strip()

            if choice == "1":
                self.user_manager.view_profile()
            elif choice == "2":
                self.user_manager.change_password()
            elif choice == "3":
                new_user = self.user_manager.switch_user()
                if new_user:
                    self.current_user = new_user
                    self.current_user_id = new_user["user_id"]
                    print(f"🔄 Now logged in as {new_user['name']}")
                else:
                    print("⚠️ Switch cancelled or failed.")
            elif choice == "4":
                self.transaction_manager.menu(self.current_user_id)
            elif choice == "5":
                self.reports.menu(self.current_user_id)
            elif choice == "6":
                self.data_menu()
            elif choice == "7":
                self.show_help()
            elif choice == "8":
                self.user_manager.logout()
                return
            else:
                print("❌ Invalid choice.")
            pause()


    # ---------------------------
    # DATA MANAGEMENT SUBMENU
    # ---------------------------

    def data_menu(self):
        while True:
            print("\n=== 📂 Data Management ===")
            print("1. Export transactions to CSV")
            print("2. Import transactions from CSV")
            print("3. Back")
            
            choice = input("👉🏼 Choose an option (1-3): ").strip()
            user_id = self.current_user_id
            
            if choice == "1":
                path = input("Enter file path to export to: ")
                tx_list = self.data_manager.load_transactions()
                self.data_manager.export_transactions_csv(user_id, tx_list, path)
                print("✅ Transactions exported successfully.")
            elif choice == "2":
                path = input("Enter file path to import from: ")
                added = self.data_manager.import_transactions_csv(user_id, path)
                print(f"✅ Imported {added} new transactions.")
            elif choice == "3":
                return
            else:
                print("❌ Invalid choice.")
            pause()

    # ---------------------------
    # EXIT PROGRAM
    # ---------------------------
    def exit_program(self):
        print("👋🏼 Goodbye!")

if __name__ == "__main__":
    app = PersonalFinanceApp()
    atexit.register(app.data_manager.create_backup_once) # insure backup is created even if we don't exit program properly
    app.run()