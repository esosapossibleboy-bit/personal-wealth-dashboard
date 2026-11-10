# 📈 Full-Stack Personal Wealth Analytics Dashboard

A high-performance, full-stack personal finance tracking utility engineered with an asynchronous architecture. The application enables users to log financial transactions, perform dynamic real-time accounting calculations, monitor localized budget safety thresholds, and visualize capital allocation matrixes seamlessly inside a modern user interface.

---

## 🚀 Key Engineering & Structural Features

* **Asynchronous Full-Stack Architecture:** Coordinates an decoupled frontend visual client with a localized Python server using cross-origin resource sharing (CORS) protocols.
* **Dynamic Budget Event Listeners:** Watches database state parameters in real time, automatically deploying warning system banners if spending debits cross customizable threshold ceilings (set to \$1,000.00).
* **Live Mathematical Data Visualization:** Integrates Chart.js via a high-availability CDN network to compute and render real-time asset vs. liability allocation doughnut charts dynamically.
* **Persistent Hardware Registry Ledger:** Restructures runtime object profiles into serialized JSON strings, bypassing volatile temporary memory (RAM) bounds to preserve transaction data inside a physical text-file ledger database.
* **Full Data Lifecycle Pipeline (CRUD):** Implements specialized micro-route canals allowing the system to append assets, index log coordinates, map tables, and fire server-side database purges via distinct execution keys.

---

## 🛠️ Technology Stack

* **Frontend Engine:** HTML5, CSS3, JavaScript (ES6+ Asynchronous Fetch Core)
* **Visual Rendering Layer:** Chart.js Engine Matrix
* **Backend Core Routing:** Python 3, Flask Micro-Framework, Flask-CORS
* **Version Control Architecture:** Git, GitHub Registry Channels

---

## 💻 Local System Architecture & Installation

Follow these operational deployment steps to fire up the system workspace locally on your machine:

### 1. Initialize the Environment & Dependencies
Open your computer terminal and download the required backend pipeline packages:
```bash
pip install flask flask-cors
```

### 2. Boot Up the Python API Server Machine
Navigate into your project source directory and start the Flask network host server to listen on port `8000`:
```bash
python finance_server.py
```

### 3. Launch the Analytical Dashboard Interface
There is no build compile step required for the client view. Simply run the `finance_app.html` file using your development environment's Live Server expansion tool, or drop the local directory path directly into any modern web browser window:
```text
http://localhost:5500/finance_app.html
```

---

## 🔍 System Pipeline Architecture Blueprint

```text
  [ Client Frontend Dashboard View ]  <--->  [ Asynchronous Fetch Bridge ]
                  ^                                          |
                  | (JSON Data Packages)                     v
        [ Chart.js Metric Matrix ]            [ Flask API Server Core (Port 8000) ]
                                                             |
                                                             v
                                             [ Persistent flat-file Data Ledger ]
```
