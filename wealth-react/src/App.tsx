import { useState, useEffect } from "react";
import LoginScreen from "./LoginScreen";
import "./App.css";

const API_BASE_URL = "https://esosa-wealth-api.onrender.com";
const MONTHLY_BUDGET_CAP = 1000.0;

interface Transaction {
  id: number;
  type: "Income" | "Expense";
  amount: number;
  category: string;
  description: string;
}

interface LedgerData {
  transactions: Transaction[];
  total_income: number;
  total_expense: number;
  balance: number;
}

export default function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem("vault_token"));
  const [ledger, setLedger] = useState<LedgerData>({ transactions: [], total_income: 0, total_expense: 0, balance: 0 });
  const [txType, setTxType] = useState<"Income" | "Expense">("Income");
  const [amountInput, setAmountInput] = useState<string>("");
  const [category, setCategory] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [formatError, setFormatError] = useState<boolean>(false);

  useEffect(() => {
    if (token) fetchLedger();
  }, [token]);

  const getAuthHeaders = () => ({ "Content-Type": "application/json", Authorization: `Bearer ${token}` });

  const handleLogout = () => {
    localStorage.removeItem("vault_token");
    setToken(null);
  };

  const fetchLedger = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/ledger`, { headers: getAuthHeaders() });
      if (res.status === 401) return handleLogout();
      setLedger(await res.json());
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddTransaction = async () => {
    const trimmed = amountInput.trim();
    if (trimmed.includes("$") || trimmed.includes(",")) return setFormatError(true);
    setFormatError(false);

    const parsedAmount = parseFloat(trimmed);
    if (isNaN(parsedAmount) || parsedAmount <= 0 || !category) return;

    await fetch(`${API_BASE_URL}/add`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ type: txType, amount: parsedAmount, category, description }),
    });
    setAmountInput("");
    setCategory("");
    setDescription("");
    fetchLedger();
  };

  const handleDelete = async (txId: number) => {
    await fetch(`${API_BASE_URL}/delete`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ tx_id: txId }),
    });
    fetchLedger();
  };

  const exportToCSV = () => {
    if (ledger.transactions.length === 0) return alert("⚠️ No transactions available to export!");
    const csvRows = ["Type,Amount,Category,Description"];
    ledger.transactions.forEach((item) => {
      csvRows.push(`${item.type},${item.amount.toFixed(2)},${item.category.replace(/,/g, " ")},${(item.description || "").replace(/,/g, " ")}`);
    });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(new Blob([csvRows.join("\n")], { type: "text/csv" }));
    link.download = "wealth_vault_react_ledger.csv";
    link.click();
  };

  if (!token) return <LoginScreen apiBaseUrl={API_BASE_URL} onLoginSuccess={setToken} />;

  const savedAmount = Math.max(0, ledger.total_income - ledger.total_expense);
  const savedPct = ledger.total_income > 0 ? Math.round((savedAmount / ledger.total_income) * 100) : 100;
  const expensePct = ledger.total_income > 0 ? Math.round((ledger.total_expense / ledger.total_income) * 100) : 0;

  return (
    <div className="wrapper">
      <div className="nav-header">
        <div>
          <h1>📈 Esosa Wealth Vault (React + TS)</h1>
          <p style={{ color: "#8f9cae", margin: 0 }}>PostgreSQL Cloud Core • JWT Secured</p>
        </div>
        <button className="logout-btn" onClick={handleLogout}>Disconnect Engine</button>
      </div>

      {ledger.total_expense > MONTHLY_BUDGET_CAP && (
        <div className="budget-alert" style={{ display: "block" }}>⚠️ WARNING: Your monthly outflow threshold has broken past your budget constraints!</div>
      )}
      {formatError && (
        <div className="input-warning" style={{ display: "block" }}>⚠️ INPUT FORMAT DETECTED: Please write plain math numbers only!</div>
      )}

      <div className="metrics-grid">
        <div className="metric-card"><h3>Net Valuation</h3><p className="balance">${ledger.balance.toLocaleString("en-US", { minimumFractionDigits: 2 })}</p></div>
        <div className="metric-card"><h3>Total Inflows</h3><p className="income">${ledger.total_income.toLocaleString("en-US", { minimumFractionDigits: 2 })}</p></div>
        <div className="metric-card"><h3>Total Outflows</h3><p className="expense">${ledger.total_expense.toLocaleString("en-US", { minimumFractionDigits: 2 })}</p></div>
      </div>

      <div className="form-panel">
        <select value={txType} onChange={(e) => setTxType(e.target.value as "Income" | "Expense")}>
          <option value="Income">Income (+)</option>
          <option value="Expense">Expense (-)</option>
        </select>
        <input type="text" placeholder="Amount ($)" style={{ width: "110px" }} value={amountInput} onChange={(e) => setAmountInput(e.target.value)} />
        <input type="text" placeholder="Category" value={category} onChange={(e) => setCategory(e.target.value)} />
        <input type="text" placeholder="Description Note" style={{ width: "220px" }} value={description} onChange={(e) => setDescription(e.target.value)} />
        <button className="post-btn" onClick={handleAddTransaction}>Post Record</button>
      </div>

      <div className="workspace">
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h2>📋 Audit History Log</h2>
            <button onClick={exportToCSV} style={{ background: "#2cfd73", color: "#0b0f19", border: "none", padding: "8px 14px", borderRadius: "6px", fontWeight: "bold", cursor: "pointer" }}>
              📥 Export CSV
            </button>
          </div>
          <table>
            <thead><tr><th>Type</th><th>Amount</th><th>Category</th><th>Description</th><th>Action</th></tr></thead>
            <tbody>
              {ledger.transactions.slice().reverse().map((item) => (
                <tr key={item.id}>
                  <td><span className={`badge ${item.type === "Income" ? "badge-income" : "badge-expense"}`}>{item.type.toUpperCase()}</span></td>
                  <td className={item.type === "Income" ? "income" : "expense"}>${item.amount.toFixed(2)}</td>
                  <td><strong>{item.category}</strong></td>
                  <td style={{ color: "#8f9cae" }}>{item.description}</td>
                  <td><button className="delete-btn" onClick={() => handleDelete(item.id)}>Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="chart-box">
          <h2 style={{ marginTop: 0, fontSize: "16px", color: "#8f9cae" }}>📊 WEALTH OUTFLOW MATRIX</h2>
          <div className="matrix-labels">
            <span style={{ color: "#2cfd73" }}>● Saved Net Wealth ({savedPct}%)</span><br />
            <span style={{ color: "#ff4a5a" }}>● Expenses Outflow ({expensePct}%)</span>
          </div>
          <div className="bar-container">
            <div id="matrix-bar-saved" style={{ width: `${savedPct}%` }}></div>
            <div id="matrix-bar-expense" style={{ width: `${expensePct}%` }}></div>
          </div>
        </div>
      </div>
    </div>
  );
}
