import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

print("\n🌐 Launching Esosa's Personal Wealth API Ledger... 🌐")
print("🚀 SUCCESS! Your transaction registry is live at: http://localhost:8000\n")

def load_ledger():
    try:
        file = open("finance_ledger.txt", "r")
        lines = file.readlines()
        file.close()
        return [json.loads(line.strip()) for line in lines if line.strip()]
    except:
        return []

def rewrite_ledger(ledger_list):
    file = open("finance_ledger.txt", "w")
    for item in ledger_list:
        file.write(json.dumps(item) + "\n")
    file.close()

@app.route("/ledger", methods=["GET"])
def get_ledger():
    ledger = load_ledger()
    total_income = sum(item["amount"] for item in ledger if item["type"] == "Income")
    total_expense = sum(item["amount"] for item in ledger if item["type"] == "Expense")
    balance = total_income - total_expense
    return jsonify({
        "transactions": ledger,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    })

@app.route("/add", methods=["POST"])
def add_transaction():
    data = request.json
    tx_record = {
        "type": data.get("type"),
        "amount": float(data.get("amount", 0)),
        "category": data.get("category"),
        "description": data.get("description")
    }
    ledger = load_ledger()
    ledger.append(tx_record)
    rewrite_ledger(ledger)
    return jsonify({"status": "Success", "message": "Transaction logged successfully!"})

# 🛣️ NEW ROADWAY: Erase a transaction from the ledger using its data index position
@app.route("/delete", methods=["POST"])
def delete_transaction():
    data = request.json
    index_to_delete = data.get("index")
    ledger = load_ledger()
    
    if 0 <= index_to_delete < len(ledger):
        removed = ledger.pop(index_to_delete)
        print(f"🗑️ PURGE WARNING: Erased {removed['type']} of ${removed['amount']} from ledger.")
        rewrite_ledger(ledger)
        return jsonify({"status": "Success", "message": "Transaction deleted!"})
    
    return jsonify({"status": "Error", "message": "Index not found"}), 400

if __name__ == "__main__":
    app.run(port=8000)
