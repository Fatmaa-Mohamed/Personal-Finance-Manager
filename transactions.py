from data_manager import DataManager
import uuid

class TransactionManager:
    def __init__(self, data_manager, get_current_user_id=None):
        self.data_manager = data_manager
        self.get_current_user_id = get_current_user_id
        self.current_user_id = self._get_user_id
        self.transactions = self.data_manager.load_transactions_for(self.current_user_id)

    def _get_user_id(self):
        if self.current_user_id:
            uid = self.get_current_user_id