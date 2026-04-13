import { useEffect, useState } from "react";
import api from "../api/axios";

interface Stats { properties_listed: number; total_bookings: number; total_views: number; }

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    api.get("/analytics/dashboard").then(r => setStats(r.data));
  }, []);

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-semibold text-gray-800 mb-6">Agent Dashboard</h1>
      {!stats ? (
        <p className="text-gray-500 text-sm">Loading...</p>
      ) : (
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
    </div>
  );
}