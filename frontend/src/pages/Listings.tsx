import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

interface Property {
  id: number; title: string; city: string;
  price: number; type: string; size: number; image_url?: string | null;
}



export default function Listings() {
  const { user } = useAuth();
  const [properties, setProperties] = useState<Property[]>([]);
  const [filters, setFilters] = useState({ city: "", min_price: "", max_price: "", type: "" });
  const [showForm, setShowForm] = useState(false);
  const [newProp, setNewProp] = useState({ title: "", city: "", price: "", type: "apartment", size: "", image_url: "" });
  const [formMsg, setFormMsg] = useState("");

  async function fetchProperties() {
    const params = Object.fromEntries(Object.entries(filters).filter(([, v]) => v !== ""));
    const res = await api.get("/properties/", { params });
    setProperties(res.data);
  }

  useEffect(() => { fetchProperties(); }, []);

  async function handleAddProperty(e: React.FormEvent) {
    e.preventDefault();
    setFormMsg("");
    try {
      await api.post("/properties/", {
        title: newProp.title,
        city: newProp.city,
        price: Number(newProp.price),
        type: newProp.type,
        size: Number(newProp.size),
        image_url: newProp.image_url || null,
      });
      setFormMsg("Property listed successfully!");
      setNewProp({ title: "", city: "", price: "", type: "apartment", size: "", image_url: "" });
      fetchProperties();
    } catch {
      setFormMsg("Failed to add property.");
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold text-gray-800">Property Listings</h1>
        {user?.role === "agent" && (
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-indigo-700"
          >
            {showForm ? "Cancel" : "+ Add Property"}
          </button>
        )}
      </div>

      {/* Agent: add property form */}
      {showForm && user?.role === "agent" && (
        <div className="bg-white rounded-xl shadow p-6 mb-6 space-y-3">
          <h2 className="font-medium text-gray-700">New listing</h2>
          {formMsg && <p className="text-sm text-green-600">{formMsg}</p>}
          <form onSubmit={handleAddProperty} className="grid grid-cols-2 gap-3">
            <input className="border rounded-lg px-3 py-2 text-sm col-span-2"
              placeholder="Title" value={newProp.title} required
              onChange={e => setNewProp({ ...newProp, title: e.target.value })} />
            <input className="border rounded-lg px-3 py-2 text-sm"
              placeholder="City" value={newProp.city} required
              onChange={e => setNewProp({ ...newProp, city: e.target.value })} />
            <select className="border rounded-lg px-3 py-2 text-sm"
              value={newProp.type}
              onChange={e => setNewProp({ ...newProp, type: e.target.value })}>
              <option value="apartment">Apartment</option>
              <option value="house">House</option>
              <option value="villa">Villa</option>
              <option value="plot">Plot</option>
            </select>
            <input className="border rounded-lg px-3 py-2 text-sm"
              placeholder="Price (₹)" type="number" value={newProp.price} required
              onChange={e => setNewProp({ ...newProp, price: e.target.value })} />
            <input className="border rounded-lg px-3 py-2 text-sm"
              placeholder="Size (sqft)" type="number" value={newProp.size} required
              onChange={e => setNewProp({ ...newProp, size: e.target.value })} />
            <input className="border rounded-lg px-3 py-2 text-sm col-span-2"
              placeholder="Image URL (optional — paste any public image link)"
              value={newProp.image_url}
              onChange={e => setNewProp({ ...newProp, image_url: e.target.value })} />
              
            <button className="col-span-2 bg-indigo-600 text-white py-2 rounded-lg text-sm hover:bg-indigo-700">
              Submit Listing
            </button>
          </form>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-xl shadow p-4 mb-6 flex flex-wrap gap-3">
        <input className="border rounded-lg px-3 py-2 text-sm flex-1 min-w-[140px]"
          placeholder="City" value={filters.city}
          onChange={e => setFilters({ ...filters, city: e.target.value })} />
        <input className="border rounded-lg px-3 py-2 text-sm flex-1 min-w-[120px]"
          placeholder="Min price" type="number" value={filters.min_price}
          onChange={e => setFilters({ ...filters, min_price: e.target.value })} />
        <input className="border rounded-lg px-3 py-2 text-sm flex-1 min-w-[120px]"
          placeholder="Max price" type="number" value={filters.max_price}
          onChange={e => setFilters({ ...filters, max_price: e.target.value })} />
        <select className="border rounded-lg px-3 py-2 text-sm flex-1 min-w-[120px]"
          value={filters.type} onChange={e => setFilters({ ...filters, type: e.target.value })}>
          <option value="">All types</option>
          <option value="apartment">Apartment</option>
          <option value="house">House</option>
          <option value="villa">Villa</option>
          <option value="plot">Plot</option>
        </select>
        <button onClick={fetchProperties}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-indigo-700">
          Search
        </button>
      </div>

      {/* Grid */}
      {properties.length === 0 ? (
        <p className="text-gray-500 text-sm">No properties found.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {properties.map(p => (
            <Link to={`/properties/${p.id}`} key={p.id}
              className="bg-white rounded-xl shadow hover:shadow-md transition overflow-hidden">
              {/* image */}
              <div className="h-44 bg-gray-100 overflow-hidden">
                {p.image_url
                  ? <img src={p.image_url} alt={p.title} className="w-full h-full object-cover" />
                  : <div className="w-full h-full flex items-center justify-center text-gray-300 text-sm">No image</div>
                }
              </div>
              {/* card body */}
              <div className="p-4 space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full">{p.type}</span>
                  <span className="text-xs text-gray-400">{p.size} sqft</span>
                </div>
                <h2 className="font-medium text-gray-800">{p.title}</h2>
                <p className="text-sm text-gray-500">{p.city}</p>
                <p className="text-indigo-600 font-semibold">₹{p.price.toLocaleString()}</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}