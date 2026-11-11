import os
import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔑 Reads your secret database URL from Render's environment settings
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    if not DATABASE_URL:
        print("⚠️ No DATABASE_URL found. Waiting for cloud configuration.")
        return
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username", "").strip().lower()
    password = data.get("password", "")
    
    if not username or not password:
        return jsonify({"status": "Error", "message": "Missing credentials"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hash_password(password)))
        conn.commit()
        return jsonify({"status": "Success", "message": "Account created permanently in cloud DB!"})
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"status": "Error", "message": "Username already taken"}), 400
    finally:
        cursor.close()
        conn.close()

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username", "").strip().lower()
    password = data.get("password", "")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        user_id, saved_hash = user
        if saved_hash == hash_password(password):
            return jsonify({"status": "Success", "message": "Login validated!", "user_id": user_id})
    return jsonify({"status": "Error", "message": "Invalid username or password"}), 401

@app.route("/ledger", methods=["GET"])
def get_ledger():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"status": "Error", "message": "Unauthorized"}), 401
        
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, type, amount, category, description FROM transactions WHERE user_id = %s ORDER BY id ASC", (user_id,))
    transactions = cursor.fetchall()
    
    total_income = sum(item["amount"] for item in transactions if item["type"] == "Income")
    total_expense = sum(item["amount"] for item in transactions if item["type"] == "Expense")
    
    cursor.close()
    conn.close()
    return jsonify({
        "transactions": transactions,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    })

@app.route("/add", methods=["POST"])
def add_transaction():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, type, amount, category, description) VALUES (%s, %s, %s, %s, %s)",
        (data.get("user_id"), data.get("type"), float(data.get("amount", 0)), data.get("category"), data.get("description"))
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "Success", "message": "Saved to PostgreSQL!"})

@app.route("/delete", methods=["POST"])
def delete_transaction():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = %s AND user_id = %s", (data.get("tx_id"), data.get("user_id")))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "Success", "message": "Deleted from PostgreSQL!"})

# Run table setup on startup
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
