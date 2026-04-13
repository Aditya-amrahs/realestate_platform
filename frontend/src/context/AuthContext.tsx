import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";
import { jwtDecode } from "jwt-decode";

interface AuthUser {
  id: number;
  role: string;
}

interface AuthContextType {
  user: AuthUser | null;
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [user, setUser] = useState<AuthUser | null>(() => {
    const t = localStorage.getItem("token");
    if (!t) return null;
    try { return jwtDecode<AuthUser>(t); }
    catch { return null; }
  });

  function login(newToken: string) {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    setUser(jwtDecode<AuthUser>(newToken));
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be inside AuthProvider");
  return ctx;
}