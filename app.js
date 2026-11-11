// ☁️ CONNECTED DIRECTLY TO THE LIVE PRODUCTION CLOUD APP SERVER CHANNEL:
// Swap this string URL out with your actual unique link from the Render Cloud interface!
const API_BASE_URL = "URL https://esosa-wealth-api.onrender.com";
const MONTHLY_BUDGET_CAP = 1000.00;
let isLoginMode = true;

window.onload = checkActiveSession;

// 🔐 SESSION MONITORING ENGINE
function checkActiveSession() {
    let uid = localStorage.getItem("vault_user_id");
    if (uid) {
        document.getElementById("auth-screen").style.display = "none";
        document.getElementById("app-screen").style.display = "block";
        fetchLedgerDataLogs(uid);
    }
}

function toggleAuthMode() {
    isLoginMode = !isLoginMode;
    document.getElementById("auth-title").innerHTML = isLoginMode ? "Account Login" : "Register Account";
    document.getElementById("auth-main-btn").innerHTML = isLoginMode ? "Sign In" : "Create Account";
    document.getElementById("auth-toggle").innerHTML = isLoginMode ? "Don't have an account? Register here" : "Already registered? Login here";
}

// 👥 SECURE NETWORK ACCESS ROUTER
function executeAuthAction() {
    let u = document.getElementById("auth-username").value, p = document.getElementById("auth-password").value;
    if (!u || !p) return;
    
    fetch(API_BASE_URL + (isLoginMode ? "/auth/login" : "/auth/register"), {
        method: "POST", 
        headers: { "Content-Type": "application/json" }, 
        body: JSON.stringify({ username: u, password: p })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "Success") {
            if (isLoginMode) { 
                localStorage.setItem("vault_user_id", data.user_id); 
                checkActiveSession(); 
            } else { 
                alert(data.message); 
                toggleAuthMode(); 
            }
        } else { alert("❌ " + data.message); }
    });
}

function logoutSession() { 
    localStorage.removeItem("vault_user_id"); 
    location.reload(); 
}

// 📊 NATIVE PROGRESSIVE ALLOCATION CALCULATOR
function updateNativeVisualization(inc, exp) {
    let savedWidth = 100;
    let expWidth = 0;

    if (inc > 0) {
        let savedAmount = inc - exp;
        if (savedAmount < 0) savedAmount = 0; 
        
        savedWidth = Math.round((savedAmount / inc) * 100);
        expWidth = Math.round((exp / inc) * 100);
    }

    document.getElementById("saved-pct").innerHTML = savedWidth;
    document.getElementById("expense-pct").innerHTML = expWidth;
    document.getElementById("matrix-bar-saved").style.width = savedWidth + "%";
    document.getElementById("matrix-bar-expense").style.width = expWidth + "%";
}

// 📋 DATA ACQUISITION & LOG VIEW MATRICES
function fetchLedgerDataLogs(uid) {
    fetch(`${API_BASE_URL}/ledger?user_id=${uid}`)
    .then(res => res.json())
    .then(data => {
        document.getElementById("net-balance").innerHTML = "$" + data.balance.toLocaleString('en-US', {minimumFractionDigits: 2});
        document.getElementById("total-income").innerHTML = "$" + data.total_income.toLocaleString('en-US', {minimumFractionDigits: 2});
        document.getElementById("total-expense").innerHTML = "$" + data.total_expense.toLocaleString('en-US', {minimumFractionDigits: 2});
        
        document.getElementById("budget-banner").style.display = data.total_expense > MONTHLY_BUDGET_CAP ? "block" : "none";
        
        updateNativeVisualization(data.total_income, data.total_expense);

        let rowsBox = document.getElementById("ledger-rows"); 
        rowsBox.innerHTML = "";
        
        data.transactions.reverse().forEach(item => {
            let row = document.createElement("tr"), bc = item.type === "Income" ? "badge-income" : "badge-expense";
            row.innerHTML = `
                <td><span class="badge ${bc}">${item.type.toUpperCase()}</span></td>
                <td class="${item.type === 'Income' ? 'income' : 'expense'}">$${item.amount.toFixed(2)}</td>
                <td><strong>${item.category}</strong></td>
                <td style="color: #8f9cae;">${item.description}</td>
                <td><button class="delete-btn" onclick="deleteTransactionAsset(${item.id})">Delete</button></td>
            `;
            rowsBox.appendChild(row);
        });
    });
}

// 🚨 VALIDATED ENTRY CONTROLLER PIPELINE
function logTransactionAsset() {
    let uid = localStorage.getItem("vault_user_id");
    let t = document.getElementById("tx-type").value;
    let a_raw = document.getElementById("tx-amount").value.trim();
    let c = document.getElementById("tx-category").value;
    let d = document.getElementById("tx-desc").value;
    let alertBox = document.getElementById("currency-format-alert");

    // 🔬 TYPO CAPTURE LAYER: Halts pipeline if illegal input modifiers are detected
    if (a_raw.includes("$") || a_raw.includes(",")) {
        if (alertBox) alertBox.style.display = "block";
        return; 
    }
    if (alertBox) alertBox.style.display = "none"; 

    let a = parseFloat(a_raw);
    if (isNaN(a) || a <= 0 || !c) return;

    fetch(API_BASE_URL + "/add", {
        method: "POST", 
        headers: { "Content-Type": "application/json" }, 
        body: JSON.stringify({ user_id: uid, type: t, amount: a, category: c, description: d })
    }).then(() => {
        document.getElementById("tx-amount").value = ""; 
        document.getElementById("tx-category").value = ""; 
        document.getElementById("tx-desc").value = "";
        fetchLedgerDataLogs(uid);
    });
}

function deleteTransactionAsset(txId) {
    let uid = localStorage.getItem("vault_user_id");
    fetch(API_BASE_URL + "/delete", {
        method: "POST", 
        headers: { "Content-Type": "application/json" }, 
        body: JSON.stringify({ tx_id: txId, user_id: uid })
    }).then(() => fetchLedgerDataLogs(uid));
}
