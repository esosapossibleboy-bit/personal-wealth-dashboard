import json

# 📐 1. THE DATA BLUEPRINT: Stamping out structured financial items safely
class Transaction:
    def __init__(self, tx_type, amount, category, description):
        self.tx_type = tx_type          # "Income" or "Expense"
        self.amount = float(amount)     # Converts money inputs into decimals
        self.category = category        # e.g., "Food", "Salary", "Rent"
        self.description = description  # e.g., "Bought groceries"

    # Turns our item variables into a clean record box package for the hard drive
    def to_dictionary(self):
        return {
            "type": self.tx_type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }

# 📝 2. DATABASE RECIPE: Read past money logs from the hard drive ledger
def load_ledger():
    try:
        file = open("finance_ledger.txt", "r")
        lines = file.readlines()
        file.close()
        return [json.loads(line.strip()) for line in lines if line.strip()]
    except:
        return [] # Return a blank list if it's our first time running the app

# 📝 3. DATABASE RECIPE: Append a new record directly to physical storage
def save_to_ledger(transaction_obj):
    file = open("finance_ledger.txt", "a")
    record_line = json.dumps(transaction_obj.to_dictionary())
    file.write(record_line + "\n")
    file.close()

# ==========================================
# 🎠 THE CORE INTERACTIVE CORE MENU
# ==========================================
print("=== 📈 WELCOME TO YOUR PERSONAL FINANCE UTILITY ENGINE ===")

while True:
    ledger = load_ledger()
    
    # Calculate Net Worth Dynamically on every loop cycle!
    total_income = sum(item["amount"] for item in ledger if item["type"] == "Income")
    total_expense = sum(item["amount"] for item in ledger if item["type"] == "Expense")
    current_balance = total_income - total_expense

    print("\n----------------------------------")
    print(f"💰 CURRENT BALANCING SUMMARY: ${current_balance:,.2f}")
    print(f"📥 Total Income: ${total_income:,.2f} | 📤 Total Expenses: ${total_expense:,.2f}")
    print("----------------------------------")
    print("1. ➕ Add Transaction Record")
    print("2. 📋 View Complete Ledger Log")
    print("3. 🚪 Exit App Engine")
    
    choice = input("\nSelect a system route (1-3): ")
    
    if choice == "1":
        print("\n--- CREATE TRANSACTION NEW ASSET ---")
        t_type = input("Is this an 'Income' or 'Expense'? ").strip().capitalize()
        if t_type not in ["Income", "Expense"]:
            print("❌ Invalid type specification! Choose 'Income' or 'Expense'.")
            continue
            
        amount_input = input("Enter the monetary amount ($): ")
        category_input = input("Enter a category (e.g., Food, Salary, Entertainment): ").strip()
        desc_input = input("Enter a quick description: ").strip()
        
        try:
            # Instantiate our transaction object stamp
            new_tx = Transaction(t_type, amount_input, category_input, desc_input)
            save_to_ledger(new_tx)
            print(f"✅ Success! Permanently recorded ${float(amount_input):.2f} to database.")
        except Exception as e:
            print("❌ Error processing calculation entries. Verify numeric formatting input.")
            
    elif choice == "2":
        print("\n📋 HISTORICAL REPOSITORY LEDGER LOG:")
        if not ledger:
            print("[Empty Database Ledger - Add your first transaction record!]")
        for idx, item in enumerate(ledger):
            prefix = "🟢 [INCOME]" if item["type"] == "Income" else "🔴 [EXPENSE]"
            print(f"{idx + 1}. {prefix} ${item['amount']:,.2f} | {item['category']} -> {item['description']}")
            
    elif choice == "3":
        print("👋 Closing finance data loops securely. System shutdown complete.")
        break
    else:
        print("❌ Invalid route instruction code selected!")
