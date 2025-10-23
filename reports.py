from datetime import datetime
from collections import defaultdict
from utils import clear_screen
from data_manager import DataManager
from decimal import Decimal as decimal

class Reports:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        #initializing our data manager
    # ----------------- dashboard summary ----------------
    def show_dashboard_summary(self, user_id: str):
        clear_screen()
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
        clear_screen()
        print(f"=== 📅 REPORT for {year}-{month:02d} ===")

        txns = self.data_manager.get_transactions(user_id)

        monthly_txns = [
            t for t in txns
            if datetime.strptime(t['date'], '%d-%m-%Y').year == year and
               datetime.strptime(t['date'], '%d-%m-%Y').month == month
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

        clear_screen()
        print("=== 📂 CATEGORY BREAKDOWN ===")

        txns = self.data_manager.get_transactions(user_id)
        categories = defaultdict(decimal)

        for t in txns:
            if t['type'] == 'expense':
                categories[t['category']] += t['amount']

        if not categories:
            print("No expenses found!")
            return

        for category, total in categories.items():
            print(f"{category:<20} | {total:.2f}")

    # -------------- Spending trends --------------
    def show_spending_trends(self, user_id: str):
        clear_screen()
        print("=== 📈 SPENDING TRENDS ===")

        txns = self.data_manager.get_transactions(user_id)
        monthly_expenses = defaultdict(decimal)

        for t in txns:
            if t['type'] == 'expense':
                date = datetime.strptime(t['date'], '%d-%m-%Y')
                month_key = f"{date.year}-{date.month:02d}"
                monthly_expenses[month_key] += t['amount']

        if not monthly_expenses:
            print("No transactions for this month.")
            return

        for month, total in sorted(monthly_expenses.items()):
            print(f"{month}: {total:.2f}")




