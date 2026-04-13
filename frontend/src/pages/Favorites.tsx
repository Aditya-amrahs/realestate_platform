import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

interface Favorite { id: number; property_id: number; }

export default function Favorites() {
  const [favorites, setFavorites] = useState<Favorite[]>([]);

  async function fetchFavorites() {
    const res = await api.get("/favorites/");
    setFavorites(res.data);
  }

  async function remove(property_id: number) {
    await api.delete(`/favorites/${property_id}`);
    fetchFavorites();
  }

  useEffect(() => { fetchFavorites(); }, []);

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-semibold text-gray-800 mb-6">My Favorites</h1>
      {favorites.length === 0 ? (
        <p className="text-gray-500 text-sm">No favorites yet. Browse listings to add some.</p>
      ) : (
        <div className="space-y-3">
          {favorites.map(f => (
            <div key={f.id} className="bg-white rounded-xl shadow p-4 flex items-center justify-between">
              <Link to={`/properties/${f.property_id}`}
                className="text-indigo-600 hover:underline text-sm">
                Property #{f.property_id}
              </Link>
              <button onClick={() => remove(f.property_id)}
                className="text-xs text-red-500 hover:underline">Remove</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}