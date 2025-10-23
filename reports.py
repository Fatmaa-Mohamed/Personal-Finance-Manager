from datetime import datetime
from collections import defaultdict
from utils import clear_screen
from data_manager import DataManager

class Reports:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        #initializing our data manager

    def show_dashboard_summary(self, user_id: str):
        clear_screen()
        print("=== 📊 DASHBOARD SUMMARY ===")
        # txns = transactions
        txns = self.data_manager.load_transactions()
