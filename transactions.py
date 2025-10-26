from utils import input_non_empty, input_positive_float, today_str, next_yearly_date, next_monthly_date, today_date, parse_date, format_date, pause
from decimal import Decimal as decimal
from datetime import timedelta
class TransactionManager:
    def __init__(self, data_manager):
        """Initialize the transaction manager and load persisted transactions.
        Expects a data_manager with load/save methods."""
        self.data_manager = data_manager

        try:
            self.transactions = self.data_manager.load_transactions()
        except AttributeError:
            raise RuntimeError("Data manager has not been initialized.")

    def _next_transaction_id(self) -> str:
        """Return the next sequential transaction ID in the format TXN###.
        Scans existing records to find the max and increments it."""
        max_num = 0
        for t in self.transactions:
            tid = t.get("transaction_id", "")
            if tid.startswith("TXN"):
                try:
                    num = int(tid[3:])
                    if num > max_num:
                        max_num = num
                except ValueError:
                    pass
        return f"TXN{max_num + 1:03d}"

    def _save(self):
        """Persist the in-memory transactions list to storage via data_manager."""
        self.data_manager.save_transactions(self.transactions)


    # CRUD operations
   # -------------------- Create ----------------
    def add_transaction(self, user_id: str, t_type: str, amount: decimal, category: str,
                        date: str, description: str, payment_method: str) -> dict:
        """Create and persist a new transaction record for the given user.
        If category == 'savings', prompt to choose a goal and update its progress."""

        # 1️⃣ Create transaction normally
        t = {
            "transaction_id": self._next_transaction_id(),
            "user_id": user_id,
            "type": t_type,
            "amount": amount,
            "category": category,
            "date": date,
            "description": description,
            "payment_method": payment_method
        }
        self.transactions.append(t)
        self._save()

        # 2️⃣ Handle savings goal contribution
        if category.lower() == "savings" and t_type.lower() == "expense":
            try:
                goals = self.data_manager.load_goals(user_id) or []
            except Exception:
                goals = []

            if not goals:
                print("⚠️ You have no savings goals yet. Create one first.")
                return t

            print("\n💰 Your Savings Goals:")
            for idx, g in enumerate(goals, start=1):
                saved = float(g.get("saved_snapshot", 0))
                target = float(g.get("target", 0))
                remaining = max(0, target - saved)
                progress = 0 if target == 0 else min(100, (saved / target) * 100)
                print(
                    f"{idx}. {g['name']} — Target: {target:.2f}, Saved: {saved:.2f}, Remaining: {remaining:.2f}, Progress: {progress:.1f}%")

            # Choose goal
            while True:
                choice = input(f"\nSelect goal number (1-{len(goals)}): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(goals):
                    goal = goals[int(choice) - 1]
                    break
                print("❌ Invalid choice. Try again.")

            # 3️⃣ Update the goal
            goal["saved_snapshot"] = float(goal.get("saved_snapshot", 0)) + float(amount)
            target = float(goal["target"])
            remaining = max(0.0, target - goal["saved_snapshot"])
            progress = min(100.0, (goal["saved_snapshot"] / target) * 100.0)

            print("\n=== Updated Goal Summary ===")
            print(f"Goal: {goal['name']}")
            print(f"Target: {target:.2f}")
            print(f"Saved: {goal['saved_snapshot']:.2f}")
            print(f"Remaining: {remaining:.2f}")
            print(f"Progress: {progress:.1f}%")

            # 4️⃣ Remove goal if complete
            if goal["saved_snapshot"] >= target:
                print(f"🎉 Goal '{goal['name']}' reached! It has been removed from active goals.")
                goals.remove(goal)

            # 5️⃣ Save goals
            try:
                self.data_manager.save_goals(user_id, goals)
            except Exception as e:
                print(f"⚠️ Could not save updated goals: {e}")

        return t
    # ------------ Read -------------
    def list_transactions(self, user_id: str) -> list:
        """Return all transactions belonging to the given user_id as a list."""
        #return all transactions for a specific user id
        return [t for t in self.transactions if t.get("user_id") == user_id]

    # ---------------- update -----------

    def update_transaction(self, transaction_id: str, updates: dict) -> bool:
        """Update fields of a transaction by ID and persist changes.
        Returns True if updated, False if not found."""
        for i, t in enumerate(self.transactions):
            if t.get("transaction_id") == transaction_id:
                t.update(updates)
                self._save()
                return True

        return False

    #------------------ Delete ----------------

    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction by ID and persist changes.
        Returns True if deleted, False if not found."""
        for i, t in enumerate(self.transactions):
            if t.get("transaction_id") == transaction_id:
                self.transactions.pop(i)
                self._save()
                return True
        return False

    def compute_total(self, user_id: str) -> dict:
        """Compute total income, expense, and balance for the given user.
        Returns a dict with keys: income, expense, balance."""
        income = sum(
            decimal(str(t["amount"]))
            for t in self.transactions
            if t.get("user_id") == user_id and t.get("type") == "income"
        )
        expense = sum(
            decimal(str(t["amount"]))
            for t in self.transactions
            if t.get("user_id") == user_id and t.get("type") == "expense"
        )
        return {"income": income, "expense": expense, "balance": income - expense}


    #----------------- interactive GUI ---------------
    # --------- Print all of user transactions --------
    def print_all_for_user(self, user_id):
        """Print a table of all transactions for the user along with totals."""
        user_txs = self.list_transactions(user_id)
        if not user_txs:
            print("No transactions found.")
            return

        print("\n===== Transactions =====")
        print(f"{'ID':<8} {'Type':<8} {'Amount':>10}  {'Category':<14} {'Date':<10}  {'Payment':<12} Description")
        print("-" * 90)

        for t in user_txs:
            print(f"{t['transaction_id']:<8} {t['type']:<8} {t['amount']:>10}  "
                  f"{t['category']:<14} {t['date']:<10}  {t['payment_method']:<12} {t['description']}")

        print("-" * 90)
        total = self.compute_total(user_id)
        print(f"Income:  {total['income']}")
        print(f"Expense: {total['expense']}")
        print(f"Balance: {total['balance']}\n")

    # ----------- Add transaction loop ------------
    def add_transactions_loop(self, user_id: str):
        """Interactive loop to add multiple transactions until the user quits."""
        print("\n➕ Add Transactions (type 'q' to stop)\n")

        added_count = 0
        while True:
            t_type = input("type[income/expense] or q to quit: ")
            if t_type in ("q", "quit"):
                break
            if t_type not in ("income", "expense"):
                print("❌ Please enter 'income' or 'expense' (or 'q' to quit).")
                continue

            amount = input_positive_float("Amount: ")
            category = input_non_empty("Category: ")
            input_date = input(f"Date: (Enter for {today_str()}): ").strip()
            date = input_date if input_date else today_str()
            description = input("Description: ").strip()
            payment_method = input_non_empty("Payment Method: ").strip()
            t = self.add_transaction(
                user_id = user_id,
                t_type = t_type,
                amount = str(amount),
                category = category,
                date = date,
                description = description,
                payment_method = payment_method
            )
            print(f"✅ Saved {t_type} #{t['transaction_id']}!\n")
            added_count += 1

        print(f"✔️ Done. Added {added_count} transaction(s).\n")

    #----------- edit transaction ----------------
    def edit_transaction(self, user_id: str):
        """Interactively edit a single transaction chosen by ID."""
        user_txs = self.list_transactions(user_id)
        if not user_txs:
            print("\n(ℹ️) Nothing to edit for this user.\n")
            return

        self.print_all_for_user(user_id)
        tx_id = input("Enter transaction ID to edit (e.g., TXN003): ").strip()
        tx = next((t for t in user_txs if t["transaction_id"] == tx_id), None)
        if not tx:
            print("❌ Transaction not found.")
            return

        print("\nPress Enter to keep the current value.\n")
        # Type
        new_type = input(f"Type [income/expense] [{tx['type']}]: ").strip().lower()
        if new_type not in ("income", "expense", ""):
            print("⚠️ Invalid type. Keeping old.")
            new_type = tx["type"]
        else:
            new_type = tx["type"] if new_type == "" else new_type

        # Amount
        raw_amount = input(f"Amount [{tx['amount']}]: ").strip()
        if raw_amount == "":
            new_amount = tx["amount"]
        else:
            try:
                val = decimal(raw_amount)
                if val <= 0:
                    print("⚠️ Amount must be positive. Keeping old.")
                    new_amount = tx["amount"]
                else:
                    new_amount = val
            except ValueError:
                print("⚠️ Not a number. Keeping old.")
                new_amount = tx["amount"]

        # Category
        new_category = input(f"Category [{tx['category']}]: ").strip() or tx["category"]
        # Date
        new_date = input(f"Date [YYYY/MM/DD] [{tx['date']}]: ").strip() or tx["date"]
        # Description
        new_desc = input(f"Description [{tx['description']}]: ").strip() or tx["description"]
        # Payment method
        new_payment = input(f"Payment method [{tx['payment_method']}]: ").strip() or tx["payment_method"]

        updated = self.update_transaction(
            transaction_id=tx_id,
            updates={
                "type": new_type,
                "amount": new_amount,
                "category": new_category,
                "date": new_date,
                "description": new_desc,
                "payment_method": new_payment
            }
        )
        if updated:
            print("✏️ Transaction updated!\n")
        else:
            print("❌ Update failed.\n")

    # ------------- Delete transaction --------------

    def delete_transaction_interactive(self, user_id: str):
        """Interactively delete a transaction after confirmation."""
        user_txs = self.list_transactions(user_id)
        if not user_txs:
            print("No transactions found.")
            return

        self.print_all_for_user(user_id)
        tx_id = input("Enter transaction ID to delete: ").strip()
        tx = next((t for t in user_txs if t["transaction_id"] == tx_id), None)
        if not tx:
            print("❌ Transaction not found.")
            return

        confirm = input(f"Delete transaction [y/n]: ").strip().lower()
        if confirm != "y":
            print("❎ Deletion cancelled.\n")
            return

        if self.delete_transaction(tx_id):
            print(f"🗑️ Deleted transaction {tx_id}.\n")
        else:
            print("❌ Delete failed.\n")

    # ----------- AF: Recurring transaction ------------
    def recurring_transaction(self, user_id: str):
        """Create one or many future-dated recurring transactions (monthly/yearly).
        Each occurrence is saved as a normal transaction entry."""
        print("\n🔁 Add RECURRING (one or many occurrences)")

        #validate input
        while True:
            t_type = input("type[income/expense]: ").strip().lower()
            if t_type in {"income", "expense"}:
                break
            print("Please enter either 'income' or 'expense'.")

        amount = input_positive_float("Amount: ")
        category = input_non_empty("Category: ")
        description = input("Description: ").strip()
        payment_method = input_non_empty("Payment Method: ")

        while True:
            freq = input("Frequency[monthly/yearly]: ").strip().lower()
            if freq in {"monthly", "yearly"}:
                break
            print("Please enter 'monthly' or 'yearly'.")

        occurrence = input("How many occurrences to create now? (Enter for 1): ").strip()
        try:
            occ_count = int(occurrence) if occurrence else 1
            if occ_count <= 0:
                occ_count = 1
        except ValueError:
            occ_count = 1

        today = today_date()
        created = 0

        if freq == "monthly":
            while True:
                try:
                    day = int(input("Day of month (1–31): ").strip())
                    if 1 <= day <= 31:
                        break
                except ValueError:
                    pass
                print("Enter a number between 1 and 31.")

            date_obj = next_monthly_date(today, day)

            for _ in range(occ_count):
                t = self.add_transaction(
                    user_id=user_id,
                    t_type=t_type,
                    amount=amount,
                    category=category,
                    description=description,
                    payment_method=payment_method,
                    date=format_date(date_obj),
                )
                print(f"✅ Saved {t_type} #{t['transaction_id']} on {format_date(date_obj)}")
                created += 1
                # Move to the next month
                first_of_next = (date_obj.replace(day=28) + timedelta(days=4)).replace(day=1)
                date_obj = next_monthly_date(first_of_next, day)

        else: #yearly occurrence
            while True:
                raw = input("Date each year (dd/mm): ").strip()
                try:
                    dd, mm = raw.split("/")
                    day = int(dd)
                    month = int(mm)
                    if 1 <= month <= 12 and 1 <= day <= 31:
                        break
                except Exception:
                    pass
                print("Please enter a valid dd/mm like 05/10")

            date_obj = next_yearly_date(today, day, month)

            for _ in range(occ_count):
                t = self.add_transaction(
                    user_id=user_id,
                    t_type=t_type,
                    amount=amount,
                    category=category,
                    date=format_date(date_obj),
                    description=description,
                    payment_method=payment_method
                )
                print(f"✅ Saved {t_type} #{t['transaction_id']} on {format_date(date_obj)}")
                created += 1
                # Move to the next year
                first_of_next = (date_obj.replace(day=28) + timedelta(days=4)).replace(day=1)
                date_obj = next_yearly_date(first_of_next, day, month)

        print(f"✔️ Done. Created {created} occurrence(s).\n")


    #---------------------------------- AF: saving goals -------------------------------------------
    def savings_goal(self, user_id: str):
        """
        Create or update a savings goal for a specific user.
        Progress is calculated from 'savings' expenses.
        Stores all numbers as strings in JSON, uses Decimal for calculations.
        """
        print("\n🏆 Savings Goal")

        # Ask user for goal info
        name = input("Goal name (e.g., 'Emergency Fund') [Enter for 'Savings Goal']: ").strip() or "Savings Goal"
        target_str = input("Target amount: ").strip() or "0"
    
        try:
            target = decimal(target_str)
        except Exception:
            print("❌ Invalid number. Goal not created.")
            return
    
        # Load existing goals for this user
        goals = self.data_manager.load_goals(user_id) or []
    
        # Calculate how much this user has saved so far
        total_saved = decimal("0")
        for t in self.transactions:
            if (
                t.get("user_id") == user_id
                and str(t.get("type", "")).lower() == "expense"
                and str(t.get("category", "")).lower() == "savings"
            ):
                try:
                    total_saved += decimal(str(t.get("amount", "0")))
                except Exception:
                    pass
    
        # Check if goal already exists
        existing_goal = next((g for g in goals if g["name"].lower() == name.lower()), None)
        if existing_goal:
            existing_goal["target"] = str(target)
            existing_goal["saved"] = str(total_saved)
        else:
            goals.append({
                "name": name,
                "target": str(target),
                "saved": str(total_saved)
            })
    
        # Save updated goals for this user
        self.data_manager.save_goals(user_id, goals)
    
        # Compute progress
        remaining = max(decimal("0"), target - total_saved)
        pct = decimal("0") if target <= 0 else min(decimal("100"), (total_saved / target) * decimal("100"))
    
        # Display summary
        print("\n=== Savings Goal Summary ===")
        print(f"Goal:       {name}")
        print(f"Target:     {target:.2f}")
        print(f"Saved:      {total_saved:.2f}")
        print(f"Remaining:  {remaining:.2f}")
        print(f"Progress:   {pct:.1f}%")
    
        if remaining <= 0:
            print("🎉 Congrats! You've reached your savings goal!")
        print()

    def export_transactions_interactive(self, user_id: str):
        """Prompt for a file path and export the user's transactions to CSV."""
        print("\n💾 Export Transactions to CSV")
        path = input("Enter filename (e.g., data/exports/my_transactions.csv): ").strip()
        if not path:
            print("❌ No file path provided.")
            return
        tx_list = self.list_transactions(user_id)
        self.data_manager.export_transactions_csv(user_id, tx_list, path)
        print(f"✅ Exported {len(tx_list)} transactions to {path}\n")

    def import_transactions_interactive(self, user_id: str):
        """Prompt for a CSV path and import transactions, skipping duplicates."""
        print("\n📥 Import Transactions from CSV")
        path = input("Enter CSV file path to import: ").strip()
        if not path:
            print("❌ No file path provided.")
            return
        added = self.data_manager.import_transactions_csv(user_id, path)
        print(f"✅ Imported {added} new transactions.\n")

    #-------------------------Transactions menu----------------------------

    def menu(self, user_id: str):
        """Interactive transactions menu for creating, viewing, and managing entries."""
        while True:
            print("\n=== 💼 TRANSACTIONS MENU ===")
            print("1. ➕ Add Transaction")
            print("2. 📋 View All Transactions")
            print("3. ✏️ Edit Transaction")
            print("4. 🗑️ Delete Transaction")
            print("5. 🔁 Add Recurring Transaction")
            print("6. 🏆 Savings Goal")
            print("7. 💾 Export to csv")
            print("8. 📥 Import from csv")
            print("9. 🔙 Back")

            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.add_transactions_loop(user_id)
            elif choice == "2":
                self.print_all_for_user(user_id)
            elif choice == "3":
                self.edit_transaction(user_id)
            elif choice == "4":
                self.delete_transaction_interactive(user_id)
            elif choice == "5":
                self.recurring_transaction(user_id)
            elif choice == "6":
                self.savings_goal(user_id)
            elif choice == "7":
                self.export_transactions_interactive(user_id)
            elif choice == "8":
                self.import_transactions_interactive(user_id)
            elif choice == "9":
                return
            else:
                print("❌ Invalid choice.")
            pause()