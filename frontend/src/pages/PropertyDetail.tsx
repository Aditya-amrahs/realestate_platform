import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

interface Property {
  id: number; title: string; city: string;
  price: number; type: string; size: number; agent_id: number;
}

export default function PropertyDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [property, setProperty] = useState<Property | null>(null);
  const [booking, setBooking] = useState({ visit_date: "", visit_time: "" });
  const [msg, setMsg] = useState("");

  useEffect(() => {
    api.get(`/properties/${id}`).then(r => setProperty(r.data));
  }, [id]);

  async function handleBook(e: React.FormEvent) {
    e.preventDefault();
    setMsg("");
    try {
      await api.post("/bookings/", {
        property_id: Number(id),
        visit_date: booking.visit_date,
        visit_time: booking.visit_time,
      });
      setMsg("Booking confirmed!");
    } catch (err: any) {
      setMsg(err.response?.data?.detail || "Booking failed");
    }
  }

  async function handleFavorite() {
    try {
      await api.post(`/favorites/${id}`);
      setMsg("Added to favorites!");
    } catch (err: any) {
      setMsg(err.response?.data?.detail || "Could not add to favorites");
    }
  }

  if (!property) return <div className="p-8 text-gray-500">Loading...</div>;

  return (
    <div className="max-w-2xl mx-auto px-4 py-10">
      <button onClick={() => navigate(-1)} className="text-sm text-indigo-600 mb-4 hover:underline">← Back</button>
      <div className="bg-white rounded-xl shadow p-6 space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full">{property.type}</span>
          <span className="text-xs text-gray-400">{property.size} sqft</span>
        </div>
        <h1 className="text-2xl font-semibold text-gray-800">{property.title}</h1>
        <p className="text-gray-500">{property.city}</p>
        <p className="text-2xl font-bold text-indigo-600">₹{property.price.toLocaleString()}</p>
        <p className="text-xs text-gray-400">Listed by Agent #{property.agent_id}</p>

        {msg && <p className="text-sm text-green-600">{msg}</p>}

        {user?.role === "user" && (
          <div className="space-y-4 pt-4 border-t">
            <button onClick={handleFavorite}
              className="w-full border border-indigo-600 text-indigo-600 py-2 rounded-lg text-sm hover:bg-indigo-50">
              Save to Favorites
            </button>
            <form onSubmit={handleBook} className="space-y-3">
              <h2 className="font-medium text-gray-700">Book a site visit</h2>
              <input type="date" required
                className="w-full border rounded-lg px-3 py-2 text-sm"
                value={booking.visit_date}
                onChange={e => setBooking({ ...booking, visit_date: e.target.value })} />
              <input type="time" required
                className="w-full border rounded-lg px-3 py-2 text-sm"
                value={booking.visit_time}
                onChange={e => setBooking({ ...booking, visit_time: e.target.value })} />
              <button className="w-full bg-indigo-600 text-white py-2 rounded-lg text-sm hover:bg-indigo-700">
                Confirm Booking
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}