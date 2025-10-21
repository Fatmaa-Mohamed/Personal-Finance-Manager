from utils import input_non_empty, input_positive_float, today_str
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



