import os
import sqlite3
import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Opens the security window so the public web can talk to us

DB_FILE = "wealth_vault.db"

# 🏛️ DATABASE ARCHITECTURE CREATOR
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 👥 Create Users Table (Stores usernames and securely encrypted passwords)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)
    
    # 📊 Create Transactions Table (Linked directly to user IDs)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

# 📝 HELPER RECIPE: Securely convert plain text passwords into a custom math hash code
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 🛣️ ACCOUNT CANAL 1: User Registration
@app.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username", "").strip().lower()
    password = data.get("password", "")
    
    if not username or not password:
        return jsonify({"status": "Error", "message": "Missing credentials"}), 400
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return jsonify({"status": "Success", "message": "Account created! You can log in now."})
    except sqlite3.IntegrityError:
        return jsonify({"status": "Error", "message": "Username already taken"}), 400
    finally:
        conn.close()

# 🛣️ ACCOUNT CANAL 2: User Login
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username", "").strip().lower()
    password = data.get("password", "")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[1] == hash_password(password):
        return jsonify({"status": "Success", "message": "Login validated!", "user_id": user[0]})
    return jsonify({"status": "Error", "message": "Invalid username or password"}), 401

# # 🛣️ DATA CANAL 3: Get User Ledger Metrics and SQL Data Rows
@app.route("/ledger", methods=["GET"])
def get_ledger():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"status": "Error", "message": "Unauthorized navigation"}), 401
        
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # Allows pulling database columns by their label names
    cursor = conn.cursor()
    
    cursor.execute("SELECT type, amount, category, description, id FROM transactions WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    
    transactions = [dict(row) for row in rows]
    total_income = sum(item["amount"] for item in transactions if item["type"] == "Income")
    total_expense = sum(item["amount"] for item in transactions if item["type"] == "Expense")
    
    conn.close()
    return jsonify({
        "transactions": transactions,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    })

# 🛣️ DATA CANAL 4: Post New Transaction Record
@app.route("/add", methods=["POST"])
def add_transaction():
    data = request.json
    user_id = data.get("user_id")
    tx_type = data.get("type")
    amount = float(data.get("amount", 0))
    category = data.get("category")
    description = data.get("description")
    
    if not user_id:
        return jsonify({"status": "Error", "message": "Unauthorized operational request"}), 401
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (user_id, type, amount, category, description) VALUES (?, ?, ?, ?, ?)",
                   (user_id, tx_type, amount, category, description))
    conn.commit()
    conn.close()
    return jsonify({"status": "Success", "message": "Transaction logged to SQL server!"})

# 🛣️ DATA CANAL 5: Delete explicit record from SQL row index
@app.route("/delete", methods=["POST"])
def delete_transaction():
    data = request.json
    tx_id = data.get("tx_id")
    user_id = data.get("user_id")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (tx_id, user_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "Success", "message": "Row deleted from SQL ledger"})

if __name__ == "__main__":
    init_db() # Run database setup checklist automatically on start
    # Read the dynamic deployment port from Render Cloud, or use 8000 locally
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
