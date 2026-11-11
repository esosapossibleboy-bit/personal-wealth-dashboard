# 📈 Esosa Wealth Vault — Full-Stack Personal Finance Analytics Platform (v2.0)

A production-ready, multi-user full-stack financial tracking application engineered with **React**, **TypeScript**, **Python (Flask)**, and **PostgreSQL**. Users can securely register accounts, log cash inflows and expenses, monitor automated budget threshold alerts, visualize capital allocation matrices, and export ledgers to CSV spreadsheets.

🌐 **Live Production App:** [https://github.io](https://github.io)  
⚙️ **REST API Endpoint:** [https://onrender.com](https://onrender.com)

---

## 🚀 Key Engineering & Security Features

* **Modern React + TypeScript Frontend:** Rebuilt into modular, strongly typed UI components (`App.tsx`, `LoginScreen.tsx`) with strict TypeScript interfaces and reactive state management.
* **JWT Token Authentication & Account Isolation:** Secures user sessions using signed **JSON Web Tokens (HS256)** via `Authorization: Bearer` headers and **SHA-256 password hashing**, ensuring strict data isolation per user.
* **Permanent Cloud PostgreSQL Database:** Migrated from local storage to a relational **PostgreSQL** instance hosted on **Neon Cloud** using parameterized queries (`psycopg2`) to prevent SQL injection.
* **Automated API Security Testing (`pytest`):** Includes an automated unit and integration test suite (`test_api.py`) validating password hashing and rejecting unauthorized or tampered JWT requests.
* **Real-Time Financial Analytics & CSV Export:** Computes live net worth, dynamically adjusts proportional asset-vs-expense allocation bars, triggers budget limit warnings, and exports transaction history to `.csv` spreadsheets.

---

## 🛠️ Tech Stack

* **Frontend:** React, TypeScript, Vite, HTML5, CSS3
* **Backend:** Python 3, Flask, Flask-CORS, Gunicorn, PyJWT
* **Database:** PostgreSQL (Neon Cloud)
* **Testing:** Pytest
* **Cloud Deployment & DevOps:** Render (Backend API), GitHub Pages (Frontend Client), Git & GitHub

---

## 🏗️ System Architecture

```text
  [ React + TypeScript Client (GitHub Pages) ]
                      │
                      │  HTTPS REST API + JWT Bearer Token
                      ▼
  [ Python Flask + Gunicorn Server (Render Cloud) ]
                      │
                      │  Parameterized SQL Queries (psycopg2)
                      ▼
  [ Relational PostgreSQL Database (Neon Cloud) ]
```

---

## 💻 Local Setup & Running Tests

### 1. Start the Python Backend & Run Automated Tests
```bash
pip install -r requirements.txt
python -m pytest
python finance_server.py
```

### 2. Start the React + TypeScript Frontend
```bash
cd wealth-react
npm install
npm run dev
```
