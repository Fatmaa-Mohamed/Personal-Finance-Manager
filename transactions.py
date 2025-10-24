from utils import input_non_empty, input_positive_float, today_str
from decimal import Decimal as decimal
class TransactionManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.transactions = self.data_manager.load_transactions()

        try:
            self.transactions = self.data_manager.load_transactions()
        except AttributeError:
            raise RuntimeError("Data manager has not been initialized.")

    def _next_transaction_id(self) -> str:
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
        self.data_manager.save_transactions(self.transactions)


    # CRUD operations
   # -------------------- Create ----------------
    def add_transaction(self, user_id: str, t_type: str, amount: decimal, category: str,
                        date:str, description:str ,payment_method: str) -> dict:

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
        return t

    # ------------ Read -------------
    def list_transactions(self, user_id: str) -> list:
        #return all transactions for a specific user id
        return [t for t in self.transactions if t.get("user_id") == user_id]

    # ---------------- update -----------

    def update_transaction(self, transaction_id: str, updates: dict) -> bool:
        for i, t in enumerate(self.transactions):
            if t.get("transaction_id") == transaction_id:
                t.update(updates)
                self._save()
                return True

        return False

    #------------------ Delete ----------------

    def delete_transaction(self, transaction_id: str) -> bool:
        for i, t in enumerate(self.transactions):
            if t.get("transaction_id") == transaction_id:
                self.transactions.pop(i)
                self._save()
                return True
        return False

    def compute_total(self, user_id: str) -> dict:
        income = sum(t["amount"] for t in self.transactions
                     if t.get("user_id") == user_id and t.get("type") == "income")
        expense = sum(t["amount"] for t in self.transactions
                      if t.get("user_id") == user_id and t.get("type") == "expense")
        return {"income": income, "expense": expense, "balance": income - expense}


    #----------------- interactive GUI ---------------
    # --------- Print all of user transactions --------
    def print_all_for_user(self, user_id):
        user_txs = self.list_transactions(user_id)
        if not user_txs:
            print("No transactions found.")
            return

        print("\n===== Transactions =====")
        print(f"{'ID':<8} {'Type':<8} {'Amount':>10}  {'Category':<14} {'Date':<10}  {'Payment':<12} Description")
        print("-" * 90)

        for t in user_txs:
            print(f"{t['transaction_id']:<8} {t['type']:<8} {t['amount']:>10.2f}  "
                  f"{t['category']:<14} {t['date']:<10}  {t['payment_method']:<12} {t['description']}")

        print("-" * 90)
        total = self.compute_total(user_id)
        print(f"Income:  {total['income']:.2f}")
        print(f"Expense: {total['expense']:.2f}")
        print(f"Balance: {total['balance']:.2f}\n")

    # --------- add income -------------
    def add_income(self, user_id: str):
        print("\n➕ Add INCOME")
        amount = input_positive_float("Amount: ")
        category = input_non_empty("Category: ")
        input_date = input(f"Date: (Enter for {today_str()}): ").strip()
        date = input_date if input_date else today_str()
        description = input("Description: ").strip()
        payment_method = input_non_empty("Payment Method: ").strip()

        t=self.add_transaction(
            user_id=user_id,
            t_type="income",
            amount=amount,
            category=category,
            date=date,
            description=description,
            payment_method=payment_method
        )

        print(f"✅ Saved income #{t['transaction_id']}!\n")

    # -------- add expense --------
    def add_expense(self, user_id: str):
        print("\n➖ Add EXPENSE")
        amount = input_positive_float("Amount: ")
        category = input_non_empty("Category: ")
        input_date = input(f"Date: (Enter for {today_str()}): ").strip()
        date = input_date if input_date else today_str()
        description = input("Description: ").strip()
        payment_method = input_non_empty("Payment Method: ").strip()
        t = self.add_transaction(
            user_id=user_id,
            t_type="expense",
            amount=amount,
            category=category,
            date=date,
            description=description,
            payment_method=payment_method
        )
        print(f"✅ Saved expense #{t['transaction_id']}!\n")

    # ----------- Add transaction loop ------------
    def add_transactions_loop(self, user_id: str):
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
                amount = amount,
                category = category,
                date = date,
                description = description,
                payment_method =payment_method
            )
            print(f"✅ Saved {t_type} #{t['transaction_id']}!\n")
            added_count += 1

        print(f"✔️ Done. Added {added_count} transaction(s).\n")

    #----------- edit transaction ----------------
    def edit_transaction(self, user_id: str):
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
        new_date = input(f"Date [YYYY-MM-DD] [{tx['date']}]: ").strip() or tx["date"]
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
        user_txs = self.list_transactions(user_id)


    def menu(self, user_id: str):
        while True:
            print("""
                    === Transactions ===
                    1) Add Income
                    2) Add Expense
                    3) View All
                    4) Edit
                    5) Delete
                    6) Back
                    """)
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.add_income(user_id)
            elif choice == "2":
                self.add_expense(user_id)
            elif choice == "3":
                self.print_all_for_user(user_id)
            elif choice == "4":
                self.edit_transaction(user_id)
            elif choice == "5":
                self.delete_transaction_interactive(user_id)
                break
            else:
                print("❌ Invalid choice.")











