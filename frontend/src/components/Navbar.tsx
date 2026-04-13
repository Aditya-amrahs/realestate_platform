import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <Link to="/" className="text-xl font-semibold text-indigo-600">EstateApp</Link>
      <div className="flex items-center gap-4 text-sm">
        <Link to="/" className="text-gray-600 hover:text-indigo-600">Listings</Link>
        {user?.role === "user" && (
          <Link to="/favorites" className="text-gray-600 hover:text-indigo-600">Favorites</Link>
        )}
        {user?.role === "agent" && (
          <Link to="/dashboard" className="text-gray-600 hover:text-indigo-600">Dashboard</Link>
        )}
        {user ? (
          <button onClick={handleLogout} className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">
            Logout
          </button>
        ) : (
          <>
            <Link to="/login" className="text-gray-600 hover:text-indigo-600">Login</Link>
            <Link to="/register" className="bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-700">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}