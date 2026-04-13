import { useEffect, useState } from "react";
import api from "../api/axios";

interface Stats {
  properties_listed: number;
  total_bookings: number;
  total_views: number;
}

interface Property {
  id: number; title: string; city: string; price: number; type: string;
}

export default function Dashboard() {
  const [stats, setStats]           = useState<Stats | null>(null);
  const [properties, setProperties] = useState<Property[]>([]);
  const [delMsg, setDelMsg]         = useState("");

  async function fetchAll() {
    const [statsRes, propsRes] = await Promise.all([
      api.get("/analytics/dashboard"),
      api.get("/properties/"),
    ]);
    setStats(statsRes.data);
    setProperties(propsRes.data);
  }

  async function handleDelete(id: number) {
    setDelMsg("");
    try {
      await api.delete(`/properties/${id}`);
      setDelMsg("Property deleted.");
      fetchAll();
    } catch {
      setDelMsg("Could not delete — you may not own this property.");
    }
  }

  useEffect(() => { fetchAll(); }, []);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <h1 className="text-2xl font-semibold text-gray-800">Agent Dashboard</h1>

      {/* Stats cards */}
      {stats && (
        <div className="grid grid-cols-3 gap-4">
          {[
            { label: "Properties Listed", value: stats.properties_listed },
            { label: "Total Bookings",    value: stats.total_bookings },
            { label: "Total Views",       value: stats.total_views },
          ].map(card => (
            <div key={card.label} className="bg-white rounded-xl shadow p-6 text-center">
              <p className="text-3xl font-bold text-indigo-600">{card.value}</p>
              <p className="text-sm text-gray-500 mt-1">{card.label}</p>
            </div>
          ))}
        </div>
      )}

      {/* Property list with delete */}
      <div>
        <h2 className="text-lg font-medium text-gray-700 mb-3">All listings</h2>
        {delMsg && <p className="text-sm text-green-600 mb-2">{delMsg}</p>}
        <div className="space-y-3">
          {properties.map(p => (
            <div key={p.id} className="bg-white rounded-xl shadow p-4 flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-800 text-sm">{p.title}</p>
                <p className="text-xs text-gray-400">{p.city} · {p.type} · ₹{p.price.toLocaleString()}</p>
              </div>
              <button
                onClick={() => handleDelete(p.id)}
                className="text-xs text-red-500 hover:underline ml-4"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}