import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Listings from "./pages/Listings";
import PropertyDetail from "./pages/PropertyDetail";
import Favorites from "./pages/Favorites";
import Dashboard from "./pages/Dashboard";
import React from "react";

// Change JSX.Element to React.ReactNode
function PrivateRoute({ children, role }: { children: React.ReactNode; role?: string }) {
  const { user } = useAuth();
  
  if (!user) return <Navigate to="/login" />;
  if (role && user.role !== role) return <Navigate to="/" />;
  
  return <>{children}</>; // Wrapping in a fragment is safer for returning children
}

export default function App() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      {user && <Navbar />}
      <Routes>
        {/* root → listings if logged in, else login */}
        <Route path="/" element={user ? <Listings /> : <Navigate to="/login" />} />
        <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
        <Route path="/register" element={!user ? <Register /> : <Navigate to="/" />} />
        <Route path="/properties/:id" element={
          <PrivateRoute><PropertyDetail /></PrivateRoute>
        } />
        <Route path="/favorites" element={
          <PrivateRoute role="user"><Favorites /></PrivateRoute>
        } />
        <Route path="/dashboard" element={
          <PrivateRoute role="agent"><Dashboard /></PrivateRoute>
        } />
      </Routes>
    </div>
  );
}