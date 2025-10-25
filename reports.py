from datetime import datetime
from collections import defaultdict
from utils import pause
from data_manager import DataManager
from decimal import Decimal as decimal

class Reports:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        #initializing our data manager
    # ----------------- dashboard summary ----------------
    def show_dashboard_summary(self, user_id: str):
        print("=== 📊 DASHBOARD SUMMARY ===")
        # txns = transactions
        txns = self.data_manager.get_transactions(user_id)

        total_income = sum(t['amount'] for t in txns if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in txns if t['type'] == 'expense')
        balance = total_income - total_expense

        print(f"💰 Total Income:  {total_income:.2f}")
        print(f"💸 Total Expense: {total_expense:.2f}")
        print(f"🧾 Balance:       {balance:.2f}\n")

    # ---------------- Monthly report -----------------
    def show_monthly_report(self, user_id: str, year:int, month: int):
        print(f"=== 📅 REPORT for {year}-{month:02d} ===")

        txns = self.data_manager.get_transactions(user_id)

        monthly_txns = [
            t for t in txns
            if datetime.strptime(t['date'], '%d/%m/%Y').year == year and
               datetime.strptime(t['date'], '%d/%m/%Y').month == month
        ]

        if not monthly_txns:
            print("No transactions for this month.")
            return

        total_income = sum(t['amount'] for t in txns if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in txns if t['type'] == 'expense')
        net = total_income - total_expense

        print(f"Income: {total_income:.2f}")
        print(f"Expense: {total_expense:.2f}")
        print(f"net: {net:.2f}")

    #-------------- Category BreakDown ------------

    def show_category_breakdown(self, user_id: str):
        print("=== 📂 CATEGORY BREAKDOWN ===")

        txns = self.data_manager.get_transactions(user_id)
        categories = defaultdict(lambda: {"income": decimal("0"), "expense": decimal("0")})

        for t in txns:
            if t['type'] == 'income':
                categories[t['category']]['income'] += t['amount']
            elif t['type'] == 'expense':
                categories[t['category']]['expense'] += t['amount']
            
        if not categories:
            print("No transactions found!")
            return
        
        print(f"{'Category':<20} | {'Income':>10} | {'Expense':>10}")
        print("-" * 45)
        for category, totals in categories.items():
            print(f"{category:<20} | {totals['income']:>10.2f} | {totals['expense']:>10.2f}")

    # -------------- Spending trends --------------
    def show_spending_trends(self, user_id: str):
        print("=== 📈 SPENDING TRENDS ===")

        txns = self.data_manager.get_transactions(user_id)
        monthly_expenses = defaultdict(decimal)

        for t in txns:
            if t['type'] == 'expense':
                date = datetime.strptime(t['date'], '%d/%m/%Y')
                month_key = f"{date.year}-{date.month:02d}"
                monthly_expenses[month_key] += t['amount']

        if not monthly_expenses:
            print("No transactions for this month.")
            return

        for month, total in sorted(monthly_expenses.items()):
            print(f"{month}: {total:.2f}")

    # ----------------- Search & Filter Menu -----------------
    def search_and_filter_menu(self, user_id: str):
        """Interactive menu for searching, filtering, and sorting transactions."""
        while True:
            print("=== 🔍 SEARCH & FILTER MENU ===")
            print("1.  🏷️ Filter by Category")
            print("2.  📆 Filter by Date Range")
            print("3.  💵 Filter by Amount Range")
            print("4.  🔢 Sort Transactions")
            print("5.  🔙 Back to Reports Menu")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.filter_by_category(user_id)
            elif choice == "2":
                self.filter_by_date_range(user_id)
            elif choice == "3":
                self.filter_by_amount_range(user_id)
            elif choice == "4":
                self.sort_transactions(user_id)
            elif choice == "5":
                return
            else:
                print("Invalid choice!")

    # ---------------- Filter by Category ----------------
    def filter_by_category(self, user_id: str):
        txns = self.data_manager.get_transactions(user_id)
        category = input("Enter category name: ").lower()
        results = [t for t in txns if t['category'].lower() == category]
        self.display_results(results)

    # ---------------- Filter by Date Range ----------------
    def filter_by_date_range(self, user_id: str):
        txns = self.data_manager.get_transactions(user_id)
        start = input("Start date (DD/MM/YYYY): ")
        end = input("End date (DD/MM/YYYY): ")

        try:
            start_date = datetime.strptime(start, "%d/%m/%Y")
            end_date = datetime.strptime(end, "%d/%m/%Y")
        except ValueError:
            print("Invalid date format!")
            pause()
            return

        results = [
            t for t in txns
            if start_date <= datetime.strptime(t['date'], "%d/%m/%Y") <= end_date
        ]

        self.display_results(results)

    # ---------------- Filter by Amount Range ----------------
    def filter_by_amount_range(self, user_id: str):
        txns = self.data_manager.get_transactions(user_id)
        try:
            min_amt = decimal(input("Minimum amount: "))
            max_amt = decimal(input("Maximum amount: "))
        except ValueError:
            print("Please enter valid numbers!")
            pause()
            return

        results = [t for t in txns if min_amt <= t['amount'] <= max_amt]
        self.display_results(results)

    # ---------------- Sort Transactions ----------------
    def sort_transactions(self, user_id: str):
        txns = self.data_manager.get_transactions(user_id)

        print("Sort by:")
        print("1. Date (newest first)")
        print("2. Date (oldest first)")
        print("3. Amount (high to low)")
        print("4. Amount (low to high)")
        choice = input("Choose option: ").strip()

        if choice == "1":
            results = sorted(txns, key=lambda t: datetime.strptime(t['date'], "%d/%m/%Y"), reverse=True)
        elif choice == "2":
            results = sorted(txns, key=lambda t: datetime.strptime(t['date'], "%d/%m/%Y"))
        elif choice == "3":
            results = sorted(txns, key=lambda t: t['amount'], reverse=True)
        elif choice == "4":
            results = sorted(txns, key=lambda t: t['amount'])
        else:
            print("Invalid choice!")
            pause()
            return

        self.display_results(results)

    # ---------------- Helper to Display Results ----------------
    def display_results(self, results):
        if not results:
            print("No matching transactions found.")
        else:
            print("=== RESULTS ===")
            print(f"{'Date':<12} | {'Type':<12} | {'Category':<15} | {'Amount':<12} | {'Description':<15}")
            print("-" * 80)
            for t in results:
                print(f"{t['date']:<12} | {t['type']:<12} | {t['category']:<15} | {t['amount']:<12} | {t['description']:<15}")
        pause()
    
    #-----------------Submenu for reports------------------------

    def menu(self, user_id: str):
        while True:
            # clear_screen()
            print("=== 📊 REPORTS MENU ===")
            print("1. 🧮 Dashboard Summary")
            print("2. 🗓️ Monthly Report")
            print("3. 📂 Category Breakdown")
            print("4. 📈 Spending Trends")
            print("5. 🔍 Search & Filter")
            print("6. 🔙 Back")

            choice = input("👉 Choose an option (1–6): ").strip()
            
            if choice == "1":
                self.show_dashboard_summary(user_id)
            
            elif choice == "2":
                try:
                    year = int(input("Enter year (YYYY): "))
                    month = int(input("Enter month (1–12): "))
                    self.show_monthly_report(user_id, year, month)
                except ValueError:
                    print("❌ Invalid input. Please enter valid numbers for year and month.")
            
            elif choice == "3":
                self.show_category_breakdown(user_id)
            
            elif choice == "4":
                self.show_spending_trends(user_id)
            
            elif choice == "5":
                self.search_and_filter_menu(user_id)
            
            elif choice == "6":
                print("↩️ Returning to user menu...")
                return
            
            else:
                print("❌ Invalid choice! Please select 1–5.")