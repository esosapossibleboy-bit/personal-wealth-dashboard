import { useState } from "react";

interface LoginScreenProps {
  apiBaseUrl: string;
  onLoginSuccess: (token: string) => void;
}

export default function LoginScreen({ apiBaseUrl, onLoginSuccess }: LoginScreenProps) {
  const [isLoginMode, setIsLoginMode] = useState<boolean>(true);
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const handleAuth = async () => {
    if (!username || !password) {
      alert("⚠️ Please enter both a username and a password!");
      return;
    }

    const endpoint = isLoginMode ? "/auth/login" : "/auth/register";
    try {
      const res = await fetch(`${apiBaseUrl}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();

      if (data.status === "Success") {
        if (isLoginMode) {
          localStorage.setItem("vault_token", data.token);
          onLoginSuccess(data.token);
        } else {
          alert("✅ " + data.message);
          setIsLoginMode(true);
        }
      } else {
        alert("❌ " + data.message);
      }
    } catch {
      alert("🚨 CONNECTION ERROR: Server may be waking up. Wait 30 seconds and try again.");
    }
  };

  return (
    <div className="auth-panel">
      <h2>{isLoginMode ? "Account Login" : "Register Account"}</h2>
      <input
        type="text"
        className="auth-input"
        placeholder="Enter Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        className="auth-input"
        placeholder="Enter Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button className="auth-btn" onClick={handleAuth}>
        {isLoginMode ? "Sign In" : "Create Account"}
      </button>
      <span className="toggle-link" onClick={() => setIsLoginMode(!isLoginMode)}>
        {isLoginMode ? "Don't have an account? Register here" : "Already registered? Login here"}
      </span>
    </div>
  );
}
