import os
import datetime
import hashlib
import jwt
import psycopg2
from psycopg2.extras import RealDictCursor
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")
# 🔑 Secret cryptographic key used to sign VIP JWT wristbands
SECRET_KEY = os.environ.get("SECRET_KEY", "esosa-super-secret-dev-key-2026")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    if not DATABASE_URL:
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

# 🛡️ SECURITY BOUNCER DECORATOR: Verifies the JWT wristband on protected routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"status": "Error", "message": "Missing or invalid security token"}), 401
        
        token = auth_header.split(" ")
        try:
            # Decode and verify the digital signature
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"status": "Error", "message": "Session expired. Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"status": "Error", "message": "Tampered or invalid token!"}), 401
            
        return f(current_user_id, *args, **kwargs)
    return decorated

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
        return jsonify({"status": "Success", "message": "Account created permanently!"})
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
            # 🎟️ Mint a signed JWT token valid for 24 hours
            token = jwt.encode({
                "user_id": user_id,
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
            }, SECRET_KEY, algorithm="HS256")
            
            return jsonify({"status": "Success", "message": "Login validated!", "token": token})
            
    return jsonify({"status": "Error", "message": "Invalid username or password"}), 401

@app.route("/ledger", methods=["GET"])
@token_required
def get_ledger(current_user_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, type, amount, category, description FROM transactions WHERE user_id = %s ORDER BY id ASC", (current_user_id,))
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
@token_required
def add_transaction(current_user_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, type, amount, category, description) VALUES (%s, %s, %s, %s, %s)",
        (current_user_id, data.get("type"), float(data.get("amount", 0)), data.get("category"), data.get("description"))
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "Success", "message": "Saved securely with JWT!"})

@app.route("/delete", methods=["POST"])
@token_required
def delete_transaction(current_user_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = %s AND user_id = %s", (data.get("tx_id"), current_user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "Success", "message": "Deleted securely!"})

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
