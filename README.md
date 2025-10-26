# Personal Finance Manager 💸
A simple, secure console-based Python application for tracking your personal finances. Manage multiple users, record transactions, set savings goals, and generate insightful reports - all from your terminal!

## ✨ What Can It Do?
- **👤 Multiple Users** - Everyone in your household can have their own account
- **💰 Track Money** - Record income and expenses with categories
- **🔁 Auto-Repeat** - Set up recurring bills and salaries
- **🎯 Savings Goals** - Track progress toward your financial targets
- **📊 Visual Reports** - See where your money goes with charts and summaries
- **💾 Auto-Save** - Never lose your data with automatic backups
- **📤 Import/Export** - Move data in and out using CSV files
- **❓ Interactive Help** - Get guidance anytime you need it

## 🚀 Quick Start

**1. Run the app:**
```python main.py```

2. **New to the app? Use the Help system!**
   - Choose Help from the main menu (option 3)
   - Follow the guided instructions

3. **Create your account:**
   - Choose option 1
   - Enter Enter a username, password, and currency

4. **Start tracking:**
   - Login and add your first transaction 🎉

## 📋 What You Need
- Python 3.7 or higher

## 📥 Installation
**Clone or download the repository:**
```
git clone https://github.com/Fatmaa-Mohamed/Personal-Finance-Manager.git
cd Personal-Finance-Manager
```

## 📁 Project structure
```
├── main.py              # Start here - main menu
├── user_manager.py      # Login and user stuff
├── transactions.py      # Add, edit, delete transactions
├── data_manager.py      # Saves everything automatically
├── reports.py           # Charts and summaries
└── utils.py             # Helper functions
```

The app creates a `data/` folder automatically to store your information safely.

## 💡 How to Use

### ➕ Adding a Transaction
```
Type: expense
Amount: 50
Category: Groceries
Date: (press Enter for today)
Description: Weekly shopping
Payment Method: Credit Card
✅ Saved!
```

### 🔁 Setting Up Recurring Transactions
Got a monthly subscription or weekly salary? Set it once and let the app create future transactions automatically!

- **Monthly**: Rent, subscriptions, etc.
- **Yearly**: Insurance, memberships, etc.

### 📊 Reports
- 📊 **Dashboard** - Total income, expenses, and balance
- 📅 **Monthly Report** - What happened this month?
- 🏷️ **By Category** - Where does your money go?
- 📈 **Trends** - Visual charts of your spending patterns

### Search & Filter
Find exactly what you're looking for:
- Filter by category, date range, or amount
- Sort by newest, oldest, highest, or lowest

## 🔒 Security
Your data is protected:
- ✅ Passwords are encrypted (SHA-256)
- ✅ Strong password requirements
- ✅ Hidden password entry
- ✅ Data stored locally on your computer

**Password Requirements:**
- At least 8 characters
- Uppercase, lowercase, numbers, and symbols

## 💾 Your Data
Everything is saved automatically in two formats:
- **JSON** - Main storage
- **CSV** - Easy-to-open backup

**Backups:**
- Created automatically when you exit
- Kept for 10 days
- Stored in `data/backup/`

## 🎯 Tips for Best Results
1. **Be Consistent** - Add transactions regularly
2. **Use Categories** - Makes reports more useful
3. **Set Goals** - Track your savings progress
4. **Check Reports** - Review monthly to stay on track
5. **Export Data** - Backup important financial records
6. **Use Help** - Stuck? Access help anytime from any menu!

## 🌟 Example Workflow
```
1. Login → 2. Add transactions → 3. View dashboard
                ↓
4. Set savings goal → 5. Check progress → 6. Export data
                ↓
        Need help? Press Help button anytime!
```

## 📊 Sample Output
```
=== 📊 DASHBOARD SUMMARY ===
💰 Total Income:  5000.00
💸 Total Expense: 3200.00
🧾 Balance:       1800.00

📂 CATEGORY BREAKDOWN
Salary          | Income: 5000.00 | Expense: 0.00
Groceries       | Income: 0.00    | Expense: 800.00
Rent            | Income: 0.00    | Expense: 1500.00
```

## 🤝 Getting Help

### 🆘 In-App Help System
- Step-by-step tutorials
- Interactive Q&A
- Direct links to features
- Color-coded guidance (✅ success, ❌ error, ℹ️ info)
Access from:
- **Main Menu → Help**
- **User Menu → Help**

### Help Topics Available
- Getting started (for first-time users)
- Transaction management
- Reports and analytics
- Data import/export
- User account management
- Security tips
- Quick tips for success

## ✨ Features Walkthrough

### Main Menu
```
💸 Your Personal Finance Manager
1. 🪪 Create User
2. 🔓 Login
3. ❓ Help
4. 🔚 Exit
```

### User Menu (After Login)
```
👤 Welcome, [Username]
1. 👁️ View Profile
2. 🔑 Change Password
3. 🔄 Switch User
4. 💰 Transactions Menu
5. 📊 Reports Menu
6. 📂 Data Management
7. ❓ Help
8. 🔒 Logout
```