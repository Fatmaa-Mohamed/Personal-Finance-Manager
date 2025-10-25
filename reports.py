from datetime import datetime, date
from collections import defaultdict
from utils import clear_screen, parse_date
from data_manager import DataManager
from decimal import Decimal as decimal
import calendar

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

    def ascii_category_bars(self, user_id: str):
        """
        ASCII bar chart by expense category.
        Uses all transactions for the user.
        """

        # Group totals by category (only expenses)
        sums = defaultdict(float)
        for t in self.data_manager.get_transactions(user_id):
            if t.get("type") == "expense":
                cat = t.get("category", "Uncategorized")
                try:
                    amt = float(t.get("amount", 0))
                    sums[cat] += amt
                except ValueError:
                    continue

        if not sums:
            print("\nNo expenses found to visualize.\n")
            return

        # Scale bars
        max_val = max(sums.values())
        scale = max_val / 40 if max_val > 0 else 1  # 40 chars wide max

        print("\n📊 Expense Breakdown by Category (ASCII)")
        print("-" * 50)
        for cat, total in sorted(sums.items(), key=lambda x: -x[1]):
            bar_len = int(total / scale)
            bar = "#" * bar_len
            print(f"{cat:<15} | {bar} {total:.2f}")
        print("-" * 50)

    def ascii_last_12_months_vertical(self, user_id: str):
        """
        Vertical ASCII chart of total expenses over the last 12 months.
        Each column = one month. The higher the column, the higher the expense.
        """
        from datetime import date
        from collections import defaultdict
        import calendar
        from utils import parse_date

        txs = self.data_manager.get_transactions(user_id)
        if not txs:
            print("\nNo transactions found.\n")
            return

        today = date.today()
        year, month = today.year, today.month
        totals = defaultdict(float)

        # 1️⃣ Aggregate totals per (year, month)
        for t in txs:
            if t.get("type") != "expense":
                continue
            d = parse_date(str(t.get("date", "")))
            key = (d.year, d.month)
            totals[key] += float(t.get("amount", 0) or 0)

        # 2️⃣ Build list of last 12 months
        months = []
        for i in range(12):
            m = month - i
            y = year
            if m <= 0:
                m += 12
                y -= 1
            months.append((y, m))
        months.reverse()

        # 3️⃣ Prepare data
        vals = [totals.get(k, 0.0) for k in months]
        max_val = max(vals) if vals else 1
        scale = max_val / 10 if max_val > 0 else 1  # max 10 rows high

        # 4️⃣ Build 2D grid (10 rows × 12 months)
        grid = []
        for level in range(10, 0, -1):
            row = ""
            threshold = level * scale
            for v in vals:
                row += " █ " if v >= threshold else "   "
            grid.append(row)

        # 5️⃣ Print chart
        print("\n📊 Expense Trend - Last 12 Months (Vertical ASCII)")
        print("-" * 50)
        for r in grid:
            print(r)
        print("-" * 50)
        print("".join([f"{calendar.month_abbr[m][0:3]:^3}" for (_, m) in months]))
        print("".join([f"{v:>3.0f}" for v in vals]))
        print("-" * 50)



